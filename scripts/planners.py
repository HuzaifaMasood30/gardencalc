"""Project planner pages: multi-material shopping lists for common projects.

Each number is derived from scripts/calculators.py, so a planner can never disagree
with the individual calculator it builds on. Planners target broader "how do I plan a
<project>" searches and are the most shareable/citable pages on the site.
"""
from __future__ import annotations

import math

import calculators as C


def _r(x: float, p: int = 1) -> float:
    return round(x + 1e-9, p)


def _new_lawn() -> list[dict]:
    rows = []
    for area in (500, 1000, 2500, 5000, 10000):
        top = C.topsoil(area, 12, 1)  # 1 inch of topsoil dressing
        seed = C.grass_seed(area, 1)  # new lawn rate
        fert = C.fertilizer(area, 1.0, 40)  # 1 lb N per 1,000 sq ft
        rows.append([f"{area:,}", f"{top['cubic_yards']:.2f}", f"{top['bags_40lb']:,}",
                     f"{seed['pounds']:,.1f}", f"{seed['bags_3lb']:,}",
                     f"{fert['pounds']:,.1f}", f"{fert['bags']:,}"])
    return [{"headers": ["Lawn area (sq ft)", "Topsoil (cu yd)", "40 lb topsoil bags",
                         "Seed (lb)", "3 lb seed bags", "Starter fertilizer (lb)",
                         "40 lb fertilizer bags"], "rows": rows}]


def _raised_bed() -> list[dict]:
    rows = []
    for l, w in ((4, 4), (4, 8), (4, 12)):
        soil = C.soil(l, w, 12)
        mulch = C.mulch(l, w, 2)
        gravel = C.gravel(l, w, 2)
        rows.append([f"{l}x{w} ft", f"{soil['cubic_yards']:.2f}", f"{soil['bags_1_5cf']:,}",
                     f"{mulch['bags_2cf']:,}", f"{gravel['cubic_yards']:.2f}",
                     f"{gravel['tons']:.2f}"])
    return [{"headers": ["Bed size", "Soil (cu yd)", "1.5 cu ft soil bags", "Mulch bags (2 in)",
                         "Drainage gravel (cu yd)", "Gravel (tons)"], "rows": rows}]


def _patio_base() -> list[dict]:
    rows = []
    for l, w in ((8, 8), (10, 10), (10, 12), (12, 12), (12, 16)):
        area = l * w
        gravel = C.gravel(l, w, 4)          # 4 in compacted base
        sand_cuyd = area * (1 / 12.0) / 27  # 1 in bedding sand
        pavers = math.ceil(area / ((12 / 12.0) * (12 / 12.0)) * 1.10)  # 12x12 pavers, 10% waste
        rows.append([f"{l}x{w} ft", f"{area:,}", f"{gravel['cubic_yards']:.2f}",
                     f"{gravel['tons']:.2f}", f"{sand_cuyd:.2f}", f"{pavers:,}"])
    return [{"headers": ["Patio size", "Area (sq ft)", "Gravel base 4 in (cu yd)",
                         "Gravel (tons)", "Bedding sand 1 in (cu yd)",
                         "12x12 pavers + 10%"], "rows": rows}]


def _bed_makeover() -> list[dict]:
    rows = []
    for l, w in ((4, 4), (4, 8), (4, 12), (6, 6)):
        soil = C.soil(l, w, 2)   # 2 in soil top-up
        mulch = C.mulch(l, w, 3)  # 3 in mulch layer
        rows.append([f"{l}x{w} ft", f"{soil['cubic_feet']:.1f}", f"{soil['bags_1_5cf']:,}",
                     f"{mulch['cubic_feet']:.1f}", f"{mulch['cubic_yards']:.2f}",
                     f"{mulch['bags_2cf']:,}"])
    return [{"headers": ["Bed size", "Soil 2 in (cu ft)", "1.5 cu ft soil bags",
                         "Mulch 3 in (cu ft)", "Mulch (cu yd)", "Mulch bags (2 cu ft)"],
             "rows": rows}]


