"""Linkable coverage-chart pages.

Every number here is derived from the same formulas as scripts/calculators.py, so a
chart can never disagree with the calculator it supports. Charts exist to capture many
long-tail "how much for <size>" searches on one strong page instead of many thin pages.
"""
from __future__ import annotations

import math
import re

import calculators as C

SQFT_LABEL = "sq ft"


def _rows(headers: list[str], rows: list[list]) -> dict:
    return {"headers": headers, "rows": rows}


def _mulch_tables() -> list[dict]:
    rows = []
    for area in (100, 200, 300, 400, 500, 600, 800, 1000):
        for depth in (2, 3, 4):
            cuft = area * depth / 12.0
            rows.append([f"{area:,}", f'{depth}"', f"{cuft:,.0f}",
                         f"{cuft / 27:.2f}", f"{math.ceil(cuft / 2):,}"])
    return [_rows(["Area (sq ft)", "Depth", "Cubic feet", "Cubic yards", "2 cu ft bags"], rows)]


def _concrete_tables() -> list[dict]:
    rows = []
    for l, w in ((4, 4), (8, 8), (10, 10), (10, 12), (12, 12), (20, 20)):
        for t in (4,):
            o = C.concrete(l, w, t)
            rows.append([f"{l}x{w}", f"{l * w:,}", f'{t}"', f"{o['cubic_feet']:,.1f}",
                         f"{o['cubic_yards']:.2f}", f"{math.ceil(o['cubic_feet'] / 0.30):,}",
                         f"{o['bags_60lb']:,}", f"{o['bags_80lb']:,}"])
    return [_rows(["Slab (ft)", "Area (sq ft)", "Thickness", "Cubic feet", "Cubic yards",
                   "40 lb bags", "60 lb bags", "80 lb bags"], rows)]


def _soil_tables() -> list[dict]:
    rows = []
    for l, w in ((4, 4), (4, 8), (4, 12), (8, 8), (3, 6), (2, 8)):
        for h in (6, 8, 10, 12):
            o = C.soil(l, w, h)
            rows.append([f"{l}x{w} ft", f'{h}"', f"{o['cubic_feet']:,.1f}",
                         f"{o['cubic_yards']:.2f}", f"{o['bags_1_5cf']:,}"])
    return [_rows(["Raised bed", "Fill depth", "Cubic feet", "Cubic yards",
                   "1.5 cu ft bags"], rows)]


def _gravel_tables() -> list[dict]:
    rows = []
    for area in (100, 200, 500, 1000):
        for depth in (2, 3, 4):
            cuft = area * depth / 12.0
            cuyd = cuft / 27.0
            rows.append([f"{area:,}", f'{depth}"', f"{cuyd:.2f}",
                         f"{cuyd * 1.2:.1f}", f"{cuyd * 1.5:.1f}"])
    return [_rows(["Area (sq ft)", "Depth", "Cubic yards", "Tons (light ~1.2 t/yd³)",
                   "Tons (heavy ~1.5 t/yd³)"], rows)]


def _paint_tables() -> list[dict]:
    rows = []
    for l, w in ((10, 10), (12, 12), (12, 16), (15, 20), (20, 20)):
        for coats in (1, 2):
            o = C.paint(l, w, 8, coats, doors=1, windows=2)
            rows.append([f"{l}x{w} ft", "8 ft", str(coats), f"{o['paintable_area']:,.0f}",
                         f"{o['gallons']:.2f}", f"{math.ceil(o['gallons'])}"])
    return [_rows(["Room", "Ceiling height", "Coats", "Paintable walls (sq ft)",
                   "Gallons needed", "Buy (gallons)"], rows)]


def _tile_tables() -> list[dict]:
    rows = []
    for l, w in ((10, 10), (12, 12), (10, 12), (20, 20)):
        for tw, th in ((12, 12), (18, 18), (12, 24)):
            o = C.tile(l, w, tw, th, 10)
            rows.append([f"{l}x{w} ft", f'{tw}x{th}"', f"{o['tiles']:,}",
                         f"{o['tiles_with_waste']:,}"])
    return [_rows(["Room", "Tile size", "Tiles (no waste)", "Tiles + 10% waste"], rows)]


def _seed_tables() -> list[dict]:
    rows = []
    for area in (1000, 2000, 5000, 10000):
        new = C.grass_seed(area, 1)
        over = C.grass_seed(area, 0)
        rows.append([f"{area:,}", f"{new['pounds']:,.1f}", f"{new['bags_3lb']:,}",
                     f"{over['pounds']:,.1f}", f"{over['bags_3lb']:,}"])
    return [_rows(["Lawn area (sq ft)", "New lawn seed (lb)", "3 lb bags",
                   "Overseeding (lb)", "3 lb bags"], rows)]


