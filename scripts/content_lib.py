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
