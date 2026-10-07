"""Article generation.

Produces an article record containing real calculator output, a structured outline,
FAQ, and prose. Uses Gemini when GEMINI_API_KEY is set; otherwise a deterministic
writer produces a genuinely useful draft from the calculator data (so the pipeline
is fully testable offline and never ships an empty page).
"""
from __future__ import annotations

import datetime as dt
import json
import re

import calculators
import llm
from common import (DATA, load_json, save_json, seo_config, slugify, topics_config,
                    word_count)

SYSTEM = (
    "You are an experienced home-improvement and gardening writer. You write clear, "
    "specific, genuinely useful articles. Rules: never invent statistics or studies; "
    "use plain English; short paragraphs; use the exact numbers provided; do not use "
    "filler phrases like 'in today's fast-paced world' or 'it is important to note'; "
    "never claim guaranteed results. Output Markdown only, no code fences."
)

OUTLINE_PROMPT = """Write a practical article for the keyword: "{kw}".

Cluster: {cluster}
Primary keyword: {kw}
Secondary keywords: {secondary}
Calculator available: {calc_title}

The article MUST:
- Open with a direct answer to the search query in the first 2 sentences.
- Include a section titled exactly "## How to Calculate {calc_short}"
- Include a worked example using these REAL computed numbers:
{worked}
- Include a "## How Much You Need at Common Sizes" section (a table is provided; keep it).
- Include "## Common Mistakes to Avoid"
- Be 900-1500 words, Markdown, with ## and ### headings only (no H1; the page supplies it).
- Mention the secondary keywords naturally, never stuffed.

Accurate domain facts you may use (do not invent others):
{facts}

Reference table to include verbatim under "How Much You Need at Common Sizes":
{size_table}

Return only the Markdown body."""

FALLBACK_SECTIONS = [
    ("How to Calculate {short}", None),
    ("Worked Example", None),
    ("Common Mistakes to Avoid", [
        "Estimating by eye instead of measuring the actual area.",
        "Forgetting the depth or thickness requirement for the job.",
        "Skipping the waste allowance, then running short mid-project.",
        "Buying the cheapest option that does not suit the application.",
    ]),
    ("Choosing the Right Material", None),
    ("Frequently Asked Questions", None),
]

