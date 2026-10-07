"""Domain content library.

Genuine, specific guidance per calculator type: required depths, coverage rates,
material choices and mistakes. Used both to enrich the offline draft and to give
the LLM accurate facts so it does not have to invent them.
"""
from __future__ import annotations

LIBRARY: dict[str, dict] = {
    "mulch": {
        "tools": "a tape measure, a wheelbarrow, a garden fork, gloves, and a hose for watering before you lay it",
        "unit_note": "Mulch is sold by the bag (usually 2 cubic feet) or by the cubic yard.",
        "depths": [
            ("1-2 in", "Refreshing thin beds and around shallow-rooted plants"),
            ("2-3 in", "Most flower beds and borders (the recommended default)"),
            ("3-4 in", "New beds and heavy weed suppression"),
            ("4+ in", "Avoid against stems; it holds moisture and can cause rot"),
        ],
        "materials": [
            ("Shredded hardwood", "Settles well, long-lasting, good for borders"),
            ("Pine bark", "Attractive, slower to break down, good for acid-loving plants"),
            ("Straw", "Cheap and light, best for vegetable beds"),
            ("Compost", "Feeds the soil as it breaks down; breaks down fastest"),
        ],
        "tips": [
            "Keep mulch a few inches clear of trunks and stems to prevent rot.",
            "Water the bed before mulching, not after.",
            "Reapply a thin layer each spring rather than one thick layer.",
        ],
    },
    "soil": {
        "tools": "a tape measure, a wheelbarrow or buckets, a garden fork, and a length of landscape fabric for the base",
        "unit_note": "Bagged soil is usually sold in 1.5 or 2 cubic foot bags; bulk is sold by the cubic yard.",
        "depths": [
            ("6 in", "Herbs, lettuce and other shallow-rooted crops"),
            ("10-12 in", "Most vegetables and flowering plants"),
            ("12-18 in", "Deep-rooted crops such as carrots, parsnips and tomatoes"),
            ("18+ in", "Raised beds over poor ground or for drainage-critical plants"),
        ],
        "materials": [
            ("60% topsoil / 30% compost / 10% perlite", "General-purpose raised-bed blend"),
            ("Compost-heavy mix", "Hungry feeders such as tomatoes and courgettes"),
            ("Sandy mix", "Root vegetables and drought-tolerant plants"),
            ("Coarse grit added", "Heavy clay soils needing drainage"),
        ],
        "tips": [
            "Fill in layers and water as you go to settle the mix.",
            "Leave two inches of freeboard so soil does not wash out.",
            "Top up by about 10% each year as the mix settles and breaks down.",
        ],
    },
    "gravel": {
        "tools": "a tape measure, landscape fabric, a rake, a plate compactor (hire for driveways), and a wheelbarrow",
        "unit_note": "Gravel is sold by the bag, the cubic yard or the ton. A cubic yard of 3/4 in crushed stone weighs about 1.4 tons.",
        "depths": [
            ("2 in", "Decorative borders and light footpaths"),
            ("3 in", "Garden paths and patio bases over fabric"),
            ("4 in", "Light driveways, compacted in two layers"),
            ("6 in", "Regular vehicle traffic and parking areas"),
        ],
        "materials": [
            ("3/4 in crushed stone", "All-round base and driveway choice"),
            ("Pea gravel", "Smooth, good for paths and play areas, less stable underfoot"),
            ("River rock", "Decorative borders and dry creek beds"),
            ("Decomposed granite", "Compacts firm, good for paths and patios"),
        ],
        "tips": [
            "Lay landscape fabric first so gravel does not sink into the soil.",
            "Compact in two thinner layers rather than one thick one.",
            "Add a border edge to stop gravel migrating into lawns.",
        ],
    },
    "paint": {
        "tools": "a tape measure, masking tape, dust sheets, a roller and tray, a brush for edges, and a filler for repairs",
        "unit_note": "One gallon covers roughly 350 square feet per coat on a smooth, primed wall.",
        "depths": [
            ("1 coat", "Same colour refresh on a similar tone"),
            ("2 coats", "Colour changes and new drywall (the usual default)"),
            ("3 coats", "Strong colour changes or dark-to-light transitions"),
        ],
        "materials": [
            ("Matt emulsion", "Ceilings and low-traffic walls; hides imperfections"),
            ("Eggshell", "Hallways and family rooms; wipes clean"),
            ("Satin", "Kitchens, bathrooms and trim"),
            ("Primer + topcoat", "Bare drywall, repairs and stained surfaces"),
        ],
        "tips": [
            "Subtract about 21 sq ft per door and 15 sq ft per window.",
            "Keep roughly 10% spare for touch-ups and note the colour code.",
            "Buy all cans at once so they come from the same batch.",
        ],
    },
    "tile": {
        "tools": "a tape measure, a notched trowel, tile spacers, a tile cutter, a spirit level, and grout",
        "unit_note": "Tile boxes list coverage in square feet; always check that figure rather than counting tiles.",
        "depths": [
            ("10% waste", "Straight, simple layouts"),
            ("15% waste", "Diagonal or offset layouts and rooms with many cuts"),
            ("20% waste", "Herringbone and complex patterns"),
        ],
        "materials": [
            ("Ceramic", "Walls and light-traffic floors; easy to cut"),
            ("Porcelain", "Floors and wet areas; denser and more water-resistant"),
            ("Natural stone", "Feature floors; needs sealing"),
            ("Mosaic", "Showers and small, shaped areas"),
        ],
        "tips": [
            "Buy all tiles in one order so the dye lots match.",
            "Open every box and mix them before laying to blend shade variation.",
            "Keep a few spares for future repairs.",
        ],
    },
    "grass_seed": {
        "tools": "a tape measure, a garden rake, a spreader for even coverage, and a hose or sprinkler",
        "unit_note": "Seed is sold by weight; a 3 lb bag covers about 660 sq ft at the new-lawn rate.",
        "depths": [
            ("2 lb / 1000 sq ft", "Overseeding an existing lawn"),
            ("4-5 lb / 1000 sq ft", "New lawn from bare soil"),
            ("5-6 lb / 1000 sq ft", "Worn areas and steep banks"),
        ],
        "materials": [
            ("Ryegrass", "Fast to establish, good for overseeding"),
            ("Fescue", "Shade-tolerant and drought-resistant"),
            ("Bluegrass", "Dense and hard-wearing, slower to germinate"),
            ("Clover blend", "Low-input lawns that fix nitrogen"),
        ],
        "tips": [
            "Sow in early autumn when the soil is warm and weeds are slowing.",
            "Keep the surface damp for the first two weeks, lightly and often.",
            "Do not bury the seed; it needs light and warmth to germinate.",
        ],
    },
    "concrete": {
        "tools": "a tape measure, a wheelbarrow, a mixing paddle or hoe, a float, an edging trowel, and a level",
        "unit_note": "An 80 lb bag yields about 0.6 cubic feet; a cubic yard needs roughly 45 of them.",
        "depths": [
            ("3 in", "Garden paths and light foot traffic"),
            ("4 in", "Patios, shed bases and standard slabs"),
            ("5-6 in", "Driveways and anything carrying vehicles"),
            ("6+ in", "Heavy loads; add reinforcement"),
        ],
        "materials": [
            ("Rapid-set mix", "Fence posts and small repairs"),
            ("Standard 80 lb mix", "Slabs and footings"),
            ("Fibre-reinforced", "Slabs where cracking is a concern"),
            ("Ready-mix delivery", "Anything over about one cubic yard"),
        ],
        "tips": [
            "Add water gradually; too much weakens the finished concrete.",
            "Compact and level a gravel base before pouring.",
            "Cure slowly by keeping it damp for the first few days.",
        ],
    },
}

