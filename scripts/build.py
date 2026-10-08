"""Static site build. Reads data/articles.json + config, writes site/."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

import charts
import images
import mdrender
import merges
import planners
import seasonal
import seo as seolib
import calculators
from common import (CONFIG, CONTENT, DATA, SITE, STATIC, TEMPLATES, human_date,
                    load_json, save_json, seo_config, site_config, topics_config)

YEAR = dt.date.today().year

# Cross-cluster "next step" links: after the primary job, these are the usual follow-ups.
# Links between calculator pillars spread crawl equity and match how a real project flows.
PROJECT_NEXT_STEPS = {
    "mulch": ["soil", "topsoil", "fertilizer"],
    "soil": ["mulch", "topsoil", "gravel"],
    "topsoil": ["grass-seed", "soil", "fertilizer"],
    "gravel": ["concrete", "soil", "mulch"],
    "concrete": ["gravel", "paint", "tile"],
    "paint": ["tile", "concrete", "gravel"],
    "tile": ["paint", "concrete", "gravel"],
    "grass-seed": ["topsoil", "fertilizer", "soil"],
    "fertilizer": ["grass-seed", "topsoil", "soil"],
}

# Extra indexable site pages, appended to the sitemap with a real lastmod.
EXTRA_PAGES = ["/calculators/", "/guides/", "/sitemap/", "/for-publishers/"]
# Inline SVG icon id for each project category (symbols live in base.html).
CATEGORY_ICONS = {
    "mulch": "mulch", "soil": "soil", "gravel": "gravel", "paint": "paint",
    "tile": "tile", "grass-seed": "seed", "concrete": "concrete",
    "topsoil": "topsoil", "fertilizer": "fertilizer",
}
BLURBS = {
    "mulch": "Work out bags or cubic yards of mulch for any bed size and depth.",
    "soil": "Fill raised beds with the right amount of soil mix.",
    "gravel": "Calculate cubic yards and tons of gravel for paths and drives.",
    "paint": "Estimate gallons of paint per room, coats and openings.",
    "tile": "Count tiles and waste allowance for floors and walls.",
    "grass-seed": "Seed a new lawn or overseed an existing one at the right rate.",
    "concrete": "Get cubic yards and bag counts for slabs and footings.",
    "topsoil": "Estimate cubic yards or bags of topsoil to fill or level any area.",
    "fertilizer": "Find pounds and bags of fertilizer for your lawn at the right rate.",
}
# What the figure shows, per category — used for the caption and image alt text.
FIG_CAPTION = {
    "mulch": "Cross-section of a mulched bed: area x depth gives the volume to order.",
    "soil": "Cross-section of a raised bed being filled to its working height.",
    "topsoil": "Cross-section of an area being levelled with topsoil.",
    "gravel": "Cross-section of a gravel layer at the chosen depth.",
    "concrete": "Cross-section of a concrete slab at the chosen thickness.",
    "paint": "How the number of coats multiplies the paint you need.",
    "grass-seed": "Sowing rates per 1,000 sq ft for new lawns and overseeding.",
    "fertilizer": "Application rates per 1,000 sq ft at light, standard and heavy doses.",
    "tile": "Tile layout showing the waste allowance added for cuts and breakage.",
}

# Homepage quick calculator: a compact version of the most common tools. Each tab shows
# only the 2-3 inputs that drive the headline result; the engine (static/js/main.js) is
# the same code the full calculator pages use, so the numbers can never disagree.
QUICK_CALCS = [
    {"key": "mulch", "label": "Mulch", "icon": "mulch", "slug": "mulch-calculator",
     "inputs": ["length", "width", "depth"],
     "presets": [{"label": "4x8 bed, 3 in", "v": {"length": 8, "width": 4, "depth": 3}},
                 {"label": "500 sq ft, 3 in", "v": {"length": 25, "width": 20, "depth": 3}}]},
    {"key": "soil", "label": "Soil", "icon": "soil", "slug": "raised-bed-soil-calculator",
     "inputs": ["length", "width", "height"],
     "presets": [{"label": "4x8 bed, 12 in", "v": {"length": 8, "width": 4, "height": 12}},
                 {"label": "4x4 bed, 6 in", "v": {"length": 4, "width": 4, "height": 6}}]},
    {"key": "gravel", "label": "Gravel", "icon": "gravel", "slug": "gravel-calculator",
     "inputs": ["length", "width", "depth"],
     "presets": [{"label": "10x10 patio, 3 in", "v": {"length": 10, "width": 10, "depth": 3}},
                 {"label": "Driveway 20x10, 4 in", "v": {"length": 20, "width": 10, "depth": 4}}]},
    {"key": "concrete", "label": "Concrete", "icon": "concrete", "slug": "concrete-calculator",
     "inputs": ["length", "width", "thickness"],
     "presets": [{"label": "10x12 slab, 4 in", "v": {"length": 12, "width": 10, "thickness": 4}},
                 {"label": "10x10 slab, 4 in", "v": {"length": 10, "width": 10, "thickness": 4}}]},
    {"key": "paint", "label": "Paint", "icon": "paint", "slug": "paint-calculator",
     "inputs": ["length", "width", "height", "coats"],
     "units": {"height": "ft"},
     "presets": [{"label": "12x10 room, 2 coats", "v": {"length": 12, "width": 10, "height": 8, "coats": 2}}]},
    {"key": "tile", "label": "Tile", "icon": "tile", "slug": "tile-calculator",
     "inputs": ["length", "width", "tile_w", "tile_h", "waste"],
     "presets": [{"label": "10x10, 12 in tiles", "v": {"length": 10, "width": 10, "tile_w": 12, "tile_h": 12, "waste": 10}}]},
    {"key": "grass_seed", "label": "Grass seed", "icon": "seed", "slug": "grass-seed-calculator",
     "inputs": ["area", "method"],
     "presets": [{"label": "5,000 sq ft new lawn", "v": {"area": 5000, "method": 1}}]},
    {"key": "fertilizer", "label": "Fertilizer", "icon": "fertilizer", "slug": "fertilizer-calculator",
     "inputs": ["area", "rate", "bag"],
     "presets": [{"label": "5,000 sq ft, 1 lb N", "v": {"area": 5000, "rate": 1, "bag": 40}}]},
]
# Short unit suffixes so the compact inputs stay readable on a 360 px screen.
QUICK_UNITS = {"length": "ft", "width": "ft", "depth": "in", "height": "in",
               "thickness": "in", "tile_w": "in", "tile_h": "in", "waste": "%",
               "area": "sq ft", "rate": "lb", "bag": "lb", "coats": "", "method": ""}

# "Popular quick answers": real numbers computed at build time from scripts/calculators.py
# (the same engine the pages use), each linking to the calculator that produced it. The
# answer text is derived from the function output, never typed by hand.
QUICK_ANSWERS = [
    {"calc": "concrete", "args": {"length": 12, "width": 10, "thickness": 4},
     "q": "10x12 ft slab, 4 in thick",
     "answer": lambda o: f"{o['cubic_yards']} cubic yards — about {o['bags_80lb']} bags of 80 lb or {o['bags_60lb']} bags of 60 lb"},
    {"calc": "mulch", "args": {"length": 25, "width": 20, "depth": 3},
     "q": "500 sq ft bed, 3 in deep",
     "answer": lambda o: f"{o['cubic_yards']} cubic yards — about {o['bags_2cf']} bags of 2 cu ft"},
    {"calc": "soil", "args": {"length": 8, "width": 4, "height": 12},
     "q": "4x8 ft raised bed, 12 in deep",
     "answer": lambda o: f"{o['cubic_feet']} cubic feet — about {o['bags_1_5cf']} bags of 1.5 cu ft"},
    {"calc": "gravel", "args": {"length": 10, "width": 10, "depth": 3},
     "q": "10x10 ft patio, 3 in deep",
     "answer": lambda o: f"{o['cubic_yards']} cubic yards, roughly {o['tons']} tons"},
    {"calc": "paint", "args": {"length": 12, "width": 10, "height": 8, "coats": 2},
     "q": "12x10 ft room, 2 coats",
     "answer": lambda o: f"about {o['gallons']} gallons"},
    {"calc": "tile", "args": {"length": 10, "width": 10, "tile_w": 12, "tile_h": 12, "waste": 10},
     "q": "10x10 ft floor, 12 in tiles",
     "answer": lambda o: f"{o['tiles']} tiles, or {o['tiles_with_waste']} with 10% waste"},
    {"calc": "grass_seed", "args": {"area": 5000, "method": 1},
     "q": "5,000 sq ft new lawn",
     "answer": lambda o: f"{o['pounds']} lb of seed — about {o['bags_3lb']} bags of 3 lb"},
    {"calc": "fertilizer", "args": {"area": 5000, "rate": 1, "bag": 40},
     "q": "5,000 sq ft lawn at 1 lb N",
     "answer": lambda o: f"{o['pounds']} lb — about {o['bags']} bag of 40 lb"},
]

# Homepage FAQ. These exact questions and answers are rendered visibly in accordions AND
# emitted as FAQPage schema, so the markup always matches what a visitor can read.
HOME_FAQS = [
    {"q": "How do I work out how much mulch I need?",
     "a": "Multiply the bed's length by its width to get square feet, multiply by the depth in "
          "feet, then divide by 27 for cubic yards. A 500 sq ft bed at 3 in deep needs about "
          "4.63 cubic yards, or 63 bags of 2 cu ft."},
    {"q": "How many bags of concrete do I need for a 10x12 slab?",
     "a": "A 10x12 ft slab at 4 in thick needs about 1.48 cubic yards: roughly 67 bags of 80 lb "
          "mix or 89 bags of 60 lb mix."},
    {"q": "How much area does a cubic yard cover?",
     "a": "One cubic yard is 27 cubic feet. Spread 3 in deep it covers about 108 sq ft; at 2 in "
          "deep it covers about 162 sq ft."},
    {"q": "How much paint do I need for a room?",
     "a": "Measure the wall area, subtract the doors and windows, divide by about 350 sq ft per "
          "gallon, then multiply by the number of coats."},
    {"q": "Are the calculator results accurate enough to order materials?",
     "a": "The formulas are the standard rules of thumb suppliers publish, but every result is "
          "an estimate. Round up and confirm the coverage on the bag or with your supplier "
          "before ordering."},
    {"q": "Is GardenCalc free to use and embed?",
     "a": "Yes. Every calculator is free, needs no sign-up, and can be embedded on your own site "
          "with the credit link kept intact."},
]

# Short, factual FAQ per category hub (2 items each) — answers reuse the standard rates the
# calculators already use, so the FAQPage schema matches visible text exactly.
CATEGORY_FAQS = {
    "mulch": [
        {"q": "How deep should mulch be?",
         "a": "Most beds are mulched 2 to 3 inches deep. Deeper than 4 inches can smother roots "
              "and hold too much moisture, so 3 inches is a safe default."},
        {"q": "How many bags of mulch is a cubic yard?",
         "a": "A cubic yard is 27 cubic feet, so it equals about 13.5 bags of 2 cubic feet."},
    ],
    "soil": [
        {"q": "How much soil does a raised bed need?",
         "a": "Multiply the bed length by width by the fill depth in feet to get cubic feet, then "
              "divide by 27 for cubic yards. A 4x8 bed filled 12 inches deep needs 32 cubic feet."},
        {"q": "Should I fill a raised bed with topsoil or a mix?",
         "a": "A blend of topsoil and compost is usual. The calculator gives the total volume; use "
              "the depth your plants need rather than filling to the very top."},
    ],
    "gravel": [
        {"q": "How much does a cubic yard of gravel weigh?",
         "a": "Gravel is about 1.2 to 1.5 tons per cubic yard depending on the stone, so the "
              "calculator uses 1.4 tons per cubic yard as a working figure."},
        {"q": "How deep should gravel be for a driveway?",
         "a": "A working driveway usually has 4 inches of gravel over a compacted base. Paths and "
              "decorative beds often use 2 to 3 inches."},
    ],
    "paint": [
        {"q": "How many square feet does a gallon of paint cover?",
         "a": "About 350 square feet per gallon for a single coat on a smooth, sealed wall. Rough "
              "or porous surfaces can use more."},
        {"q": "Do I need to subtract doors and windows?",
         "a": "Yes. Deducting a door (about 21 square feet) and a window (about 15 square feet) "
              "keeps the estimate realistic."},
    ],
    "tile": [
        {"q": "How much waste should I allow for tile?",
         "a": "Add 10 percent for a straight lay and 15 to 20 percent for diagonal or patterned "
              "layouts, to cover cuts and breakage."},
        {"q": "How do I work out how many tiles I need?",
         "a": "Divide the floor area by the area of one tile, then round up and add the waste "
              "allowance. The calculator does both steps for you."},
    ],
    "grass-seed": [
        {"q": "How much grass seed do I need per 1,000 square feet?",
         "a": "A new lawn uses about 4.5 pounds per 1,000 square feet; overseeding an existing lawn "
              "uses about 2 pounds per 1,000 square feet."},
        {"q": "When is the best time to sow grass seed?",
         "a": "Late summer to early autumn suits cool-season grasses, giving the seed warm soil and "
              "cool, damp air. Spring works too if you keep it watered."},
    ],
    "concrete": [
        {"q": "How many bags of concrete make a cubic yard?",
         "a": "About 45 bags of 80 lb mix or 60 bags of 60 lb mix make a cubic yard, depending on "
              "the yield printed on the bag."},
        {"q": "How thick should a concrete slab be?",
         "a": "A garden path or shed base is usually 4 inches thick. Driveways and heavier loads "
              "often use 5 to 6 inches over a compacted base."},
    ],
    "topsoil": [
        {"q": "How much topsoil do I need to level a lawn?",
         "a": "Multiply the area by the depth in feet to get cubic feet, then divide by 27 for "
              "cubic yards. Spread thinly and settle it rather than smothering the grass."},
        {"q": "Is topsoil sold by the bag or the yard?",
         "a": "Both. Small jobs use 40 lb bags; larger jobs are cheaper by the cubic yard. The "
              "calculator shows the bag and cubic-yard totals side by side."},
    ],
    "fertilizer": [
        {"q": "How much fertilizer do I put on my lawn?",
         "a": "A common rate is 1 pound of actual nitrogen per 1,000 square feet per feeding. Check "
              "the nitrogen number on the bag to convert that to product."},
        {"q": "How do I convert a nitrogen rate to bags?",
         "a": "Divide the pounds of nitrogen by the nitrogen share on the bag label, then divide by "
              "the bag weight. The calculator does this from your area and bag size."},
    ],
}


def _env() -> Environment:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)),
                      autoescape=select_autoescape(["html", "xml"]))
    # Display dates as "Oct 8, 2026" while <time datetime> keeps the ISO value.
    env.filters["date_human"] = human_date
    return env


def _base(site: dict) -> str:
    return (site.get("custom_domain") or site["base_url"]).rstrip("/")


def _abs(site: dict, path: str) -> str:
    return _base(site) + "/" + path.lstrip("/")


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _contact_block(site: dict) -> str:
    """Honest contact route: a real email if configured, otherwise the repo issues page."""
    email = site.get("contact_email", "").strip()
    if email and "example.com" not in email:
        return f"Email us at **{email}** and we will reply within a few working days."
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if repo:
        return (f"The fastest way to reach us is to open an issue on the project's "
                f"[GitHub repository](https://github.com/{repo}/issues). We reply within "
                f"a few working days.")
    return ("Contact details will be published here shortly. In the meantime, please use "
            "the repository's issue tracker if you found this project through GitHub.")


def _reading_time(words: int) -> int:
    return max(1, round(words / 220))


def _thumb(site: dict, art: dict) -> str:
    """Article thumbnail URL (theme figure), with a CSS fallback if images were skipped."""
    return _abs(site, f"/static/img/thumb/{art['slug']}.webp")


def _fig(site: dict, art: dict) -> str:
    return _abs(site, f"/static/img/fig/{art['slug']}.webp")


def _short_desc(text: str, limit: int = 120) -> str:
    """Trim a meta description to a card length at a word boundary, with an ellipsis."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return cut + "…"


