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
    "sand": [
        ("How much does a cubic yard of sand weigh?", "About 1.35 tons for damp builder's sand, a little more when wet."),
        ("How deep should sand be under pavers?", "About one inch as a screeded bedding layer over a compacted base."),
        ("How many bags of sand in a cubic yard?", "Fifty-four 0.5 cubic foot bags, since a cubic yard is 27 cubic feet."),
        ("Can I use play sand for a paver base?", "No. Use sharp or builder's sand, which compacts and locks together; play sand is too round and smooth."),
    ],
    "compost": [
        ("How much compost should I add?", "One to three inches worked into the top layer of a bed, or a quarter inch as a lawn top-dressing."),
        ("How many bags of compost in a cubic yard?", "Twenty-seven 1 cubic foot bags, since a cubic yard is 27 cubic feet."),
        ("Can you put compost too thick?", "Yes. A deep blanket can smother roots and tie up nitrogen, so mix it in rather than piling it on."),
        ("Is compost the same as topsoil?", "No. Compost is decomposed organic matter that feeds the soil; topsoil is mineral soil that adds bulk and structure."),
    ],
    "bark": [
        ("How deep should bark mulch be?", "Two to three inches for most beds; keep it clear of trunks and stems."),
        ("How many bags of bark in a cubic yard?", "Thirteen and a half 2 cubic foot bags, since a cubic yard is 27 cubic feet."),
        ("Do bark chips stop weeds?", "They suppress most weeds at three inches deep, especially over a layer of landscape fabric."),
        ("Which lasts longer, bark nuggets or shredded bark?", "Nuggets last longer but float and shift on slopes; shredded bark knits together and stays put."),
    ],
    "sod": [
        ("How many rolls of sod do I need?", "Divide the lawn area by the roll coverage, usually 10 sq ft, then add about 5% for trimming."),
        ("How much does a pallet of sod cover?", "Commonly about 500 square feet, though it varies by supplier and roll size."),
        ("How long does sod take to root?", "About two weeks of keeping it damp; then water deeply and less often to push roots down."),
        ("Can you lay sod over existing grass?", "No. Remove or kill the old grass and prepare a firm, level base, or the new sod will not knit in."),
    ],
}


def _meta_description(title: str, kw: str, calc_title: str, body: str = "") -> str:
    """Lead with the article's own answer rather than echoing the query, which reads
    as filler in search results and suppresses clicks."""
    import re as _re
    plain = _re.sub(r"[#*`_>\[\]]", "", body or "")
    plain = _re.sub(r"\s+", " ", plain).strip()
    sentences = _re.split(r"(?<=[.!?])\s+", plain)
    # Keep adding sentences until the meta is long enough to read as a real
    # snippet (>=110 chars), then trim to the upper bound.
    parts, length = [], 0
    for sent in sentences:
        if len(sent) < 40:
            continue
        parts.append(sent)
        length = len(" ".join(parts))
        if length >= 110:
            break
    answer = " ".join(parts).strip().replace("**", "")
    if not answer:
        answer = (f"How much {kw} you need, with the formula, a worked example and "
                  f"common mistakes.")
    return _clip_meta(answer)


# Words a search snippet should never end on: a description cut after one of these
# reads as truncated filler ("...13 bags of.").
_DANGLING = {"a", "an", "the", "of", "to", "for", "and", "or", "by", "with", "in",
             "on", "at", "as", "is", "are", "was", "were", "be", "been", "this",
             "that", "these", "those", "your", "you", "it", "its", "from", "into",
             "over", "under", "than", "then", "about", "atop"}