def _fertilizer_tables() -> list[dict]:
    rows = []
    for area in (1000, 2500, 5000, 10000):
        for rate in (0.5, 1.0):
            o = C.fertilizer(area, rate, 40)
            rows.append([f"{area:,}", f"{rate}", f"{o['pounds']:,.1f}", f"{o['bags']:,}"])
    return [_rows(["Lawn area (sq ft)", "lbs N per 1,000 sq ft", "Fertilizer (lb)",
                   "40 lb bags"], rows)]


CHARTS: list[dict] = [
    {
        "slug": "mulch-coverage-chart",
        "title": "Mulch Coverage Chart: Bags & Yards by Area and Depth",
        "description": ("How much mulch you need by area and depth: cubic feet, cubic yards "
                        "and 2 cu ft bags for 100-1,000 sq ft at 2, 3 and 4 inches deep."),
        "keyword": "mulch coverage chart",
        "cluster": "mulch",
        "calc": "mulch-calculator",
        "intro": ("Use this chart to order mulch without guessing. Pick your bed area down the "
                  "left and the depth you want across the middle, and read off cubic feet, "
                  "cubic yards and the number of 2 cu ft bags. Three inches is the usual depth "
                  "for beds; go to four inches only where you are smothering weeds."),
        "tables": _mulch_tables,
        "faqs": [
            ("How many bags of mulch are in a cubic yard?",
             "A cubic yard is 27 cubic feet, so it fills 13.5 two-cubic-foot bags. Most stores "
             "sell 2 cu ft bags, so a cubic yard is about 13 to 14 bags."),
            ("How much mulch for 500 sq ft at 3 inches?",
             "500 sq ft at 3 in deep needs 125 cubic feet, which is 4.63 cubic yards or 63 "
             "two-cubic-foot bags."),
            ("What depth of mulch should I use?",
             "Two to three inches is right for most beds. Four inches helps suppress weeds but "
             "keep it a few inches away from stems and trunks so the plants can breathe."),
        ],
    },
    {
        "slug": "concrete-bags-by-slab-size-chart",
        "title": "Concrete Bags by Slab Size Chart (40, 60 & 80 lb)",
        "description": ("Bags of concrete for common slab sizes at 4 in thick: 4x4 to 20x20 ft, "
                        "with cubic feet, yards and 40, 60 and 80 lb bag counts."),
        "keyword": "concrete bags per slab size",
        "cluster": "concrete",
        "calc": "concrete-calculator",
        "intro": ("Ready-mix is sold by the cubic yard from a truck, but small slabs are poured "
                  "from bags. For a slab, volume = length x width x thickness, and one 80 lb bag "
                  "yields about 0.60 cu ft, a 60 lb bag about 0.45 cu ft, and a 40 lb bag about "
                  "0.30 cu ft. The table assumes a 4 in slab, the most common patio and shed "
                  "thickness."),
        "tables": _concrete_tables,
        "faqs": [
            ("How many 80 lb bags of concrete for a 10x10 slab?",
             "A 10x10 ft slab at 4 in thick is 33.3 cubic feet. At 0.60 cu ft per 80 lb bag that "
             "is about 56 bags."),
            ("How many cubic feet is an 80 lb bag of concrete?",
             "About 0.60 cubic feet. A 60 lb bag is about 0.45 cu ft and a 40 lb bag about "
             "0.30 cu ft."),
            ("How many bags of concrete for a 10x12 slab?",
             "A 10x12 ft slab at 4 in is 40 cubic feet, which is about 67 bags of 80 lb or 89 "
             "bags of 60 lb."),
        ],
    },
    {
        "slug": "raised-bed-soil-chart",
        "title": "Raised Bed Soil Chart: Bags & Yards by Bed Size",
        "description": ("Soil needed for raised beds from 4x4 to 4x12 ft at 6 to 12 in deep, in "
                        "cubic feet, cubic yards and 1.5 cu ft bags."),
        "keyword": "raised bed soil chart",
        "cluster": "soil",
        "calc": "raised-bed-soil-calculator",
        "intro": ("Raised beds are measured by the volume they hold, not the area they cover. "
                  "Volume = length x width x fill depth, all in feet. Most beds are filled to "
                  "about 10 to 12 inches for vegetables, and less if you are topping up an "
                  "established bed. A 1.5 cu ft bag is the common bagged-soil size."),
        "tables": _soil_tables,
        "faqs": [
            ("How much soil for a 4x8 raised bed?",
             "A 4x8 ft bed 12 in deep holds 32 cubic feet, which is 1.19 cubic yards or 22 "
             "bags of 1.5 cu ft."),
            ("How many bags of soil for a 4x4 raised bed?",
             "At 12 in deep a 4x4 bed needs 16 cubic feet, or 11 bags of 1.5 cu ft. At 10 in it "
             "needs 13.3 cu ft, or 9 bags."),
            ("Should I fill a raised bed with topsoil or a soil mix?",
             "Use a blend of topsoil, compost and a little aged manure. Straight topsoil can "
             "compact and lacks the organic matter vegetables want."),
        ],
    },
    {
        "slug": "gravel-coverage-chart",
        "title": "Gravel Coverage Chart: Yards & Tons by Area and Depth",
        "description": ("Gravel needed by area and depth in cubic yards and tons, with light "
                        "(1.2 t/yd³) and heavy (1.5 t/yd³) weight ranges."),
        "keyword": "gravel coverage chart",
        "cluster": "gravel",
        "calc": "gravel-calculator",
        "intro": ("Gravel is ordered by the cubic yard or by the ton. Volume = area x depth. "
                  "Weight depends on the stone and how wet it is, so treat tonnage as a range: "
                  "about 1.2 to 1.5 tons per cubic yard for common crushed stone. For driveways "
                  "use 4 inches of compacted base; for paths 2 to 3 inches is usually enough."),
        "tables": _gravel_tables,
        "faqs": [
            ("How many tons of gravel in a cubic yard?",
             "About 1.2 to 1.5 tons per cubic yard for common crushed stone, depending on the "
             "rock type and moisture. The supplier's figure is the one to order against."),
            ("How much gravel for a driveway?",
             "A typical single-car driveway about 12 ft wide and 40 ft long at 4 in deep needs "
             "about 11.9 cubic yards, or roughly 14 to 18 tons."),
            ("How deep should a gravel path be?",
             "Two to three inches of gravel over a weed membrane is enough for a garden path. "
             "Driveways need about four inches of compacted base."),
        ],
    },
    {
        "slug": "paint-coverage-chart",
        "title": "Paint Coverage Chart: Gallons per Room, 1 or 2 Coats",
        "description": ("Gallons of paint per room size for one and two coats at about 350 sq ft "
                        "per gallon, deducting a door and two windows."),
        "keyword": "paint coverage chart",
        "cluster": "paint",
        "calc": "paint-calculator",
        "intro": ("One gallon of wall paint covers about 350 sq ft per coat, but paintability is "
                  "the key word: subtract about 21 sq ft per door and 15 sq ft per window. The "
                  "chart uses an 8 ft ceiling, one door and two windows, and shows both a single "
                  "coat and two coats. Always buy a little extra for touch-ups."),
        "tables": _paint_tables,
        "faqs": [
            ("How much paint for a 12x12 room?",
             "A 12x12 ft room with an 8 ft ceiling, one door and two windows has about 311 sq ft "
             "of paintable wall. Two coats need about 1.78 gallons, so buy two gallons."),
            ("How many square feet does a gallon of paint cover?",
             "About 350 square feet per coat on a smooth, sealed wall. Rough or bare surfaces "
             "soak up more, so plan on less coverage."),
            ("Do I need to paint the ceiling too?",
             "The chart counts walls only. A ceiling adds its own area, so add that separately if "
             "you are painting it."),
        ],
    },
    {
        "slug": "tile-quantity-chart",
        "title": "Tile Quantity Chart: How Many Tiles by Room and Size",
        "description": ("How many tiles for common rooms and tile sizes, with a 10% waste "
                        "allowance for cuts and breakage built in."),
        "keyword": "tile quantity chart",
        "cluster": "tile",
        "calc": "tile-calculator",
        "intro": ("Tile count is the floor area divided by the area of one tile, plus a waste "
                  "allowance. Ten percent is the usual rule for straight lay; go to 15 percent "
                  "for diagonal or herringbone patterns and for rooms with lots of cuts. Kitchen "
                  "and bathroom floors mean many cuts, so treat the higher figure as normal."),
        "tables": _tile_tables,
        "faqs": [
            ("How many 12x12 tiles for a 10x10 room?",
             "A 10x10 ft floor is 100 sq ft. Each 12x12 in tile is 1 sq ft, so you need 100 "
             "tiles, or 110 with a 10% waste allowance."),
            ("How much waste should I add for tile?",
             "About 10 percent for a straight lay and 15 percent for diagonal or patterned "
             "layouts, plus more for rooms with many cuts."),
            ("How many tiles in a box?",
             "It varies by tile. Check the box for the square feet it covers, then divide your "
             "room area by that number and round up."),
        ],
    },
    {
        "slug": "grass-seed-rate-chart",
        "title": "Grass Seed Rate Chart: Pounds per 1,000 Sq Ft",
        "description": ("Pounds of grass seed for lawns of 1,000 to 10,000 sq ft for new lawns "
                        "and overseeding, with 3 lb bag counts."),
        "keyword": "grass seed rate chart",
        "cluster": "grass-seed",
        "calc": "grass-seed-calculator",
        "intro": ("Seed is applied by weight per 1,000 sq ft, and the rate depends on the job. A "
                  "new lawn takes about 4 to 5 lb per 1,000 sq ft; overseeding an existing lawn "
                  "takes about 2 lb. Always check the label on your seed, because rates differ "
                  "by species. These figures are typical labels, not guarantees."),
        "tables": _seed_tables,
        "faqs": [
            ("How much grass seed per 1,000 sq ft?",
             "About 4 to 5 lb for a new lawn and about 2 lb for overseeding. Follow the seeding "
             "rate on your seed bag, as species vary."),
            ("How much grass seed for 5,000 sq ft?",
             "A new lawn needs about 22.5 lb and overseeding about 10 lb for 5,000 sq ft at the "
             "rates above."),
            ("Does overseeding need less seed?",
             "Yes. Overseeding only thickens an existing lawn, so it uses roughly half the seed "
             "of a full new-lawn seeding."),
        ],
    },
    {
        "slug": "fertilizer-rate-chart",
        "title": "Fertilizer Rate Chart: Pounds of Fertilizer per 1,000 Sq Ft",
        "description": ("Fertilizer needed for lawns of 1,000 to 10,000 sq ft at 0.5 and 1.0 lb "
                        "of nitrogen per 1,000 sq ft, with 40 lb bag counts."),
        "keyword": "fertilizer rate chart",
        "cluster": "fertilizer",
        "calc": "fertilizer-calculator",
        "intro": ("Fertilizer is dosed by nitrogen per 1,000 sq ft. A light feeding is about "
                  "0.5 lb and a standard feeding about 1 lb of nitrogen per 1,000 sq ft. A 40 lb "
                  "bag is the common size. The pounds below are the product weight to apply at "
                  "the stated nitrogen rate; divide by the nitrogen percentage on the bag if it "
                  "is not a straight 1:1 product."),
        "tables": _fertilizer_tables,
        "faqs": [
            ("How much fertilizer per 1,000 sq ft?",
             "Aim for about 0.5 to 1 lb of nitrogen per 1,000 sq ft per feeding. Spread it "
             "evenly and water it in."),
            ("How many bags of fertilizer for 5,000 sq ft?",
             "At 1 lb of nitrogen per 1,000 sq ft and a 40 lb bag, 5,000 sq ft needs about 5 lb "
             "of nitrogen, or roughly one 40 lb bag for a light feeding."),
            ("When should I fertilize a lawn?",
             "Feed in early spring and again in early autumn for cool-season grass. Avoid heavy "
             "summer feeding, which can burn the lawn."),
        ],
    },
]


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