FAQ_ORDER = ["mulch", "soil", "gravel", "paint", "tile", "grass_seed", "concrete"]

# Standard job sizes used to build a "coverage at a glance" table in each article.
# Values are input overrides for the calculator; anything omitted uses the default.
SCENARIOS: dict[str, list[tuple[str, dict]]] = {
    "mulch": [
        ("100 sq ft", {"length": 10, "width": 10}),
        ("200 sq ft", {"length": 20, "width": 10}),
        ("300 sq ft", {"length": 20, "width": 15}),
        ("500 sq ft", {"length": 25, "width": 20}),
        ("1,000 sq ft", {"length": 50, "width": 20}),
    ],
    "soil": [
        ("4x4 bed, 12 in deep", {"length": 4, "width": 4, "height": 12}),
        ("4x8 bed, 12 in deep", {"length": 8, "width": 4, "height": 12}),
        ("4x8 bed, 18 in deep", {"length": 8, "width": 4, "height": 18}),
        ("4x12 bed, 12 in deep", {"length": 12, "width": 4, "height": 12}),
    ],
    "gravel": [
        ("100 sq ft, 3 in deep", {"length": 10, "width": 10, "depth": 3}),
        ("200 sq ft, 3 in deep", {"length": 20, "width": 10, "depth": 3}),
        ("400 sq ft, 4 in deep", {"length": 20, "width": 20, "depth": 4}),
        ("600 sq ft, 4 in deep", {"length": 30, "width": 20, "depth": 4}),
    ],
    "paint": [
        ("10x10 room", {"length": 10, "width": 10}),
        ("12x12 room", {"length": 12, "width": 12}),
        ("15x15 room", {"length": 15, "width": 15}),
        ("20x15 room", {"length": 20, "width": 15}),
    ],
    "tile": [
        ("10x10 room", {"length": 10, "width": 10}),
        ("12x12 room", {"length": 12, "width": 12}),
        ("12x15 room", {"length": 15, "width": 12}),
        ("20x20 room", {"length": 20, "width": 20}),
    ],
    "grass_seed": [
        ("1,000 sq ft", {"area": 1000}),
        ("2,500 sq ft", {"area": 2500}),
        ("5,000 sq ft", {"area": 5000}),
        ("10,000 sq ft", {"area": 10000}),
    ],
    "concrete": [
        ("4x4 slab, 4 in", {"length": 4, "width": 4, "thickness": 4}),
        ("8x8 slab, 4 in", {"length": 8, "width": 8, "thickness": 4}),
        ("10x10 slab, 4 in", {"length": 10, "width": 10, "thickness": 4}),
        ("20x20 slab, 4 in", {"length": 20, "width": 20, "thickness": 4}),
    ],
}