def _clip_meta(text: str, limit: int = 158, floor: int = 110) -> str:
    """Trim a meta description to a length Google will not truncate.

    Cuts at a sentence boundary when one fits, otherwise at a word boundary, and
    never leaves a dangling function word or a half word at the end.
    """
    text = text.strip()
    if len(text) > limit:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        kept = ""
        for sent in sentences:
            candidate = (kept + " " + sent).strip()
            if len(candidate) > limit:
                break
            kept = candidate
        if kept and len(kept) >= 100:
            text = kept
        else:
            text = text[: limit - 1].rsplit(" ", 1)[0]
    # A value cut after a connector and a bare figure ("...cubic yards or 22.",
    # "...and the number of 60.") reads as truncated. Drop only the dangling clause,
    # back to the previous clause boundary, so the rest of the sentence is kept.
    _tail = re.compile(
        r"\b(?:of|or|about|approximately|around|roughly|per|by|to|and|at|for|with|"
        r"than|over|under|near)\s+[\d.,]+\s*\.?$", re.I)
    core0 = text.rstrip(".!? ")
    m = _tail.search(core0)
    if m:
        head = core0[:m.start()]
        cut = max(head.rfind(", "), head.rfind(" and "), head.rfind(" or "))
        if cut > 0:
            head = head[:cut]
        head = head.rstrip(" ,;:—-")
        # Only cut when the result still clears the minimum length; a too-short meta
        # fails the quality gate, which is worse than an awkward but complete one.
        if len(head) >= floor:
            text = head
    # Never leave a dangling function word: a snippet cut after "...bags of."
    # reads as truncated filler and depresses clicks.
    core = text.rstrip(".!? ").rstrip(" ,;:—-")
    while core and core.rsplit(" ", 1)[-1].lower() in _DANGLING:
        core = core.rsplit(" ", 1)[0].rstrip(" ,;:—-")
    if core != text.rstrip(".!? ").rstrip(" ,;:—-"):
        return core + "."
    return text


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
    suffix = ": Calculator & Guide"
    if len(kw_title) + len(suffix) <= 60:
        return kw_title + suffix
    if len(kw_title) <= 60:
        return kw_title
    return kw_title[:57].rstrip() + "..."


def _cluster_key(calc_key: str) -> str:
    """FAQ_TEMPLATES keys grass_seed; calculators use grass_seed too. Keep them aligned."""
    return calc_key


def _primary_size(kw: str) -> float | None:
    """Pull a job size out of the keyword (e.g. '500 sq ft', '10x10', '10 x 12')."""
    m = re.search(r"(\d+)\s*[x×]\s*(\d+)", kw)
    if m:
        return float(m.group(1)) * float(m.group(2))
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*(?:sq\s*\.?\s*ft|square\s+feet|square\s+foot)", kw)
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _keyword_defaults(calc_key: str, calc_def: dict, kw: str) -> dict:
    """Keyword-faithful inputs: when the search says '300 square feet' or '10x10', the
    worked example must use that size, not the calculator's generic defaults."""
    defaults = {i["id"]: i["default"] for i in calc_def["inputs"] if "default" in i}
    ids = {i["id"] for i in calc_def["inputs"]}
    size = _primary_size(kw)

    if calc_key in ("mulch", "soil", "gravel", "concrete") and size:
        if "length" in ids and "width" in ids:
            defaults["length"] = round(size ** 0.5, 1)
            defaults["width"] = round(size ** 0.5, 1)
    elif calc_key == "grass_seed" and size and "area" in ids:
        defaults["area"] = size
    elif calc_key == "paint" and size and "length" in ids and "width" in ids:
        defaults["length"] = round(size ** 0.5, 1)
        defaults["width"] = round(size ** 0.5, 1)
    elif calc_key == "tile" and size and "length" in ids and "width" in ids:
        defaults["length"] = round(size ** 0.5, 1)
        defaults["width"] = round(size ** 0.5, 1)

    # Room/slab keywords that name the room type rather than the size.
    if "bedroom" in kw and calc_key == "paint":
        defaults.update({"length": 12, "width": 10, "height": 8})
    if "driveway" in kw and calc_key == "gravel":
        defaults.update({"length": 30, "width": 12, "depth": 4})
    if "french drain" in kw and calc_key == "gravel":
        defaults.update({"length": 20, "width": 1, "depth": 18})
    return defaults