FAQ_TEMPLATES = {
    "mulch": [
        ("How deep should mulch be?", "Two to three inches for most beds. More than four inches can hold too much moisture against stems."),
        ("How many bags of mulch is a cubic yard?", "Thirteen and a half 2-cubic-foot bags, since a cubic yard is 27 cubic feet."),
        ("When is the best time to mulch?", "Early spring, after the soil has warmed, and again in autumn if you want winter protection."),
        ("Does mulch prevent weeds?", "It suppresses most weeds if the layer is at least two inches deep and kept clear of plant stems."),
    ],
    "soil": [
        ("How much soil do I need for a raised bed?", "Multiply length by width by depth in feet. An 8x4 ft bed 12 inches deep needs 32 cubic feet, about 1.2 cubic yards."),
        ("What is the best soil mix for a raised bed?", "A common blend is 60% topsoil, 30% compost and 10% perlite or coarse sand for drainage."),
        ("Do I need a liner under a raised bed?", "On soil, no. On concrete or gravel, use landscape fabric to stop weeds and slow drainage loss."),
        ("How deep should a raised bed be?", "Ten to twelve inches for most vegetables; six inches is enough for shallow-rooted herbs and salads."),
    ],
    "gravel": [
        ("How much does a cubic yard of gravel weigh?", "Roughly 1.4 tons for 3/4-inch crushed stone, though it varies by stone type."),
        ("How deep should gravel be for a driveway?", "Four inches compacted for a light drive, six inches for regular vehicle traffic."),
        ("Can I put gravel directly on soil?", "Yes for paths, but lay landscape fabric first to stop the gravel sinking into the soil."),
        ("How many tons of gravel in a cubic yard?", "About 1.3 to 1.5 tons depending on the stone, with 1.4 tons a good default."),
    ],
    "paint": [
        ("How much does a gallon of paint cover?", "Around 350 square feet per coat on a smooth, primed surface."),
        ("Do I need to subtract windows and doors?", "Yes. Allow about 21 square feet per door and 15 square feet per window."),
        ("How many coats of paint do I need?", "Two coats for a colour change, and often two even when refreshing the same colour."),
        ("Should I buy extra paint?", "Keep about 10% spare for touch-ups, and note the colour code for future matching."),
    ],
    "tile": [
        ("How much extra tile should I buy?", "Add 10% for straight layouts and 15% for diagonal or patterned work."),
        ("How many tiles in a box?", "It varies by size; check the box coverage in square feet rather than counting tiles."),
        ("Do I need to account for grout lines?", "Yes for precise work, though the waste allowance usually covers the small difference."),
        ("Can I return leftover tile?", "Often yes if unopened and from the same batch, but dye lots differ, so buy all you need at once."),
    ],
    "grass_seed": [
        ("How much grass seed per 1000 square feet?", "About 4 to 5 pounds for a new lawn, and 2 pounds when overseeding an existing one."),
        ("What is the best time to sow grass seed?", "Early autumn, when the soil is warm and weeds are slowing down."),
        ("How long until grass seed grows?", "Seven to fourteen days for ryegrass, up to three weeks for bluegrass."),
        ("Should I cover grass seed with soil?", "A thin layer of compost or topsoil helps, but leave the seed near the surface so it can sprout."),
    ],
    "concrete": [
        ("How many bags of concrete make a cubic yard?", "About 45 bags of 80 lb mix, or 60 bags of 60 lb mix, per cubic yard."),
        ("How thick should a concrete slab be?", "Four inches for paths and patios, five to six inches for driveways and heavy loads."),
        ("How much water do I add to concrete mix?", "Follow the bag instructions; roughly 3 quarts per 80 lb bag, added gradually."),
        ("Can I pour concrete over soil?", "Yes if the ground is compacted and level, with a gravel base for drainage."),
    ],
}


def _meta_description(title: str, kw: str, calc_title: str) -> str:
    base = (f"Use our free {calc_title.lower()} to work out exactly what you need for "
            f"{kw}. Includes the formula, a worked example and common mistakes.")
    return base[:155].rsplit(" ", 1)[0] + "." if len(base) > 155 else base


SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of",
               "on", "or", "the", "to", "with"}


def _title_case(text: str) -> str:
    words = text.split()
    out = []
    for i, w in enumerate(words):
        low = w.lower()
        if i not in (0, len(words) - 1) and low in SMALL_WORDS:
            out.append(low)
        elif low in ("i", "sq", "ft"):
            out.append(w.upper())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return " ".join(out)


def _title_for(kw: str, calc_title: str) -> str:
    kw_title = _title_case(kw.strip())
    suffix = ": Free Calculator & Guide"
    if len(kw_title) + len(suffix) <= 60:
        return kw_title + suffix
    if len(kw_title) <= 60:
        return kw_title
    return kw_title[:57].rstrip() + "..."