# The direct question each chart answers, used in the answer-first block for snippets.
CHART_QUESTIONS = {
    "mulch-coverage-chart": "How much mulch do I need?",
    "concrete-bags-by-slab-size-chart": "How many bags of concrete do I need?",
    "raised-bed-soil-chart": "How much soil does a raised bed need?",
    "gravel-coverage-chart": "How much gravel do I need?",
    "paint-coverage-chart": "How much paint do I need?",
    "tile-quantity-chart": "How many tiles do I need?",
    "grass-seed-rate-chart": "How much grass seed do I need?",
    "fertilizer-rate-chart": "How much fertilizer does my lawn need?",
}


def page(chart: dict, base: str, site: dict) -> dict:
    """Build the render context for one chart page."""
    url = f"{base}/{chart['slug']}/"
    calc_slug = chart.get("calc", "")
    tables = chart["tables"]()
    # Jump links: one anchor per distinct first-column value (the size/area), so
    # Google can surface deep links and readers can skip to their row. Only the first
    # row for each label gets the id, so ids never repeat.
    anchors = []
    seen: set[str] = set()
    for tbl in tables:
        ids = []
        for row in tbl["rows"]:
            label = str(row[0])
            rid = _slugify(label)
            if rid and rid not in seen:
                seen.add(rid)
                ids.append(rid)
                anchors.append({"label": label, "id": rid})
            else:
                ids.append("")
        tbl["ids"] = ids
    related = {
        "calculator": f"{base}/{calc_slug}/" if calc_slug else "",
        "category": f"{base}/category/{chart['cluster']}/",
    }
    return {
        "slug": chart["slug"],
        "title": chart["title"],
        "description": chart["description"],
        "keyword": chart["keyword"],
        "cluster": chart["cluster"],
        "question": CHART_QUESTIONS.get(chart["slug"], chart["title"]),
        "intro": chart["intro"],
        "tables": tables,
        "anchors": anchors,
        "faqs": [{"q": q, "a": a} for q, a in chart["faqs"]],
        "url": url,
        "related": related,
    }