# Curated pillar prose for clusters the generic fallback cannot serve well: their tools
# are close enough that a templated draft trips the duplicate-content gate. Each body is
# written per topic, with the live worked example spliced in under "## Worked Example".
PILLAR_PROSE: dict[str, str] = {
    "sand": """Sand is bought by the ton, the cubic yard or the bag, and the right depth
depends on the job. A paver bedding layer is screeded to about an inch over a compacted
base; a sandbox is filled three to four inches deep; structural fill is placed in shallow
lifts and compacted. Measure the length and width, set the depth for your job, and the
calculator converts the volume into cubic yards, tons and bags of 0.5 cubic feet.

## How to Calculate Sand

1. Measure the length and width of the area in feet and multiply them to get square feet.
2. Decide the depth in inches: about 1 in for a paver bedding layer, 3-4 in for a sandbox.
3. Convert the depth to feet by dividing by 12.
4. Multiply the area by the depth in feet to get cubic feet.
5. Divide by 27 for cubic yards, or use the ton and bag figures the calculator reports.

## Which Sand to Use

Not every bag labelled "sand" behaves the same. Sharp or builder's sand has angular grains
that interlock under compaction, which is why it is the standard bedding layer under pavers.
Masonry sand is finer and more uniform, which suits mortar and a thin leveling course. Play
sand is washed and rounded, so it stays soft underfoot and drains freely but will not lock
together; keep it for sandboxes, not for a patio base. For joints between pavers, polymeric
sand is swept in and wetted so it sets and resists washing out.

## Worked Example

{worked}

## How Deep Should Sand Be?

Match the depth to the job rather than filling to one uniform height. A bedding layer much
deeper than an inch is hard to screed evenly and can settle unevenly under the pavers. A
sandbox needs enough depth for play, but any deeper than four inches and the top dries out
while the base stays damp. Structural fill should always go in shallow, compacted lifts, or
it will slump after the first wet season.

## Ordering Sand by Weight or Volume

Damp builder's sand weighs about 1.35 tons per cubic yard, so a bulk order is often priced
and delivered by weight even though the job is measured by volume. Ask the supplier which
figure they use, and remember that a cubic yard is 27 cubic feet, or 54 bags of 0.5 cubic
feet. For anything small enough to carry, bagged sand is easier to handle, but it costs far
more per cubic foot than a bulk delivery.

## Sand for Sandboxes and Play Areas

Play sand is screened and washed so it is free of sharp debris and fine dust, which is why
it costs more than builder's sand. Fill a sandbox three to four inches deep for young
children, a little deeper for older ones, and cover it when it is not in use to keep animals
and leaves out. Because play sand is rounded, it drains well and stays loose underfoot, but
that same roundness is why it will not compact or support a paver.

## Sand or Gravel Under a Patio?

Both go under hard landscaping, but they do different jobs. Gravel forms the structural base,
compacted in layers so it carries the load without settling. Sand is the thin bedding layer
that lets you screed the surface flat and tap each paver down to the same height. Skipping the
gravel and using deep sand alone is a common shortcut that ends with pavers sinking and
shifting within a season, so treat the two as a pair rather than a choice.

## Common Mistakes to Avoid

- Using rounded play sand under pavers, which will not compact or interlock.
- Raking the bedding sand to a guessed depth instead of screeding it to a straight board.
- Laying sand over soft soil with no landscape fabric, so it migrates downward.
- Filling a base in one deep layer instead of compacting shallow lifts.
""",
    "compost": """Compost is a soil amendment rather than a mulch or a fill: its job is to
feed soil life and improve structure, and it works best mixed into the top few inches rather
than left in a thick blanket on the surface. For a new bed, spread about two inches and fork
it into the top six inches; for an established bed, an inch as a top-dressing is plenty. Enter
the area and depth, and the calculator returns cubic feet, cubic yards and bags of one cubic
foot.

## How to Calculate Compost

1. Measure the length and width of the bed in feet and multiply them for the area.
2. Choose a depth: a quarter to half an inch to top-dress a lawn, one inch to refresh beds,
   two to three inches to work into new or poor soil.
3. Convert the depth to feet by dividing by 12.
4. Multiply the area by the depth in feet to get cubic feet.
5. Divide by 27 for cubic yards, or read the bag count the calculator reports.

## How Much Compost to Add

The right amount depends on what you are doing. A light quarter-inch top-dressing on an
established lawn feeds the grass without smothering it. An inch raked over a border tops up
the organic matter that the previous season used. Two inches forked into a new bed gives
roots something to work with, and three inches is about the most worth tilling into poor
soil before it stops behaving like an amendment and starts behaving like a growing medium.

## Worked Example

{worked}

## Compost, Topsoil and Mulch Are Not the Same

These three are often used together but do different jobs. Compost is decomposed organic
matter that feeds soil biology and improves structure. Topsoil is mineral soil that adds bulk
and a rooting depth where there is none. Mulch sits on the surface to slow evaporation and
suppress weeds. A raised bed usually wants a blend, while an established border mostly wants
compost worked in and a separate mulch layer on top.

## Buying Compost in Bulk or by the Bag

Bagged compost is normally sold in one cubic foot bags, so a cubic yard is 27 of them, and
that is the number to compare against a bulk price. Bulk compost is far cheaper per cubic
foot but arrives tipped on a hard surface, so plan where the pile goes and how you will move
it before you order. Fresh manure-based compost should be left to age, or it can burn young
roots and carry weed seeds through to the bed.

## Compost for Lawns and Vegetable Beds

Lawns and vegetable beds want compost in different ways. A lawn is top-dressed thinly and
then watered in, so the grass is fed without being buried; a quarter inch is the usual dose,
worked in with the back of a rake. Vegetable beds are hungry and are replanted every season,
so two inches forked into the top layer before planting gives the roots something to draw on
and improves how the soil holds water. Both benefit from a repeat the following year, because
compost is consumed as it feeds the soil.

## Does Compost Replace Fertiliser?

No. Compost feeds the soil, slowly releasing nutrients as it breaks down and improving the
soil's structure and water-holding capacity. Fertiliser feeds the plant directly with a
measured dose of nutrients. In practice you want both: compost to build the soil over time,
and a fertiliser at the right rate when a crop or a lawn needs a quick, specific boost. The
fertiliser calculator covers that side of the job.

## Common Mistakes to Avoid

- Spreading a deep blanket instead of mixing a modest layer into the top few inches.
- Using fresh, unaged manure-based compost around young plants.
- Treating compost as a substitute for topsoil when the job needs bulk and rooting depth.
- Forgetting that compost keeps breaking down, so beds settle and need topping up.
""",
    "bark": """Bark and wood chips are decorative mulches, and both the texture and the
depth matter. Large bark nuggets last longest but float in heavy rain and shift on slopes,
while shredded bark knits into a mat that stays put. Spread two to three inches for most
beds, up to four where weeds are established, and keep every layer a few inches clear of
trunks and stems. Enter the area and depth and the calculator returns cubic feet, cubic
yards and bags of two cubic feet.

## How to Calculate Bark

1. Measure the length and width of the bed in feet and multiply them for the area.
2. Choose a depth: two inches to refresh beds, three inches for standard cover, up to four
   inches where you are suppressing established weeds.
3. Convert the depth to feet by dividing by 12.
4. Multiply the area by the depth in feet to get cubic feet.
5. Divide by 27 for cubic yards, or read the bag count the calculator reports.

## Bark, Wood Chips and Compost Compared

Bark nuggets are the slowest to break down and hold their colour for years, which suits
formal beds, but they are the least stable on a slope. Shredded bark interlocks and resists
washing, so it is the better choice on banks and around trees. Wood chips are the cheapest
cover and excellent on paths and in play areas, though they break down faster. Compost is not
a surface mulch at all; it belongs mixed into the soil, not piled on top of it.

## Worked Example

{worked}

## Spreading Bark So It Stays Put

Water the ground before you lay bark, because a thick, dry layer can shed rain rather than
let it through. Rake it to an even depth rather than dumping and spreading, and feather the
edges so the bed does not look like a raised box. Keep the layer clear of trunks, stems and
the crowns of perennials: a pile held against bark traps moisture and invites rot and pests.
On a slope, use shredded bark and lay it a little thicker at the top of the run.

## Refreshing Bark Each Season

A thin fresh layer each spring keeps the colour and the weed control without the cost of
replacing the whole bed. Bark sold in bags is usually two cubic feet, so a cubic yard is
thirteen and a half bags; bulk is sold by the cubic yard and is much cheaper for a large
area. Break up any matted or compacted old layer first, so water can still reach the soil
underneath.

## Bark Around Trees and Shrubs

Trees and shrubs are where bark earns its keep, but they are also where it is most often
misused. A ring of bark out to the drip line keeps mowers and strimmers away from the trunk
and holds moisture over the roots, which is exactly what a young tree needs. The mistake is
the "mulch volcano": a cone of bark piled up against the trunk, which keeps the bark tissue
permanently damp and invites rot, canker and pests. Keep the layer flat and pull it back a
few inches from the trunk so the flare is visible.

## How Often to Top Up Bark

Bark breaks down slowly and sinks as it does, so a bed loses perhaps an inch of depth over a
year. A thin fresh layer each spring restores the look and the weed control without the cost
and effort of stripping the bed. Rake the old surface first to break up any matted or
compacted patches, then top up to the depth you want. If the layer has built up past about
four inches over several years, rake some out rather than adding more, because too deep a
layer keeps water from reaching the soil.

## Common Mistakes to Avoid

- Piling bark against trunks and stems, which holds moisture and causes rot.
- Using nuggets on a slope, where they float and slide after heavy rain.
- Laying it too thin, so weeds push through within weeks.
- Treating bark as a soil improver and digging it in, instead of using compost for that.
""",
    "sod": """Sod is living turf lifted with a thin layer of soil, so it has to root into the
ground below within days of arriving. That makes ground preparation the whole job. Measure
the lawn area, allow about five per cent extra for trimming around edges and curves, and the
calculator returns the number of rolls (at 10 square feet each) and the pallets, at about 500
square feet each.

## How to Calculate Sod

1. Measure the length and width of the lawn in feet and multiply them for the area.
2. Divide by the coverage of one roll, commonly 10 square feet.
3. Add about five per cent for trimming around edges, paths and curves.
4. Round up to whole rolls, or order by the pallet where the area is large enough.
5. Prepare and firm the soil before delivery so the sod can be laid the same day.

## Preparing the Ground

Sod roots into whatever is underneath it, so the base decides whether it takes. Clear and
kill the old grass, rotovate or fork the top few inches, firm it, and rake it level. Water
the surface just before the rolls go down so there is moisture for the roots to find. On a
slope, rake the surface to a slight tilt so water does not pool under the turf and rot the
roots.

## Worked Example

{worked}

## Laying the Rolls

Lay the first roll along a straight edge, such as a path or a drive, and work outward from
there. Butt each roll tight against the last and stagger the joints like brickwork, so the
seams do not line up into a weak strip. Press each roll firmly onto the soil, then roll the
finished area to squeeze out air pockets and ensure good contact. Trim the edges with a
half-moon edger or a sharp knife, and keep the whole area damp for the first fortnight.

## Watering and the First Few Weeks

New sod needs frequent, light watering until it knits in, then a change of habit: water
deeply and less often, which pushes roots downward and makes the lawn tougher in dry spells.
Stay off it for the first week or two, and hold off on fertiliser until it has started to
grow, so the plant puts its energy into rooting rather than top growth. Once it has rooted,
tug a corner gently: if it lifts, it needs more time and more water.

## Sod or Seed?

Sod gives you an instant lawn, holds a slope against erosion from day one, and is the usual
choice when the area is on show or you cannot wait a season. Seed costs far less per square
foot and lets you pick a mix for shade, wear or drought, but it needs watering, weeding and
patience, and it will not hold bare ground through heavy rain. As a rough guide, sod for a
front lawn or a steep bank, and seed for a large back lawn where a few weeks of care are
acceptable.

## Choosing a Grass for Your Climate

Match the turf to the climate rather than to the picture on the pallet. Cool-season grasses
such as Kentucky bluegrass and tall fescue look best in northern states and stay green in
spring and autumn, though they can struggle in a hot, dry summer. Warm-season grasses such as
Bermuda and St. Augustine thrive in the south and shrug off heat, but they go dormant and
brown off in winter. Tell the supplier where you live and how much sun the lawn gets, and let
them steer the choice.

## Common Mistakes to Avoid

- Ordering the exact area with no allowance for trimming and offcuts.
- Laying sod onto unprepared or uneven ground, so the roots never make contact.
- Letting rolls sit stacked in the sun, which cooks the turf before it is laid.
- Watering lightly and often forever, which keeps roots shallow and the lawn fragile.
""",
}