def _one_sentence(text: str) -> str:
    """First complete sentence of a meta description, for card excerpts.

    Falls back to the whole text when the first sentence is too short to stand alone, so
    an excerpt never ends on a dangling fragment.
    """
    text = (text or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    if m and len(m.group(1)) >= 60:
        return m.group(1)
    return _short_desc(text)


def _card_meta(site: dict, art: dict, category: str | None = None) -> dict:
    return {
        "slug": art["slug"],
        "title": art["title"],
        "desc": _short_desc(art.get("meta_description", "")),
        "excerpt": _one_sentence(art.get("meta_description", "")),
        "thumb": _thumb(site, art),
        "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        "category": category or "",
        "updated": art.get("updated", ""),
        "updated_human": human_date(art.get("updated", "")),
    }


def _split_first_section(body_html: str) -> tuple[str, str]:
    """Split rendered article HTML after the first <h2> section.

    Lets guide pages drop the "open the calculator" card right after the opening
    section, where readers have just read the answer and are ready to use the tool.
    """
    idx = body_html.find("<h2 ")
    if idx <= 0:
        return body_html, ""
    end = body_html.find("<h2 ", idx + 1)
    if end == -1:
        return body_html, ""
    return body_html[:end], body_html[end:]


def _calc_context(art: dict, cfg: dict, site: dict) -> dict | None:
    calc_key = art.get("calculator")
    defs = cfg.get("calculators", {}).get(calc_key)
    if not defs:
        return None
    inputs = []
    defaults = {}
    for inp in defs.get("inputs", []):
        d = dict(inp)
        d.setdefault("step", "0.1")
        inputs.append(d)
        defaults[d["id"]] = d.get("default")
    presets = next((q.get("presets", []) for q in QUICK_CALCS if q["key"] == calc_key), [])
    return {
        "key": calc_key,
        "title": art.get("calculator_title") or defs.get("title", "Calculator"),
        "sub": "Change any value and the answer updates instantly. Nothing is sent anywhere — it runs in your browser.",
        "hint": "Estimates only. Round up when ordering and check with your supplier.",
        "inputs": inputs,
        "defaults": defaults,
        "presets": presets,
        "slug": art["slug"],
        # Set data/videos.json as {"mulch": {"id": "...", "upload": "YYYY-MM-DD"}} to
        # publish a walkthrough; empty renders nothing (no fake videos, no empty player).
        "video": (load_json(DATA / "videos.json", default={}) or {}).get(calc_key, {}),
    }


def build() -> dict:
    site = site_config()
    tcfg = topics_config()
    arts = load_json(DATA / "articles.json", default=[])
    published = [a for a in arts
                 if a.get("status") in ("published", "approved")
                 and a.get("quality", {}).get("passed")]
    published.sort(key=lambda a: a.get("created", ""), reverse=True)

    # Merged URLs stay alive as redirect stubs (Phase 2) but must not appear in
    # listings, the sitemap, RSS, feeds or the internal link graph.
    merged_slugs = merges.merged_slugs()
    live = [a for a in published if a["slug"] not in merged_slugs]
    for a in live:
        a.setdefault("internal_links", [])
        a["internal_links"] = [l for l in a["internal_links"]
                               if l.get("to") not in merged_slugs]
    published = live

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    base = _base(site)
    categories = tcfg.get("clusters", [])
    for c in categories:
        c["blurb"] = BLURBS.get(c["id"], "Free calculators and practical guides.")
        c["icon"] = CATEGORY_ICONS.get(c["id"], "leaf")
    cat_map = {c["id"]: c for c in categories}
    nav_categories = [{"id": c["id"], "name": c["name"], "icon": c["icon"],
                       "blurb": c["blurb"]} for c in categories]
    # Top calculators for the footer's "Popular calculators" column, in the same order the
    # homepage shows them so the two never drift apart.
    popular_calcs = [{"slug": a["slug"], "title": a.get("calculator_title") or a["title"]}
                     for a in published if a.get("is_pillar")][:6]

    env = _env()
    env.globals.update(base_url=base, site=site, year=YEAR,
                       nav_categories=nav_categories, popular_calcs=popular_calcs,
                       calc_defs=tcfg.get("calculators", {}))

    default_og = _abs(site, "/static/img/og-default.png")
    # Social scrapers handle PNG far more reliably than WebP, so the OG card always
    # points at a PNG. Page figures are WebP; swap them for their PNG twin.
    default_og_png = default_og.rsplit(".", 1)[0] + ".png"

    def _og(url: str) -> str:
        return default_og_png if url.endswith((".webp", ".svg")) else url

    # Cache-busting token for the CSS/JS bundle: a short hash of the source files, so a
    # redeploy always serves fresh assets to returning visitors. Safe to change every run.
    import hashlib
    _asset_src = (STATIC / "css" / "style.css").read_bytes() + (STATIC / "js" / "main.js").read_bytes()
    asset_v = hashlib.sha1(_asset_src).hexdigest()[:8]

    def common(title, description, canonical, og_type="website", og_image=None,
               schemas=None, robots=None, keywords=None):
        return dict(title=title, description=description, canonical=canonical,
                    og_type=og_type, og_image=_og(og_image or default_og),
                    schemas=schemas or [],
                    robots=robots or "index, follow, max-snippet:-1, max-image-preview:large",
                    keywords=keywords, base_url=base, asset_v=asset_v)

    # Index for prev/next within each cluster, ordered by creation date.
    by_cluster: dict[str, list[dict]] = {}
    for a in sorted(published, key=lambda x: x.get("created", "")):
        by_cluster.setdefault(a.get("cluster", ""), []).append(a)
    order_index = {a["slug"]: i for lst in by_cluster.values() for i, a in enumerate(lst)}
    pillar_by_cluster = {a.get("cluster"): a for a in published if a.get("is_pillar")}
    chart_cards = [{"slug": ch["slug"], "title": ch["title"], "description": ch["description"],
                    "cluster_name": cat_map.get(ch["cluster"], {}).get("name", ch["cluster"].title())}
                   for ch in charts.CHARTS]
    planner_cards = [{"slug": pl["slug"], "title": pl["title"], "description": pl["description"],
                      "cluster_name": cat_map.get(pl["cluster"], {}).get("name", pl["cluster"].title())}
                     for pl in planners.PLANNERS]
    seasonal_cards = [{"slug": it["slug"], "title": it["title"], "description": it["description"],
                       "cluster_name": cat_map.get(it["cluster"], {}).get("name", it["cluster"].title())}
                      for it in seasonal.SEASONAL]
    chart_by_cluster = {ch["cluster"]: {"slug": ch["slug"], "title": ch["title"]} for ch in charts.CHARTS}
    planner_by_cluster = {pl["cluster"]: {"slug": pl["slug"], "title": pl["title"]} for pl in planners.PLANNERS}
    seasonal_by_cluster = {it["cluster"]: {"slug": it["slug"], "title": it["title"]} for it in seasonal.SEASONAL}

    # --- articles ---
    for art in published:
        body_html, toc = mdrender.render_with_toc(art.get("body_markdown", ""),
                                                  {x["slug"]: f"{base}/{x['slug']}/" for x in published})
        figure = {
            "src": _fig(site, art),
            "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
            "caption": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        }
        ct = cat_map.get(art.get("cluster", ""), {})
        category_name = ct.get("name", "Guides")

        # Related: sibling articles in the same cluster, excluding self.
        cl = by_cluster.get(art.get("cluster", ""), [])
        sib = [a for a in cl if a["slug"] != art["slug"]]
        pos = next((i for i, a in enumerate(cl) if a["slug"] == art["slug"]), 0)
        prev_art = cl[pos - 1] if pos > 0 else None
        next_art = cl[pos + 1] if pos + 1 < len(cl) else None
        related = [_card_meta(site, a, category_name) for a in sib[:3]]

        # Link the article to its own coverage chart and project planner (where they exist)
        # so crawl equity flows both ways and readers find the printable/reference view.
        cluster_chart = chart_by_cluster.get(art.get("cluster", ""))
        cluster_planner = planner_by_cluster.get(art.get("cluster", ""))
        cluster_seasonal = seasonal_by_cluster.get(art.get("cluster", ""))

        # "Plan the whole project": link to the pillar calculator of the usual follow-up
        # clusters, so crawl equity moves between categories and users find the next step.
        project_links = []
        for cid in PROJECT_NEXT_STEPS.get(art.get("cluster", ""), []):
            p = pillar_by_cluster.get(cid)
            if p and p["slug"] != art["slug"]:
                project_links.append({"slug": p["slug"], "title": p["title"],
                                      "desc": p.get("meta_description", "")[:90]})

        # Answer-first block (featured-snippet bait): the first FAQ answer is a direct,
        # numeric answer to the page's main question.
        faq_items = art.get("faq") or []
        answer_first = faq_items[0]["a"] if faq_items else art.get("meta_description", "")

        schemas = [json.dumps(s, ensure_ascii=False) for s in
                   seolib.all_schema(art, site, figure=_fig(site, art))]
        calc_ctx = _calc_context(art, tcfg, site)
        if calc_ctx:
            schemas.append(json.dumps(seolib.webapp_schema(
                calc_ctx["title"], _abs(site, f"/{art['slug']}/"),
                art.get("meta_description", ""), site), ensure_ascii=False))
            vid = calc_ctx.get("video") or {}
            if vid.get("id"):
                v = seolib.video_schema(calc_ctx["title"], vid["id"],
                                        _abs(site, f"/{art['slug']}/"),
                                        art.get("meta_description", ""))
                v["uploadDate"] = vid.get("upload", art.get("updated", ""))
                schemas.append(json.dumps(v, ensure_ascii=False))
        ctx = common(title=art["title"], description=art["meta_description"],
                     canonical=_abs(site, f"/{art['slug']}/"), og_type="article",
                     og_image=_fig(site, art), schemas=schemas,
                     keywords=", ".join([art.get("primary_keyword", "")] +
                                        art.get("secondary_keywords", [])))
        body_head, body_rest = _split_first_section(body_html)
        ctx.update(article=art, body_html=body_html, body_head=body_head, body_rest=body_rest,
                   toc=toc, figure=figure,
                   calc=calc_ctx, faq=faq_items, answer_first=answer_first,
                   category_name=category_name, reading_time=_reading_time(art.get("word_count", 0)),
                   related=related, project_links=project_links,
                   # Guide pages get a compact link back to their category's calculator.
                   calc_link=(_card_meta(site, pillar_by_cluster[art["cluster"]], category_name)
                              if not art.get("is_pillar")
                              and art.get("cluster") in pillar_by_cluster else None),
                   cluster_chart=cluster_chart, cluster_planner=cluster_planner,
                   cluster_seasonal=cluster_seasonal,
                   pager={"prev": {"slug": prev_art["slug"], "title": prev_art["title"]} if prev_art else None,
                          "next": {"slug": next_art["slug"], "title": next_art["title"]} if next_art else None})
        _write(SITE / art["slug"] / "index.html",
               env.get_template("article.html").render(**ctx))

    # --- categories ---
    for c in categories:
        items = [a for a in published if a.get("cluster") == c["id"]]
        pillars = [a for a in items if a.get("is_pillar")]
        others = [a for a in items if not a.get("is_pillar")]
        og = _abs(site, "/static/img/og-default.png")  # brand card for category hubs
        cat_faqs = CATEGORY_FAQS.get(c["id"], [])
        schemas = [json.dumps(seolib.collection_schema(c, items, site), ensure_ascii=False)]
        if cat_faqs:
            schemas.append(json.dumps(seolib.faq_schema({"faq": cat_faqs}), ensure_ascii=False))
        ctx = common(title=f"{c['name']} Calculators | {site['name']}",
                     description=(c["blurb"] + " Free, instant calculators with the formula shown.")[:155],
                     canonical=_abs(site, f"/category/{c['id']}/"), og_image=og,
                     schemas=schemas)
        ctx.update(category=c,
                   pillars=[_card_meta(site, a, c["name"]) for a in pillars],
                   others=[_card_meta(site, a, c["name"]) for a in others],
                   cat_faqs=cat_faqs)
        _write(SITE / "category" / c["id"] / "index.html",
               env.get_template("category.html").render(**ctx))

    # --- homepage ---
    pillars = [a for a in published if a.get("is_pillar")][:8]
    by_slug = {a["slug"]: a for a in published}
    calc_defs_all = tcfg.get("calculators", {})
    quick_calcs = []
    for qc in QUICK_CALCS:
        cdef = calc_defs_all.get(qc["key"], {})
        defs = {i["id"]: i for i in cdef.get("inputs", [])}
        inputs = []
        for iid in qc["inputs"]:
            if iid not in defs:
                continue
            d = defs[iid]
            inputs.append({
                "id": iid,
                "label": d.get("label", iid).split(" (")[0],
                "min": d.get("min"), "max": d.get("max"),
                "step": d.get("step", "0.1"),
                "default": d.get("default"),
                "unit": qc.get("units", {}).get(iid, QUICK_UNITS.get(iid, "")),
                "options": d.get("options"),
            })
        art = by_slug.get(qc["slug"])
        quick_calcs.append({
            "key": qc["key"], "label": qc["label"], "icon": qc["icon"],
            "title": cdef.get("title", qc["label"]),
            "slug": qc["slug"],
            "url": _abs(site, f"/{qc['slug']}/") if art else "",
            "inputs": inputs,
            "presets": qc.get("presets", []),
        })
    ctx = common(title=f"{site['name']} — Free Home & Garden Calculators",
                 description=("Free mulch, soil, topsoil, gravel, fertilizer, paint, tile, seed and "
                              "concrete calculators. Instant answers with the formula shown."),
                 canonical=_abs(site, "/"),
                 schemas=[json.dumps(seolib.website_schema(site), ensure_ascii=False),
                          json.dumps(seolib.organization_schema(site), ensure_ascii=False),
                          json.dumps(seolib.faq_schema({"faq": HOME_FAQS}), ensure_ascii=False)])
    quick_answer_items = []
    for qa in QUICK_ANSWERS:
        try:
            out = calculators.compute(qa["calc"], qa["args"])
        except Exception:
            continue
        art = by_slug.get(f"{qa['calc'].replace('_', '-')}-calculator")
        quick_answer_items.append({
            "q": qa["q"], "answer": qa["answer"](out),
            "url": _abs(site, f"/{art['slug']}/") if art else "",
            "label": calc_defs_all.get(qa["calc"], {}).get("title", qa["calc"].replace("_", " ").title()),
        })
    ctx.update(categories=categories, articles=published[:12],
               article_count=len(published), category_count=len(categories),
               chart_count=len(charts.CHARTS), chart_cards=chart_cards,
               planner_cards=planner_cards, seasonal_cards=seasonal_cards,
               quick_calcs=quick_calcs, quick_answers=quick_answer_items,
               home_faqs=HOME_FAQS,
               latest_cards=[_card_meta(site, a, cat_map.get(a.get("cluster", ""), {}).get("name", ""))
                             for a in published[:6]],
               latest_all=[{"slug": a["slug"], "title": a["title"],
                            "desc": _one_sentence(a.get("meta_description", "")),
                            "updated": a.get("updated", ""),
                            "updated_human": human_date(a.get("updated", "")),
                            "category": cat_map.get(a.get("cluster", ""), {}).get("name", "")}
                           for a in published[6:12]],
               pillar_cards=[_card_meta(site, a, cat_map.get(a.get("cluster", ""), {}).get("name", ""))
                             for a in pillars])
    _write(SITE / "index.html", env.get_template("index.html").render(**ctx))

    # --- legal / info pages ---
    pages = [
        ("about", "About", "Who we are and how our calculators work."),
        ("contact", "Contact", "Get in touch with the team."),
        ("privacy-policy", "Privacy Policy", "How we handle data and cookies."),
        ("terms", "Terms of Use", "The terms for using this site."),
        ("disclaimer", "Disclaimer", "Important limitations of our calculators."),
    ]
    for slug, title, desc in pages:
        src = CONTENT / "pages" / f"{slug}.md"
        body = src.read_text(encoding="utf-8") if src.exists() else f"# {title}\n\nComing soon."
        body = (body.replace("{{SITE_NAME}}", site["name"])
                    .replace("{{CONTACT_EMAIL}}", site.get("contact_email", ""))
                    .replace("{{CONTACT_BLOCK}}", _contact_block(site)))
        body = re.sub(r"\A\s*#\s+.*?\n", "", body)
        ctx = common(title=f"{title} | {site['name']}", description=desc[:155],
                     canonical=_abs(site, f"/{slug}/"),
                     schemas=[json.dumps(seolib.webpage_schema(title, desc, _abs(site, f"/{slug}/"), site),
                                         ensure_ascii=False),
                              json.dumps(seolib.breadcrumb_list(
                                  [("Home", "/"), (title, f"/{slug}/")], site),
                                  ensure_ascii=False)])
        ctx.update(page={"title": title, "html": mdrender.render(body)})
        _write(SITE / slug / "index.html", env.get_template("page.html").render(**ctx))

    # --- search (client-side; backs the WebSite SearchAction) ---
    search_index = [{"t": a["title"], "s": a["slug"], "k": a.get("primary_keyword", ""),
                     "c": cat_map.get(a.get("cluster", ""), {}).get("name", ""),
                     "d": a.get("meta_description", "")} for a in published]
    ctx = common(title=f"Search | {site['name']}",
                 description="Search GardenCalc's mulch, soil, gravel and other calculators.",
                 canonical=_abs(site, "/search/"), robots="noindex, follow")
    ctx.update(page={"title": "Search calculators & guides",
                     "html": '<div id="search-ui"><input type="search" id="q" '
                             'placeholder="Search calculators and guides…" aria-label="Search">'
                             '<ul id="results" class="post-list"></ul></div>',
                     "search": True})
    _write(SITE / "search" / "index.html", env.get_template("page.html").render(**ctx))

    # --- 404 ---
    cats_links = "".join(f'<li><a href="{base}/category/{c["id"]}/">{c["name"]} calculator</a></li>'
                         for c in categories)
    ctx = common(title=f"Page not found | {site['name']}",
                 description="The page you requested was not found.",
                 canonical=_abs(site, "/404.html"), robots="noindex, follow")
    ctx.update(page={"title": "Page not found",
                     "html": ("<p>That page does not exist. Try the <a href='" + base + "/'>homepage</a>, "
                              "or jump straight to a category:</p><ul>" + cats_links + "</ul>")})
    _write(SITE / "404.html", env.get_template("page.html").render(**ctx))

    # --- redirect stubs for merged pages (kept alive, canonical to the target) ---
    for st in merges.stubs(arts) + merges.rename_stubs(arts):
        target_url = _abs(site, f"/{st['target']}/")
        sctx = common(title=st["old_title"],
                      description=f"This page has moved to {st['target_title']}.",
                      canonical=target_url, robots="noindex, follow")
        sctx.update(page={"title": "This page has moved"},
                    target_url=target_url, target_title=st["target_title"])
        html = env.get_template("redirect.html").render(**sctx)
        _write(SITE / st["slug"] / "index.html", html)

    # --- chart pages (linkable, formula-derived reference tables) ---
    for ch in charts.CHARTS:
        cluster = cat_map.get(ch["cluster"], {})
        cluster_name = cluster.get("name", ch["cluster"].title())
        cp = charts.page(ch, base, site)
        calc_slug = ch.get("calc", "")
        cctx = common(title=ch["title"], description=ch["description"],
                      canonical=cp["url"], og_type="article",
                      og_image=_abs(site, "/static/img/og-default.png"),
                      keywords=ch["keyword"],
                      schemas=[json.dumps(seolib.breadcrumb_list(
                                   [("Home", "/"), (cluster_name, f"/category/{ch['cluster']}/"),
                                    (ch["title"], f"/{ch['slug']}/")], site), ensure_ascii=False),
                               json.dumps(seolib.webpage_schema(
                                   ch["title"], ch["description"], cp["url"], site),
                                   ensure_ascii=False),
                               json.dumps(seolib.faq_schema(
                                   {"faq": [{"q": q, "a": a} for q, a in ch["faqs"]]}),
                                   ensure_ascii=False)])
        cctx.update(chart=cp, cluster_name=cluster_name,
                    answer=ch["faqs"][0][1] if ch.get("faqs") else ch["description"],
                    pin_image=_abs(site, f"/static/img/pins/{ch['slug']}.png"),
                    cluster_planner=planner_by_cluster.get(ch["cluster"]))
        _write(SITE / ch["slug"] / "index.html",
               env.get_template("chart.html").render(**cctx))

    # --- project planners (multi-material shopping lists) ---
    for pl in planners.PLANNERS:
        cluster = cat_map.get(pl["cluster"], {})
        cluster_name = cluster.get("name", pl["cluster"].title())
        pp = planners.page(pl, base, site)
        pctx = common(title=pl["title"], description=pl["description"],
                      canonical=pp["url"], og_type="article",
                      og_image=_abs(site, "/static/img/og-default.png"),
                      keywords=pl["question"],
                      schemas=[json.dumps(seolib.breadcrumb_list(
                                   [("Home", "/"), (cluster_name, f"/category/{pl['cluster']}/"),
                                    (pl["title"], f"/{pl['slug']}/")], site), ensure_ascii=False),
                               json.dumps(seolib.webpage_schema(
                                   pl["title"], pl["description"], pp["url"], site),
                                   ensure_ascii=False),
                               json.dumps(seolib.faq_schema(
                                   {"faq": [{"q": q, "a": a} for q, a in pl["faqs"]]}),
                                   ensure_ascii=False)])
        pctx.update(planner=pp, cluster_name=cluster_name,
                    answer=pl["faqs"][0][1] if pl.get("faqs") else pl["description"],
                    pin_image=_abs(site, f"/static/img/pins/{pl['slug']}.png"))
        _write(SITE / pl["slug"] / "index.html",
               env.get_template("planner.html").render(**pctx))

    # --- seasonal evergreen guides (stable URLs, refreshed dates) ---
    for item in seasonal.SEASONAL:
        cluster = cat_map.get(item["cluster"], {})
        cluster_name = cluster.get("name", item["cluster"].title())
        sp = seasonal.page(item, base, site)
        sctx = common(title=item["title"], description=item["description"],
                      canonical=sp["url"], og_type="article",
                      og_image=_abs(site, "/static/img/og-default.png"),
                      keywords=item["keyword"],
                      schemas=[json.dumps(seolib.breadcrumb_list(
                                   [("Home", "/"), (cluster_name, f"/category/{item['cluster']}/"),
                                    (item["title"], f"/{item['slug']}/")], site), ensure_ascii=False),
                               json.dumps(seolib.webpage_schema(
                                   item["title"], item["description"], sp["url"], site),
                                   ensure_ascii=False),
                               json.dumps(seolib.faq_schema(
                                   {"faq": [{"q": q, "a": a} for q, a in item["faqs"]]}),
                                   ensure_ascii=False)])
        sctx.update(seasonal=sp, cluster_name=cluster_name,
                    answer=item["faqs"][0][1],
                    pin_image=_abs(site, f"/static/img/pins/{item['slug']}.png"))
        _write(SITE / item["slug"] / "index.html",
               env.get_template("seasonal.html").render(**sctx))

    # --- calculators hub ---
    groups = []
    for c in categories:
        cards = [_card_meta(site, a, c["name"]) for a in published
                 if a.get("cluster") == c["id"] and a.get("is_pillar")]
        if cards:
            groups.append({"id": c["id"], "name": c["name"], "cards": cards})
    ctx = common(title=f"Home & Garden Calculators | {site['name']}",
                 description=("Every free GardenCalc calculator in one place: mulch, soil, topsoil, "
                              "gravel, paint, tile, grass seed, concrete and fertilizer."),
                 canonical=_abs(site, "/calculators/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Calculators", "/calculators/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=groups, chart_cards=chart_cards, planner_cards=planner_cards,
               seasonal_cards=seasonal_cards)
    _write(SITE / "calculators" / "index.html",
           env.get_template("calculators.html").render(**ctx))

    # --- guides index (all non-pillar articles, grouped, filterable) ---
    guide_groups = []
    for c in categories:
        items = [_card_meta(site, a, c["name"]) for a in published
                 if a.get("cluster") == c["id"] and not a.get("is_pillar")]
        if items:
            guide_groups.append({"id": c["id"], "name": c["name"], "entries": items})
    ctx = common(title=f"Garden & Home Project Guides | {site['name']}",
                 description=("Every GardenCalc how-to guide in one place, grouped by project: "
                              "mulch, soil, gravel, paint, tile, seed, concrete and more."),
                 canonical=_abs(site, "/guides/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Guides", "/guides/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=guide_groups, seasonal_cards=seasonal_cards)
    _write(SITE / "guides" / "index.html", env.get_template("guides.html").render(**ctx))

    # --- HTML sitemap (human-readable; helps discovery and internal linking) ---
    site_pages = [{"slug": s, "title": t} for s, t, _ in pages]
    ctx = common(title=f"Sitemap | {site['name']}",
                 description=("A full list of every calculator, chart and guide on "
                              f"{site['name']}."),
                 canonical=_abs(site, "/sitemap/"),
                 schemas=[json.dumps(seolib.breadcrumb_list([("Home", "/"), ("Sitemap", "/sitemap/")], site),
                                     ensure_ascii=False)])
    ctx.update(groups=guide_groups,
               calculators=[_card_meta(site, a, cat_map.get(a.get("cluster", ""), {}).get("name", ""))
                            for a in published if a.get("is_pillar")],
               chart_cards=chart_cards, planner_cards=planner_cards,
               seasonal_cards=seasonal_cards, site_pages=site_pages)
    _write(SITE / "sitemap" / "index.html", env.get_template("sitemap.html").render(**ctx))

    # --- for publishers (indexable; explains how to embed/cite the calculators) ---
    embeds = []
    for a in published:
        if a.get("is_pillar") and a.get("calculator"):
            embeds.append({"title": a.get("calculator_title") or a["title"],
                           "calc_slug": a["slug"],
                           "embed_url": _abs(site, f"/embed/{a['calculator']}/")})
    ctx = common(title=f"Embed or Cite Our Calculators | {site['name']}",
                 description=("Free embeddable garden and home calculators. Add a mulch, soil or "
                              "concrete calculator to your site with one line of HTML."),
                 canonical=_abs(site, "/for-publishers/"),
                 schemas=[json.dumps(seolib.breadcrumb_list(
                              [("Home", "/"), ("For publishers", "/for-publishers/")], site),
                              ensure_ascii=False)])
    ctx.update(embeds=embeds)
    _write(SITE / "for-publishers" / "index.html",
           env.get_template("publishers.html").render(**ctx))

    # --- embed pages (noindex, canonical to the full calculator; not in the sitemap) ---
    for a in published:
        if not (a.get("is_pillar") and a.get("calculator")):
            continue
        calc_ctx = _calc_context(a, tcfg, site)
        if not calc_ctx:
            continue
        ectx = dict(site=site, base_url=base, calc=calc_ctx,
                    canonical=_abs(site, f"/{a['slug']}/"),
                    calc_url=_abs(site, f"/{a['slug']}/"))
        _write(SITE / "embed" / a["calculator"] / "index.html",
               env.get_template("embed.html").render(**ectx))

    # --- static (copied first so generated figures sit in site/static) ---
    static_dest = SITE / "static"
    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(STATIC, static_dest)

    # Generate original figures into the copied static dir so pages can link them.
    img_stats = images.generate(published, static_dest)
    brand_stats = images.render_brand(static_dest)
    pin_cards = [{"slug": ch["slug"], "title": ch["title"], "question": charts.CHART_QUESTIONS.get(ch["slug"], ""),
                  "cluster": ch["cluster"]} for ch in charts.CHARTS]
    pin_cards += [{"slug": pl["slug"], "title": pl["title"], "question": pl["question"],
                   "cluster": pl["cluster"]} for pl in planners.PLANNERS]
    pin_cards += [{"slug": it["slug"], "title": it["title"], "question": it["question"],
                   "cluster": it["cluster"]} for it in seasonal.SEASONAL]
    pin_stats = images.render_pins(pin_cards, static_dest)
    _write(static_dest / "search-index.json", json.dumps(search_index, ensure_ascii=False))

    # --- sitemap, robots, rss, CNAME ---
    # Only canonical, indexable pages go in the sitemap. <priority> is omitted: it is
    # ignored by Google/Bing, so emitting it only adds noise.
    today = dt.date.today().isoformat()
    urls = [{"loc": "/", "lastmod": today,
             "image": _thumb(site, published[0]) if published else None,
             "image_title": site["name"]}]
    urls += [{"loc": f"/category/{c['id']}/", "lastmod": today} for c in categories]
    urls += [{"loc": f"/{a['slug']}/", "lastmod": a.get("updated"),
              "image": _fig(site, a), "image_title": a["title"]} for a in published]
    urls += [{"loc": f"/{ch['slug']}/", "lastmod": today} for ch in charts.CHARTS]
    urls += [{"loc": f"/{pl['slug']}/", "lastmod": today} for pl in planners.PLANNERS]
    urls += [{"loc": f"/{item['slug']}/", "lastmod": item["updated"]} for item in seasonal.SEASONAL]
    urls += [{"loc": f"/{s}/", "lastmod": today} for s, _, _ in pages]
    urls += [{"loc": p, "lastmod": today} for p in EXTRA_PAGES]
    _write(SITE / "sitemap.xml", seolib.sitemap_xml(urls, site))
    _write(SITE / "robots.txt", seolib.robots_txt(site, _abs(site, "/sitemap.xml")))
    feed_extra = [{"title": ch["title"], "url": _abs(site, f"/{ch['slug']}/"),
                   "description": ch["description"]} for ch in charts.CHARTS]
    feed_extra += [{"title": pl["title"], "url": _abs(site, f"/{pl['slug']}/"),
                    "description": pl["description"]} for pl in planners.PLANNERS]
    feed_extra += [{"title": item["title"], "url": _abs(site, f"/{item['slug']}/"),
                    "description": item["description"]} for item in seasonal.SEASONAL]
    _write(SITE / "rss.xml", seolib.rss_xml(published, site, extra=feed_extra))
    if site.get("custom_domain"):
        _write(SITE / "CNAME", site["custom_domain"] + "\n")
    _write(SITE / ".nojekyll", "")

    _generate_og_images(published, site)

    indexnow_key = str(site.get("indexnow_key", "")).strip()
    if indexnow_key:
        _write(SITE / f"{indexnow_key}.txt", indexnow_key)

    stats = {
        "built": dt.datetime.now(dt.timezone.utc).isoformat(),
        "articles": len(published),
        "categories": len(categories),
        "pages": len(pages) + 1,
        "urls": len(urls),
        "figures": img_stats.get("figures", 0),
    }
    save_json(DATA / "build.json", stats)
    print(f"[build] {stats}")
    return stats


def _generate_og_images(arts: list[dict], site: dict) -> None:
    """Lightweight SVG social images (no external service, no cost)."""
    out = SITE / "static" / "img" / "og"
    out.mkdir(parents=True, exist_ok=True)

    def card(title: str, sub: str) -> str:
        t = title[:70].replace("&", "&amp;").replace("<", "&lt;")
        s = sub[:90].replace("&", "&amp;").replace("<", "&lt;")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">'
                f'<rect width="1200" height="630" fill="#14532d"/>'
                f'<rect x="40" y="40" width="1120" height="550" fill="#166534" rx="24"/>'
                f'<text x="90" y="300" font-family="Georgia,serif" font-size="54" fill="#f0fdf4">{t}</text>'
                f'<text x="90" y="380" font-family="Arial" font-size="30" fill="#bbf7d0">{s}</text>'
                f'<text x="90" y="540" font-family="Arial" font-size="26" fill="#86efac">{site["name"]}</text>'
                f'</svg>')

    _write(out / ".." / "og-default.svg", card(site["name"], site.get("tagline", "")))
    for a in arts:
        _write(out / f"{a['slug']}.svg", card(a["title"], a["meta_description"]))


if __name__ == "__main__":
    build()