# Which computed outputs to show, and their column headings, per calculator.
TABLE_COLUMNS: dict[str, list[tuple[str, str]]] = {
    "mulch": [("cubic_feet", "Cubic feet"), ("cubic_yards", "Cubic yards"),
              ("bags_2cf", "2 cu ft bags")],
    "soil": [("cubic_feet", "Cubic feet"), ("cubic_yards", "Cubic yards"),
             ("bags_1_5cf", "1.5 cu ft bags")],
    "gravel": [("cubic_yards", "Cubic yards"), ("tons", "Tons")],
    "paint": [("paintable_area", "Paintable sq ft"), ("gallons", "Gallons")],
    "tile": [("tiles", "Tiles"), ("tiles_with_waste", "With 10% waste")],
    "grass_seed": [("pounds", "Pounds"), ("bags_3lb", "3 lb bags")],
    "concrete": [("cubic_yards", "Cubic yards"), ("bags_60lb", "60 lb bags"),
                 ("bags_80lb", "80 lb bags")],
}


def size_table_md(calc_key: str) -> str:
    """Build a markdown table of results for standard job sizes."""
    import calculators
    scenarios = SCENARIOS.get(calc_key, [])
    cols = TABLE_COLUMNS.get(calc_key, [])
    if not scenarios or not cols:
        return ""
    header = "| Job size | " + " | ".join(h for _, h in cols) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    rows = []
    for label, overrides in scenarios:
        try:
            res = calculators.compute(calc_key, overrides)
        except Exception:
            continue
        cells = " | ".join(str(res.get(k, "-")) for k, _ in cols)
        rows.append(f"| {label} | {cells} |")
    return header + "\n" + sep + "\n" + "\n".join(rows)