def _fallback_body(kw: str, calc_title: str, calc_short: str, worked: str,
                   secondary: list[str], calc_key: str = "") -> str:
    import content_lib
    lib = content_lib.LIBRARY.get(calc_key, {})
    material_word = {
        "mulch": "mulch", "soil": "soil mix", "gravel": "gravel",
        "paint": "paint", "tile": "tile", "grass_seed": "grass seed",
        "concrete": "concrete mix",
    }.get(calc_key, "material")

    parts = [
        f"The quick answer: measure the area, multiply by the required depth, then convert "
        f"to the units you buy in. Our {calc_title.lower()} below does it for you and shows "
        f"every step, so you can check the maths and order with confidence.\n",
        f"## How to Calculate {calc_short.title()}\n",
        "1. Measure the length and width in feet and multiply them to get the area.\n"
        "2. Decide the depth (or thickness) the job needs, in inches.\n"
        "3. Convert depth to feet by dividing by 12.\n"
        "4. Multiply area by depth in feet to get cubic feet.\n"
        "5. Divide cubic feet by 27 to get cubic yards, or use the bag figures below.\n",
        f"## Worked Example\n\n{worked}\n",
        f"This example uses the calculator's default values, so you can see the whole "
        f"calculation laid out before you change anything.\n",
    ]

    if lib.get("depths"):
        parts.append(f"## How Deep Should {material_word.title()} Be?\n")
        parts.append(content_lib.depth_table_md(calc_key) + "\n")
        parts.append("Pick the depth that matches the job rather than the deepest option "
                     "available. Too shallow and the job fails early; too deep and you "
                     "waste money on material you did not need.\n")

    size_table = content_lib.size_table_md(calc_key)
    if size_table:
        parts.append("## How Much You Need at Common Sizes\n")
        parts.append(size_table + "\n")
        parts.append("Use the calculator above for your exact measurements; the table is "
                     "here so you can sanity-check the result at a glance.\n")

    if lib.get("materials"):
        parts.append(f"## Which Type of {material_word.title()} to Choose\n")
        parts.append(content_lib.materials_md(calc_key) + "\n")
        parts.append("Match the product to the job rather than to the lowest price. Check "
                     "the supplier's stated coverage too, because it varies between brands "
                     "and is usually given per bag or per cubic yard.\n")

    parts.append("## Common Mistakes to Avoid\n")
    for m in [
        "Estimating by eye instead of measuring the actual area.",
        "Forgetting the depth or thickness requirement for the job.",
        "Skipping the waste allowance, then running short mid-project.",
        "Mixing bags from different batches, which can show as shade differences.",
        "Buying the cheapest option that does not suit the application.",
    ]:
        parts.append(f"- {m}\n")

    parts.append("\n## Measuring Your Area Accurately\n")
    parts.append(
        "Most errors come from the measurement, not the arithmetic. Measure at the widest "
        "and narrowest points and use the average, because beds and rooms are rarely "
        "perfect rectangles. For an L-shaped area, split it into two rectangles, work out "
        "each one, and add the results. For a circular bed, measure the diameter, halve it "
        "to get the radius, then multiply the radius by itself and by 3.14. Write the "
        "figures down in feet before you start, so you are not converting units in your "
        "head while you work.\n")

    parts.append("## Converting Between Units\n")
    parts.append(
        "Suppliers sell in different units, so it helps to know how they relate. There are "
        "27 cubic feet in a cubic yard, so divide cubic feet by 27 to get cubic yards. To "
        "go the other way, multiply cubic yards by 27. Bagged products state their volume "
        "on the label, usually 1.5 or 2 cubic feet for soil and mulch, so divide your total "
        "cubic feet by the bag size and round up to the next whole bag. For stone and "
        "aggregate sold by weight, a cubic yard of typical 3/4 inch crushed stone weighs "
        "about 1.4 tons, though this varies with the material.\n")

    parts.append("## Ordering: Bags or Bulk\n")
    parts.append(
        "For small jobs, bagged product is simpler and you can carry it yourself. As the "
        "volume grows, bulk delivery usually works out cheaper per unit, but check whether "
        "the supplier charges a delivery fee and whether they will place it where you need "
        "it. Order in one go where you can, so the material comes from the same batch, and "
        "add a small margin for settling and waste. If you are close to a whole cubic yard, "
        "it often makes sense to round up rather than make a second trip.\n")

    if lib.get("tips"):
        parts.append("\n## Practical Tips\n")
        for t in lib["tips"]:
            parts.append(f"- {t}\n")

    if lib.get("tools"):
        parts.append("\n## Tools and Materials You Will Need\n")
        parts.append(f"For this job, have to hand {lib['tools']}. None of it is specialist; "
                     f"the only item worth hiring is a compactor for a gravel driveway, since "
                     f"hand tamping rarely gets the base firm enough.\n")

    parts.append("## When to Call a Professional\n")
    parts.append(
        "Measuring and ordering are straightforward for most garden and decorating jobs, but "
        "a few situations are worth handing over. Structural work, retaining walls over about "
        "two feet, anything affecting drainage around a building, and electrical or gas work "
        "should go to a qualified tradesperson. The same applies if the ground is unstable or "
        "you are unsure about the base preparation for a driveway or slab: a professional "
        "survey costs far less than a failed pour or a wall that moves.\n")

    if secondary:
        parts.append(
            f"\n## Related Questions\n\nPeople also ask about "
            f"{', '.join(secondary[:3])}. The method is the same in every case: measure the "
            f"area, choose the depth that suits the job, then convert the result into the "
            f"units your supplier sells in.\n")

    return "\n".join(parts)