PLANNERS: list[dict] = [
    {
        "slug": "new-lawn-planner",
        "title": "New Lawn Planner: Topsoil, Seed & Fertilizer",
        "description": ("A shopping list for a new lawn: topsoil, grass seed and starter "
                        "fertilizer for 500-10,000 sq ft, with bags and cubic yards."),
        "question": "How much topsoil, seed and fertilizer do I need for a new lawn?",
        "cluster": "grass-seed",
        "calc": "grass-seed-calculator",
        "intro": ("Starting a lawn from scratch takes three materials: a thin topsoil dressing "
                  "to level and feed the seedbed, grass seed at the new-lawn rate, and a "
                  "starter fertilizer. This planner combines all three for common lawn sizes "
                  "so you can buy once. Rates are typical label figures - check your seed and "
                  "fertilizer bags, as species and products vary."),
        "formula": ("Topsoil volume = area (sq ft) x 1 in / 12. Seed = area / 1,000 x 4.5 lb. "
                    "Starter fertilizer = area / 1,000 x 1 lb of nitrogen."),
        "tables": _new_lawn,
        "faqs": [
            ("How much topsoil for a new lawn?",
             "A thin dressing of about 1 inch is enough to level and feed a seedbed. For 1,000 "
             "sq ft that is 83 cubic feet, about 3.1 cubic yards or 111 bags of 40 lb."),
            ("How much grass seed for a new lawn?",
             "New lawns take about 4 to 5 lb of seed per 1,000 sq ft. This planner uses 4.5 lb "
             "per 1,000 sq ft; follow your seed bag if it states a different rate."),
            ("Do I need starter fertilizer?",
             "Yes. A starter fertilizer high in phosphorus helps new roots. Apply about 1 lb of "
             "nitrogen per 1,000 sq ft at seeding and water it in."),
            ("What order do I apply everything?",
             "Spread topsoil and level it, seed evenly, then apply starter fertilizer and water "
             "gently. Keep the surface moist until the grass is established."),
        ],
    },
    {
        "slug": "raised-garden-bed-planner",
        "title": "Raised Garden Bed Planner: Soil, Mulch & Gravel",
        "description": ("A materials list for a raised bed: soil to fill it, mulch to top it "
                        "off and gravel for drainage, for 4x4, 4x8 and 4x12 beds."),
        "question": "How much soil, mulch and gravel does a raised garden bed need?",
        "cluster": "soil",
        "calc": "raised-bed-soil-calculator",
        "intro": ("Filling a raised bed is a volume job. Soil volume = length x width x depth, "
                  "and the same maths gives the mulch you top it with and the gravel you put "
                  "under the frame for drainage. The table assumes a bed filled to 12 inches, "
                  "topped with 2 inches of mulch and set on a 2 inch gravel drainage layer."),
        "formula": ("Volume (cu ft) = length (ft) x width (ft) x depth (in) / 12. "
                    "1 cubic yard = 27 cubic feet."),
        "tables": _raised_bed,
        "faqs": [
            ("How much soil for a 4x8 raised bed?",
             "At 12 inches deep a 4x8 ft bed holds 32 cubic feet, which is 1.19 cubic yards or "
             "22 bags of 1.5 cu ft."),
            ("Do raised beds really need gravel?",
             "On soil, a 2 inch gravel layer under the frame improves drainage and stops the "
             "soil washing out. On a hard surface, skip the gravel and use a weed membrane."),
            ("Should I fill the whole bed with bagged soil?",
             "For a deep bed, fill the bottom third with cheaper topsoil or compost and save the "
             "richer mix for the top. Roots feed mostly in the upper 8 to 10 inches."),
        ],
    },
    {
        "slug": "patio-base-planner",
        "title": "Patio Base Planner: Gravel, Sand & Paver Count",
        "description": ("Plan a paver patio base: 4 in of gravel, 1 in of bedding sand and the "
                        "number of 12x12 pavers for 8x8 to 12x16 ft patios."),
        "question": "How much gravel, sand and how many pavers does a patio need?",
        "cluster": "gravel",
        "calc": "gravel-calculator",
        "intro": ("A paver patio is built in layers: a compacted gravel base, a bedding layer of "
                  "sand, then the pavers. This planner uses the common depths of 4 inches of "
                  "gravel, 1 inch of sand and 12x12 inch pavers with a 10 percent cut allowance. "
                  "Gravel tonnage is a range because weight varies with the stone and moisture."),
        "formula": ("Gravel and sand volume (cu ft) = area (sq ft) x depth (in) / 12; "
                    "cu yd = cu ft / 27. Pavers = area / paver area x 1.10 waste."),
        "tables": _patio_base,
        "faqs": [
            ("How deep should a patio base be?",
             "For a foot-traffic patio, 4 inches of compacted gravel is the usual base, plus "
             "about 1 inch of sand for bedding the pavers."),
            ("How much sand goes under pavers?",
             "About 1 inch. More than that and the pavers can shift; less and they will not bed "
             "evenly. For 100 sq ft that is about 0.31 cubic yards."),
            ("How many pavers for a 10x10 patio?",
             "A 10x10 ft patio is 100 sq ft. With 12x12 pavers at 1 sq ft each and a 10 percent "
             "waste allowance, order about 110 pavers."),
        ],
    },
    {
        "slug": "garden-bed-makeover-planner",
        "title": "Garden Bed Makeover Planner: Soil & Mulch",
        "description": ("Refresh a tired bed: how much soil to top up and mulch to cover, in "
                        "bags, cubic feet and cubic yards for beds up to 6x6 ft."),
        "question": "How much soil and mulch do I need to refresh a garden bed?",
        "cluster": "mulch",
        "calc": "mulch-calculator",
        "intro": ("A bed makeover usually means topping up the soil and laying fresh mulch. This "
                  "planner uses a 2 inch soil top-up and a 3 inch mulch layer, the depths most "
                  "beds want. The same volume formula - area x depth - drives both, so you can "
                  "scale any row to your own bed size."),
        "formula": ("Volume (cu ft) = length (ft) x width (ft) x depth (in) / 12. "
                    "Mulch bags = cu ft / 2. Soil bags = cu ft / 1.5."),
        "tables": _bed_makeover,
        "faqs": [
            ("How much mulch for a 4x8 bed?",
             "A 4x8 ft bed at 3 inches deep needs 8 cubic feet of mulch, which is 4 bags of 2 cu "
             "ft, or 0.30 cubic yards."),
            ("Do I need to add soil every year?",
             "A 1 to 2 inch top-up of compost or soil each year replaces what plants use and "
             "what settles. More than that can bury stems."),
            ("Can I put mulch straight on top of the soil?",
             "Yes, but keep it a few inches clear of stems and trunks. Water first, then mulch, "
             "so the water soaks in rather than running off."),
        ],
    },
]


def page(planner: dict, base: str, site: dict) -> dict:
    calc_slug = planner.get("calc", "")
    return {
        "slug": planner["slug"],
        "title": planner["title"],
        "description": planner["description"],
        "question": planner["question"],
        "cluster": planner["cluster"],
        "intro": planner["intro"],
        "formula": planner["formula"],
        "tables": planner["tables"](),
        "faqs": [{"q": q, "a": a} for q, a in planner["faqs"]],
        "url": f"{base}/{planner['slug']}/",
        "calculator": f"{base}/{calc_slug}/" if calc_slug else "",
        "category": f"{base}/category/{planner['cluster']}/",
    }