def facts_block(calc_key: str) -> str:
    d = LIBRARY.get(calc_key)
    if not d:
        return ""
    lines = [f"Unit note: {d['unit_note']}", "", "Recommended depths / rates:"]
    for a, b in d["depths"]:
        lines.append(f"- {a}: {b}")
    lines += ["", "Material choices:"]
    for a, b in d["materials"]:
        lines.append(f"- {a}: {b}")
    lines += ["", "Practical tips:"]
    for t in d["tips"]:
        lines.append(f"- {t}")
    return "\n".join(lines)


def depth_table_md(calc_key: str) -> str:
    d = LIBRARY.get(calc_key)
    if not d:
        return ""
    head = "| Depth / rate | Best for |\n|---|---|"
    rows = "\n".join(f"| {a} | {b} |" for a, b in d["depths"])
    return head + "\n" + rows


def materials_md(calc_key: str) -> str:
    d = LIBRARY.get(calc_key)
    if not d:
        return ""
    head = "| Option | Why people choose it |\n|---|---|"
    rows = "\n".join(f"| {a} | {b} |" for a, b in d["materials"])
    return head + "\n" + rows


def tips(calc_key: str) -> list[str]:
    return LIBRARY.get(calc_key, {}).get("tips", [])


EXTRAS: dict[str, str] = {
    "mulch": """## Mulch and Soil Health

Mulch does more than tidy a bed. It moderates soil temperature, slows evaporation, and
breaks down into organic matter that feeds worms and soil life. That is why the depth
matters: a thin scatter looks neat but dries out and lets weeds through, while a layer
over four inches can hold so much moisture against stems that they rot.

Different materials behave differently. Shredded hardwood and pine bark last a season or
more and suit borders and trees. Straw is cheap, light and easy to spread, which makes it
the choice for vegetable beds where you will replant often. Compost is the odd one out: it
breaks down quickly and is better thought of as feeding the soil than as a long-term
surface cover, so use it thinly and top it up.

A simple schedule keeps beds looking good all year. In spring, top up to the two-to-three
inch band once the soil has warmed. Through summer, check after heavy rain, because
splash can expose bare soil. In autumn, a thin extra layer protects roots over winter.
Keep every layer a few inches clear of trunks and stems, and water the ground before you
spread rather than after.
""",
    "soil": """## Soil Volume, Weight and Delivery

Soil is sold two ways, and they are not interchangeable. Bagged mixes are measured by
volume, usually 1.5 or 2 cubic feet. Bulk topsoil and compost are sold by the cubic yard
or, sometimes, by weight. A cubic yard of damp topsoil weighs roughly a ton, so a pickup
load is often at its limit before the bed is full.

That gap between volume and weight is where most ordering mistakes happen. If you need
two cubic yards, that is about 54 cubic feet, or roughly 27 bags of the two-cubic-foot
size. Buying bulk is cheaper per unit once you pass about one cubic yard, but you need
somewhere to tip it and a way to move it to the bed.

Leave the mix to settle. A freshly filled bed drops by around a tenth of its volume over
the first season as air escapes and organic matter breaks down. Fill to within two inches
of the rim, water in stages as you go, and plan to top up each spring. Mixing your own
blend rather than buying a single bagged product usually works out cheaper and lets you
match the mix to what you are growing.
""",
    "gravel": """## Choosing the Right Stone

Not all gravel is the same, and the wrong choice shows up within a season. For a
decorative border or a light path, a rounded pea gravel or a small 10 mm stone looks well
and drains freely. For a driveway, you want an angular crushed stone that locks together
under a compactor; rounded stones roll and rut.

Depth and stone size go together. A 20 mm crushed stone at four inches compacted makes a
firm light driveway. For regular vehicle traffic, go to six inches in two layers, with the
coarser stone at the bottom and a finer layer on top. The sub-base is the part people
skip, and it is the part that decides whether the surface stays flat.

Edging matters too. Without a solid edge, angular stone spreads outward under wheels and
the depth thins at the edges first. A steel or timber edge set just above the finished
level holds the stone in place. Lay landscape fabric before the first layer on any path or
drive, so the stone does not sink into the soil and weeds do not push through.
""",
    "paint": """## Ceilings, Trim and Extra Rooms

Walls are only part of the job. If you are painting the ceiling, add its area to the total;
multiply the room's length by its width just as you did for the floor. A ceiling usually
takes one or two coats and, being flat and bright, hides less than walls do.

Trim, skirting, doors and window frames are measured in linear feet rather than square
feet, and they are painted separately. Budget roughly a gallon for every 100 to 150 linear
feet of trim, and remember that gloss and satin finishes cover differently from wall paint.
Doors are best taken off and painted flat to avoid runs.

When a project spans several rooms, work out each room's wall area, subtract its doors and
windows, then add the totals before you convert to gallons. Buying in one large tin is
cheaper per litre than several small ones, and it guarantees the same batch, so any
touch-up later matches exactly. Keep a labelled tin of each colour for repairs.
""",
    "tile": """## Layout Patterns and Offcuts

How you lay the tile changes how much you waste. A straight grid is the most economical,
so a 10 per cent allowance usually covers the cuts. A diagonal or diamond pattern turns
every edge into a triangle cut, and that pushes waste toward 15 per cent. Herringbone and
other patterned layouts waste more again.

Plan the layout from the centre of the room so the cut tiles at opposite walls are the
same width. That looks deliberate; starting from one corner leaves a full tile on one side
and a sliver on the other. Dry-lay a row before you fix anything, especially in a doorway
where the two rooms should meet on a full tile.

Grout lines add a small amount back. If you are working to an exact grid, add a couple of
millimetres per tile for the joint, which can change the tile count on a large floor. Buy
all the tile in one go so it comes from a single dye lot, keep a box in reserve for
breakages, and check the coverage printed on the box rather than counting tiles.
""",
    "grass_seed": """## Preparing the Ground and Aftercare

Seed fails more often from poor preparation than from the wrong rate. Rake the surface to
loosen the top inch, remove stones and old roots, and firm it so you leave a shallow
footprint when you walk across. Seed needs contact with soil, not a resting place on top
of it.

Sow at the rate for your method, then rake lightly so the seed is barely covered, and firm
again with the back of a rake. On a slope, scatter a thin layer of compost to hold it in
place, but keep the seed near the surface; buried seed will not sprout.

Watering is what decides the result. Keep the top inch damp for the first two weeks with
light, frequent watering rather than a single soak, which can wash seed into hollows. Once
the grass is up and has been cut twice, ease off and water more deeply and less often. Stay
off the new lawn until it is rooted, or the young plants pull straight out of the soil.
""",
    "concrete": """## Ready-Mix or Bags

For anything larger than about one cubic yard, ready-mix concrete delivered by truck is
easier and often cheaper than mixing bags by hand. The trade-off is that you must have the
area prepared and helpers ready before the truck arrives, because a pour cannot wait. Most
suppliers have a minimum load, so small jobs price badly.

Bagged mix suits small pours: fence post footings, steps, a small pad or a repair. Work
out the volume first, then divide by the yield printed on the bag, usually about 0.6 cubic
feet for an 80 lb bag. Mix only what you can place within about half an hour, and mix it
stiff rather than wet, because extra water is the main cause of weak concrete.

Whichever route you take, prepare the base properly. Compact the ground, add a gravel
sub-base for drainage, and form the edges so the slab is a true rectangle. Laying a sheet
of reinforcement mesh in the lower third of a slab that carries vehicles makes a real
difference to how long it lasts.
""",
}


def extra_section_md(calc_key: str) -> str:
    return EXTRAS.get(calc_key, "")