def generate_article(plan_item: dict) -> dict | None:
    cfg = topics_config()
    seo = seo_config()
    calc_key = plan_item.get("calculator") or ""
    calc_def = cfg.get("calculators", {}).get(calc_key)
    if not calc_def:
        print(f"[generate] no calculator for cluster {plan_item.get('cluster')}")
        return None

    kw = plan_item["primary_keyword"]
    slug = plan_item["slug"]
    calc_title = calc_def["title"]
    calc_short = calc_key.replace("_", " ")

    defaults = {i["id"]: i["default"] for i in calc_def["inputs"]}
    result = calculators.compute(calc_key, defaults)
    worked = calculators.worked_example(calc_key, defaults)

    kws = load_json(DATA / "keywords.json", default=[])
    secondary = [k["keyword"] for k in kws
                 if k.get("cluster") == plan_item.get("cluster") and k["keyword"] != kw][:5]

    body = None
    if llm.available():
        import content_lib
        prompt = OUTLINE_PROMPT.format(
            kw=kw, cluster=plan_item.get("cluster", ""), secondary=", ".join(secondary),
            calc_title=calc_title, calc_short=calc_short.title(), worked=worked,
            facts=content_lib.facts_block(calc_key),
            size_table=content_lib.size_table_md(calc_key))
        body = llm.generate(prompt, system=SYSTEM, max_tokens=4096)
        if body:
            print(f"[generate] LLM draft for {slug}: {word_count(body)} words")
    if not body:
        body = _fallback_body(kw, calc_title, calc_short, worked, secondary, calc_key)
        print(f"[generate] template draft for {slug}: {word_count(body)} words")

    title = _title_for(kw, calc_title)
    faqs = FAQ_TEMPLATES.get(calc_key, [])
    today = dt.date.today().isoformat()
    return {
        "id": slug,
        "slug": slug,
        "title": title,
        "cluster": plan_item.get("cluster", ""),
        "primary_keyword": kw,
        "secondary_keywords": secondary,
        "intent": "calculator",
        "is_pillar": bool(plan_item.get("is_pillar")),
        "calculator": calc_key,
        "calculator_title": calc_title,
        "calculator_defaults": defaults,
        "calculator_output": result,
        "meta_description": _meta_description(title, kw, calc_title),
        "body_markdown": body,
        "faq": [{"q": q, "a": a} for q, a in faqs],
        "status": "draft",
        "created": today,
        "updated": today,
        "revision": 1,
        "internal_links": [],
        "schema_types": seo.get("default_schema", []) + (["FAQPage"] if faqs else []),
        "quality": {},
        "metrics": {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0},
        "word_count": word_count(body),
    }


def run(limit: int = 1) -> list[dict]:
    import cluster
    plans = cluster.plan(limit=limit)
    arts = load_json(DATA / "articles.json", default=[])
    existing = {a["slug"] for a in arts}
    created = []
    for p in plans:
        if p["slug"] in existing:
            continue
        art = generate_article(p)
        if art:
            arts.append(art)
            created.append(art)
            existing.add(art["slug"])
    save_json(DATA / "articles.json", arts)
    print(f"[generate] created {len(created)} articles")
    return created


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run(limit=n)