def _curated_body(calc_key: str, calc_title: str, calc_short: str, worked: str,
                  secondary: list[str]) -> str:
    body = PILLAR_PROSE[calc_key].replace("{worked}", worked)
    if secondary:
        body += (f"\n## Related Questions\n\nPeople also search for "
                 f"{', '.join(secondary[:3])}. The method is the same in every case: measure "
                 f"the area, apply the depth or rate the job needs, then convert into the "
                 f"units your supplier sells in, using the {calc_title.lower()} for the "
                 f"arithmetic.\n")
    return body


def _fallback_body(kw: str, calc_title: str, calc_short: str, worked: str,
                   secondary: list[str], calc_key: str = "") -> str:
    if calc_key in PILLAR_PROSE:
        return _curated_body(calc_key, calc_title, calc_short, worked, secondary)
    import content_lib
    lib = content_lib.LIBRARY.get(calc_key, {})
    material_word = {
        "mulch": "mulch", "soil": "soil mix", "gravel": "gravel",
        "paint": "paint", "tile": "tile", "grass_seed": "grass seed",
        "concrete": "concrete mix", "sand": "sand", "compost": "compost",
        "bark": "bark", "sod": "sod",
    }.get(calc_key, "material")
    m = material_word
    size = _primary_size(kw)

    if size:
        context = (f"To cover {int(size) if size == int(size) else size} square feet, the "
                   f"short answer is to measure the area, multiply it by the depth or "
                   f"coverage rate the job needs, and convert the result into the units "
                   f"your supplier sells in.")
    else:
        context = (f"For {kw}, the short answer is to measure the area, multiply it by the "
                   f"depth or coverage rate the job needs, and convert the result into the "
                   f"units your supplier sells in.")
    analysis = (f"Our free {calc_title.lower()} below does the arithmetic and shows every "
                f"step, so you can sanity-check the answer and order with confidence.")

    if calc_key in ("mulch", "soil", "gravel", "concrete", "sand", "compost", "bark"):
        steps = ("1. Measure the length and width in feet and multiply them to get the area.\n"
                 "2. Decide the depth (or thickness) the job needs, in inches.\n"
                 "3. Convert the depth to feet by dividing by 12.\n"
                 "4. Multiply the area by the depth in feet to get cubic feet.\n"
                 "5. Divide cubic feet by 27 to get cubic yards, or use the bag and ton "
                 "figures the calculator reports.\n")
    elif calc_key == "sod":
        steps = ("1. Measure the lawn area in square feet.\n"
                 "2. Divide by the coverage of one roll, commonly 10 sq ft.\n"
                 "3. Add about 5% for trimming around edges and curves.\n"
                 "4. Round up to whole rolls, or order by the pallet (about 500 sq ft).\n"
                 "5. Prepare and firm the soil before the sod arrives so it can be laid the "
                 "same day.\n")
    elif calc_key == "grass_seed":
        steps = ("1. Measure the lawn area in square feet.\n"
                 "2. Check whether you are seeding a new lawn or overseeding an existing one.\n"
                 "3. Apply the coverage rate for that method, in pounds per 1,000 sq ft.\n"
                 "4. Multiply the area by the rate to get total pounds.\n"
                 "5. Round up to whole bags so you do not run short.\n")
    elif calc_key == "paint":
        steps = ("1. Add the room's length and width, then double it to get the perimeter.\n"
                 "2. Multiply the perimeter by the wall height for the wall area.\n"
                 "3. Subtract about 21 sq ft per door and 15 sq ft per window.\n"
                 "4. Multiply by the number of coats.\n"
                 "5. Divide by the paint's coverage per gallon, usually about 350 sq ft.\n")
    elif calc_key == "tile":
        steps = ("1. Measure the length and width of the floor and multiply for the area.\n"
                 "2. Work out each tile's area from its own width and height.\n"
                 "3. Divide the floor area by the tile area to get the tile count.\n"
                 "4. Add a waste allowance: 10% for a straight lay, 15% for diagonal.\n"
                 "5. Round up to whole boxes, checking the coverage printed on the box.\n")
    else:
        steps = ("1. Measure the area and the required depth.\n"
                 "2. Multiply area by depth to get the volume.\n"
                 "3. Convert to the units you buy in.\n")

    parts = [
        f"{context}\n",
        f"{analysis}\n",
        f"## How to Calculate {calc_short.title()}\n",
        steps,
        f"## Worked Example\n\n{worked}\n",
    ]

    if calc_key in ("mulch", "soil", "gravel", "concrete", "sand", "compost", "bark"):
        if size:
            parts.append(f"This example is set to the job size in the question, so the "
                         f"figures line up with what you searched for. Change the inputs in "
                         f"the calculator to match your own measurements.\n")
        else:
            parts.append(f"These are the calculator's default values, so you can see the "
                         f"whole calculation laid out before you change anything.\n")
    else:
        parts.append(f"Work through the same steps with your own measurements; the "
                     f"calculator above updates as you type.\n")

    if lib.get("depths"):
        parts.append(f"## How Deep Should {m.title()} Be?\n")
        parts.append(content_lib.depth_table_md(calc_key) + "\n")
        parts.append(f"Match the depth to the job rather than reaching for the deepest "
                     f"option. Too shallow and {m} fails early; too deep and you waste "
                     f"material and money.\n")

    size_table = content_lib.size_table_md(calc_key)
    if size_table:
        parts.append("## How Much You Need at Common Sizes\n")
        parts.append(size_table + "\n")
        parts.append("Use the calculator for your exact measurements; this table is here so "
                     "you can sanity-check the result at a glance.\n")

    if lib.get("materials"):
        parts.append(f"## Which Type of {m.title()} to Choose\n")
        parts.append(content_lib.materials_md(calc_key) + "\n")
        parts.append("Match the product to the job rather than to the lowest price, and check "
                     "the supplier's stated coverage because it varies between brands.\n")

    mistakes = {
        "mulch": [
            "Piling mulch against trunks and stems, which traps moisture and causes rot.",
            "Laying it too thin, so weeds push straight through within weeks.",
            "Mulching dry soil and then not watering, which slows the bed down.",
            "Skipping the edge of the bed, where weeds creep back in first.",
        ],
        "soil": [
            "Filling a raised bed with garden soil straight from the ground, which compacts and drains poorly.",
            "Forgetting that the mix settles, so the bed ends up short of the brim.",
            "Mixing in fresh manure that has not rotted, which burns young roots.",
            "Leaving no freeboard, so soil washes out in the first heavy rain.",
        ],
        "gravel": [
            "Laying gravel straight onto soil without landscape fabric, so it sinks and weeds grow through.",
            "Skipping compaction, which leaves a loose surface that ruts under wheels.",
            "Ordering the exact volume with no margin, then running short mid-lay.",
            "Using a single coarse layer instead of a compacted base for a driveway.",
        ],
        "paint": [
            "Buying for one coat when two are needed for an even finish.",
            "Forgetting to subtract doors and windows, and over-buying.",
            "Painting over a glossy surface without priming, so the paint fails.",
            "Not keeping spare paint for touch-ups in the same colour code.",
        ],
        "tile": [
            "Ordering the exact area and ignoring the waste allowance for cuts.",
            "Mixing dye lots, which shows as a patchwork across the floor.",
            "Not checking the coverage on the box, which varies by size and thickness.",
            "Returning unopened boxes without keeping a spare for future repairs.",
        ],
        "grass_seed": [
            "Sowing on hard, compacted ground without preparing the surface.",
            "Using the new-lawn rate when overseeding, which wastes seed.",
            "Letting the seed dry out; it needs light, frequent watering to germinate.",
            "Sowing in summer heat instead of the damp early-autumn window.",
        ],
        "concrete": [
            "Mixing too much water, which weakens the finished slab.",
            "Pouring onto soft or uneven ground without a compacted base.",
            "Making the slab too thin for the load it will carry.",
            "Not allowing the slab to cure slowly under cover.",
        ],
    }.get(calc_key, [
        "Estimating by eye instead of measuring the actual area.",
        "Skipping the waste allowance, then running short mid-project.",
    ])
    parts.append("## Common Mistakes to Avoid\n")
    parts.extend(f"- {x}\n" for x in mistakes)

    closing = {
        "mulch": "## Getting the Coverage Right\n\nCoverage on the bag is only a guide. "
                 "Bags vary between 1.5 and 2 cubic feet, and the figure assumes a flat bed "
                 "rather than loose, fluffy mulch. If you are dressing beds that have not "
                 "been mulched for a year, the first layer will settle into the gaps and look "
                 "thin, so work to the deeper end of your chosen band and top up later.\n",
        "soil": "## Filling the Bed Properly\n\nFill in stages and water each layer so the "
                "mix settles before the next. Leave about two inches of freeboard below the "
                "rim, both to stop the soil washing out and to give you room to top up as the "
                "mix compacts. A raised bed topped off each spring normally needs about 10% of "
                "its original volume to stay full.\n",
        "gravel": "## Building a Surface That Lasts\n\nGravel is only as good as what is "
                  "underneath it. For anything driven on, excavate a little, lay landscape "
                  "fabric, then put down the stone in two compacted layers rather than one "
                  "thick tip. Each layer binds into the next and the surface stays flat far "
                  "longer. On a path, a single compacted layer over fabric is fine.\n",
        "paint": "## Getting an Even Finish\n\nA smooth, primed surface takes paint evenly "
                 "and covers in fewer coats. Sand lightly between coats, cut in the edges "
                 "first, and keep a wet edge so you are not painting over a drying line. If "
                 "you are changing colour, expect to need a primer or an extra coat, as "
                 "strong colours on light walls are the hardest to cover.\n",
        "tile": "## Ordering and Cutting\n\nOrder all the tile in one go so it comes from a "
                "single dye lot, and keep a box in reserve for damage. Plan the layout from "
                "the centre of the room so cut tiles are even on both sides, and allow a few "
                "millimetres for grout lines if you are working to an exact grid.\n",
        "grass_seed": "## Getting Seed to Germinate\n\nSeed needs contact with the soil, "
                      "light moisture and warmth. Rake it in so it is barely covered rather "
                      "than buried, keep the surface damp for the first fortnight, and protect "
                      "it from birds if you have a lot of foot traffic. Early autumn is the "
                      "easiest window, as the soil is still warm and weeds are slowing.\n",
        "concrete": "## Getting the Mix and Curing Right\n\nA stiff mix made with the water "
                    "stated on the bag cures far stronger than a wet, easy-to-pour one. Let "
                    "the slab cure slowly under a cover for several days rather than letting "
                    "it dry in the sun, and cut control joints so it cracks where you want it "
                    "to.\n",
    }.get(calc_key)
    if closing:
        parts.append(closing)

    if lib.get("tools"):
        parts.append(f"\n## Tools and Materials You Will Need\n\nFor this job, have to "
                     f"hand {lib['tools']}. None of it is specialist, and most of it you "
                     f"probably already own; hire only what you will use once.\n")

    parts.append("## When to Call a Professional\n")
    parts.append("Measuring and ordering are straightforward for most garden and decorating "
                 "jobs, but a few are worth handing over. Structural work, retaining walls "
                 "over about two feet, anything affecting drainage around a building, and "
                 "electrical or gas work should go to a qualified tradesperson. The same "
                 "applies if the ground is unstable or you are unsure about base preparation, "
                 "because a survey costs far less than a failed pour or a wall that moves.\n")

    if secondary:
        parts.append(f"\n## Related Questions\n\nPeople also search for "
                     f"{', '.join(secondary[:3])}. The method is the same in every case: "
                     f"measure the area, apply the depth or rate the job needs, then convert "
                     f"into the units your supplier sells in, using the {calc_title.lower()} "
                     f"for the arithmetic.\n")

    extra = content_lib.extra_section_md(calc_key)
    if extra:
        parts.append("\n" + extra + "\n")

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

    defaults = _keyword_defaults(calc_key, calc_def, kw)
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
        # A truncated or interrupted response can come back very short. Retry once
        # rather than publishing/throwing away the slot with a stub.
        for attempt in range(2):
            body = llm.generate(prompt, system=SYSTEM, max_tokens=4096)
            if body and word_count(body) >= 400:
                break
            if body:
                print(f"[generate] short draft for {slug} "
                      f"({word_count(body)} words), retrying")
        if body:
            print(f"[generate] LLM draft for {slug}: {word_count(body)} words")
        if body and word_count(body) < 300:
            print(f"[generate] discard {slug}: draft too short after retry")
            return None
    if not body:
        # Without an LLM key the fallbacks produce templated drafts that are short and
        # alike across a cluster. Publishing those at scale is what creates duplicate/thin
        # pages, so a reject here is safer than a low-quality page. The curated pillar and
        # long-tail articles are hand-written and are never regenerated by this path.
        if not plan_item.get("is_pillar"):
            print(f"[generate] skip {slug}: no LLM key, long-tail fallback would be "
                  f"templated/thin (set GEMINI_API_KEY to generate quality articles)")
            return None
        body = _fallback_body(kw, calc_title, calc_short, worked, secondary, calc_key)
        print(f"[generate] template draft for {slug}: {word_count(body)} words")

    title = _title_for(kw, calc_title)
    faqs = FAQ_TEMPLATES.get(calc_key, [])
    today = dt.date.today().isoformat()
    record = {
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
        "meta_description": _meta_description(title, kw, calc_title, body),
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
    # The answer box is filled here, not only in the fixer: article_fix runs before the
    # quality gate, while a new article is still "draft", so a page that the fixer never
    # revisits would otherwise ship without the answer-first sentence a snippet needs.
    import article_fix  # local import: article_fix imports generate for its own repair
    record["answer"] = article_fix.answer_text(record)
    return record


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
