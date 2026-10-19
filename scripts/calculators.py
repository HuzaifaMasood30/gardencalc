"""Real calculator engine. Every article ships a working tool with computed output.

Formulas are the standard industry rules of thumb used by suppliers (Home Depot,
Lowe's, landscape suppliers), so the results are genuinely useful, not filler.
"""
from __future__ import annotations

import math

# Density of common gravel/stone in tons per cubic yard.
GRAVEL_TONS_PER_CUYD = {
    "default": 1.4,      # ~3/4" crushed stone
    "pea_gravel": 1.35,
    "river_rock": 1.3,
    "decomposed_granite": 1.35,
}

# Density of damp builder's / masonry sand in tons per cubic yard. Sand is denser
# than 3/4" crushed stone, so a sand page cannot reuse the gravel constant.
SAND_TONS_PER_CUYD = 1.35


def _round(value: float, places: int = 2) -> float:
    return round(value + 1e-9, places)


def mulch(length_ft: float, width_ft: float, depth_in: float) -> dict:
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    return {
        "square_feet": _round(sqft, 1),
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuyd, 2),
        "bags_2cf": math.ceil(cuft / 2),  # 2 cu ft bags
    }


def soil(length_ft: float, width_ft: float, height_in: float) -> dict:
    cuft = length_ft * width_ft * (height_in / 12.0)
    return {
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuft / 27.0, 2),
        "bags_1_5cf": math.ceil(cuft / 1.5),
    }


def gravel(length_ft: float, width_ft: float, depth_in: float, kind: str = "default") -> dict:
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    tons = cuyd * GRAVEL_TONS_PER_CUYD.get(kind, GRAVEL_TONS_PER_CUYD["default"])
    return {
        "square_feet": _round(sqft, 1),
        "cubic_yards": _round(cuyd, 2),
        "tons": _round(tons, 2),
    }


def paint(length_ft: float, width_ft: float, height_ft: float, coats: int,
          doors: int = 1, windows: int = 2) -> dict:
    perimeter = 2 * (length_ft + width_ft)
    wall_area = perimeter * height_ft
    ceiling = length_ft * width_ft
    openings = doors * 21 + windows * 15  # sq ft of unpainted openings
    paintable = max(wall_area - openings, 0)
    total = (paintable * coats) + (ceiling * coats)
    # 1 gallon covers ~350 sq ft per coat
    gallons = total / 350.0
    return {
        "wall_area": _round(wall_area, 1),
        "paintable_area": _round(paintable, 1),
        "gallons": _round(gallons, 2),
    }


def tile(length_ft: float, width_ft: float, tile_w_in: float, tile_h_in: float,
         waste_pct: float) -> dict:
    floor_area = length_ft * width_ft
    tile_area = (tile_w_in / 12.0) * (tile_h_in / 12.0)
    tiles = floor_area / tile_area
    return {
        "floor_area": _round(floor_area, 1),
        "tile_area": _round(tile_area, 3),
        "tiles": math.ceil(tiles),
        "tiles_with_waste": math.ceil(tiles * (1 + waste_pct / 100.0)),
    }


def grass_seed(area_sqft: float, method: int) -> dict:
    # New lawn ~ 4-5 lb per 1000 sq ft; overseeding ~ 2 lb per 1000 sq ft.
    rate = 4.5 if int(method) == 1 else 2.0
    pounds = area_sqft / 1000.0 * rate
    return {
        "rate_per_1000": rate,
        "pounds": _round(pounds, 2),
        "bags_3lb": math.ceil(pounds / 3.0),
    }


def concrete(length_ft: float, width_ft: float, thickness_in: float) -> dict:
    cuft = length_ft * width_ft * (thickness_in / 12.0)
    cuyd = cuft / 27.0
    # 80 lb bag yields ~0.60 cu ft; 60 lb bag ~0.45 cu ft
    return {
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuyd, 2),
        "bags_60lb": math.ceil(cuft / 0.45),
        "bags_80lb": math.ceil(cuft / 0.60),
    }


def topsoil(length_ft: float, width_ft: float, depth_in: float) -> dict:
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    return {
        "square_feet": _round(sqft, 1),
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuyd, 2),
        "bags_40lb": math.ceil(cuft / 0.75),  # 40 lb bag ~= 0.75 cu ft
    }


def sand(length_ft: float, width_ft: float, depth_in: float) -> dict:
    """Builder's / paver sand, sold by the ton, cubic yard or 0.5 cu ft bag."""
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    return {
        "square_feet": _round(sqft, 1),
        "cubic_yards": _round(cuyd, 2),
        "tons": _round(cuyd * SAND_TONS_PER_CUYD, 2),
        "bags_0_5cf": math.ceil(cuft / 0.5),  # 0.5 cu ft bags
    }


def compost(length_ft: float, width_ft: float, depth_in: float) -> dict:
    """Compost / soil amendment, spread far shallower than mulch, in 1 cu ft bags."""
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    return {
        "square_feet": _round(sqft, 1),
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuyd, 2),
        "bags_1cf": math.ceil(cuft),  # 1 cu ft bags
    }


def bark(length_ft: float, width_ft: float, depth_in: float) -> dict:
    """Bark and wood chips, spread thicker than mulch and sold in 2 cu ft bags."""
    sqft = length_ft * width_ft
    cuft = sqft * (depth_in / 12.0)
    cuyd = cuft / 27.0
    return {
        "square_feet": _round(sqft, 1),
        "cubic_feet": _round(cuft, 1),
        "cubic_yards": _round(cuyd, 2),
        "bags_2cf": math.ceil(cuft / 2),  # 2 cu ft bags
    }


def sod(length_ft: float, width_ft: float, waste_pct: float) -> dict:
    """Sod is ordered by the roll (a common 10 sq ft) and by the pallet (~500 sq ft)."""
    sqft = length_ft * width_ft
    rolls = sqft / 10.0
    return {
        "square_feet": _round(sqft, 1),
        "rolls": math.ceil(rolls),
        "rolls_with_waste": math.ceil(rolls * (1 + waste_pct / 100.0)),
        "pallets": math.ceil(sqft / 500.0),
    }


def fertilizer(area_sqft: float, rate_per_1000: float, bag_lb: float,
               nitrogen_pct: float = 20.0) -> dict:
    """Product needed to deliver a target nitrogen rate.

    ``rate_per_1000`` is pounds of *actual nitrogen* per 1,000 sq ft. The product
    weight is that nitrogen divided by the bag's nitrogen fraction, so a 20-0-0
    bag needs twice the weight of a 10-10-10 bag for the same nitrogen.
    """
    pounds_nitrogen = area_sqft / 1000.0 * rate_per_1000
    share = (nitrogen_pct or 20.0) / 100.0
    pounds_product = pounds_nitrogen / share
    bag_lb = bag_lb or 40.0
    return {
        "pounds_nitrogen": _round(pounds_nitrogen, 2),
        "pounds": _round(pounds_product, 2),
        "bags": math.ceil(pounds_product / bag_lb),
    }


REGISTRY = {
    "mulch": mulch,
    "soil": soil,
    "gravel": gravel,
    "paint": paint,
    "tile": tile,
    "grass_seed": grass_seed,
    "concrete": concrete,
    "topsoil": topsoil,
    "fertilizer": fertilizer,
    "sand": sand,
    "compost": compost,
    "bark": bark,
    "sod": sod,
}


# --- Metric engine -------------------------------------------------------------------
# Inputs arrive in the *config* ids (length, width, depth, height, thickness, tile_w,
# tile_h, waste, area, rate, nitrogen, bag) but in metric units: linear dims in metres,
# small dims (depth/height/thickness/tile size) in centimetres, areas in square metres.
# Kept independent of the imperial functions above so neither system's rounding leaks
# into the other. Litres, kilograms and tonnes are the units a metric buyer orders in.

LITRES_PER_CUM = 1000.0
# 1 cu yd = 0.764555 m3, so 1.4 tons/cu yd == 1.8311 t/m3 of 3/4" crushed stone.
TONS_PER_CUM = GRAVEL_TONS_PER_CUYD["default"] / 0.764554857984
# A 350 sq ft/gallon US rate is 32.516 m2 per litre of paint.
SQM_PER_LITRE = 350.0 * 0.09290304 / 3.785411784
DOOR_SQM = 21 * 0.09290304   # 21 sq ft
WINDOW_SQM = 15 * 0.09290304  # 15 sq ft
CONCRETE_KG_PER_CUM = 2400.0  # cured concrete density, for bag yield


def _bags(volume_cum: float, bag_litres: float) -> int:
    return math.ceil(volume_cum * LITRES_PER_CUM / bag_litres)


def mulch_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "litres": _round(vol * LITRES_PER_CUM, 0),
        "bags_50l": _bags(vol, 50),
    }


def soil_m(length: float, width: float, height: float) -> dict:
    """length/width in metres, height in centimetres."""
    vol = length * width * (height / 100.0)
    return {
        "cubic_metres": _round(vol, 2),
        "litres": _round(vol * LITRES_PER_CUM, 0),
        "bags_50l": _bags(vol, 50),
    }


def gravel_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "tonnes": _round(vol * TONS_PER_CUM, 2),
    }


def paint_m(length: float, width: float, height: float, coats: int,
            doors: int = 1, windows: int = 2) -> dict:
    """All linear dims in metres."""
    wall = 2 * (length + width) * height
    ceiling = length * width
    openings = doors * DOOR_SQM + windows * WINDOW_SQM
    paintable = max(wall - openings, 0)
    total = (paintable * coats) + (ceiling * coats)
    return {
        "wall_area": _round(wall, 1),
        "paintable_area": _round(paintable, 1),
        "litres": _round(total / SQM_PER_LITRE, 1),
    }


def tile_m(length: float, width: float, tile_w: float, tile_h: float,
           waste: float) -> dict:
    """Room dims in metres, tile size in centimetres."""
    floor = length * width
    tile_area = (tile_w / 100.0) * (tile_h / 100.0)
    tiles = floor / tile_area
    return {
        "floor_area": _round(floor, 2),
        "tiles": math.ceil(tiles),
        "tiles_with_waste": math.ceil(tiles * (1 + waste / 100.0)),
    }


def grass_seed_m(area: float, method: int) -> dict:
    """area in square metres; rate in kilograms per 100 m2."""
    rate = 2.2 if int(method) == 1 else 1.0
    kg = area / 100.0 * rate
    return {
        "rate_per_100m2": rate,
        "kilograms": _round(kg, 2),
        "bags_1kg": math.ceil(kg),
    }


def concrete_m(length: float, width: float, thickness: float) -> dict:
    """length/width in metres, thickness in centimetres."""
    vol = length * width * (thickness / 100.0)
    return {
        "cubic_metres": _round(vol, 2),
        "bags_20kg": math.ceil(vol * CONCRETE_KG_PER_CUM / 20.0),
        "bags_25kg": math.ceil(vol * CONCRETE_KG_PER_CUM / 25.0),
    }


def topsoil_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "litres": _round(vol * LITRES_PER_CUM, 0),
        "bags_50l": _bags(vol, 50),
    }


def sand_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "tonnes": _round(vol * (SAND_TONS_PER_CUYD / 0.764554857984), 2),
    }


def compost_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "litres": _round(vol * LITRES_PER_CUM, 0),
        "bags_50l": _bags(vol, 50),
    }


def bark_m(length: float, width: float, depth: float) -> dict:
    """length/width in metres, depth in centimetres."""
    sqm = length * width
    vol = sqm * (depth / 100.0)
    return {
        "square_metres": _round(sqm, 1),
        "cubic_metres": _round(vol, 2),
        "litres": _round(vol * LITRES_PER_CUM, 0),
        "bags_50l": _bags(vol, 50),
    }


def sod_m(length: float, width: float, waste: float) -> dict:
    """length/width in metres; rolls of 1 sq m (a common metric sod roll)."""
    sqm = length * width
    rolls = sqm / 1.0
    return {
        "square_metres": _round(sqm, 1),
        "rolls": math.ceil(rolls),
        "rolls_with_waste": math.ceil(rolls * (1 + waste / 100.0)),
        "pallets": math.ceil(sqm / 50.0),
    }


def fertilizer_m(area: float, rate: float, bag: float,
                 nitrogen: float = 20.0) -> dict:
    """area in square metres; rate in kg of actual nitrogen per 100 m2."""
    kg_n = area / 100.0 * rate
    share = (nitrogen or 20.0) / 100.0
    kg_product = kg_n / share
    bag = bag or 20.0
    return {
        "kg_nitrogen": _round(kg_n, 2),
        "kilograms": _round(kg_product, 2),
        "bags": math.ceil(kg_product / bag),
    }


METRIC_REGISTRY = {
    "mulch": mulch_m,
    "soil": soil_m,
    "gravel": gravel_m,
    "paint": paint_m,
    "tile": tile_m,
    "grass_seed": grass_seed_m,
    "concrete": concrete_m,
    "topsoil": topsoil_m,
    "fertilizer": fertilizer_m,
    "sand": sand_m,
    "compost": compost_m,
    "bark": bark_m,
    "sod": sod_m,
}

# Config ids -> metric function keyword names. Metric functions take the config id
# spelling, so this is only needed where a config id is not a valid Python name or
# differs from the keyword; presently it is the identity map for every calculator.
METRIC_PARAM_MAP = {kind: {} for kind in METRIC_REGISTRY}

# Maps config input ids -> function keyword arguments.
PARAM_MAP = {
    "mulch": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "soil": {"length": "length_ft", "width": "width_ft", "height": "height_in"},
    "gravel": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "paint": {"length": "length_ft", "width": "width_ft", "height": "height_ft",
              "coats": "coats", "doors": "doors", "windows": "windows"},
    "tile": {"length": "length_ft", "width": "width_ft", "tile_w": "tile_w_in",
             "tile_h": "tile_h_in", "waste": "waste_pct"},
    "grass_seed": {"area": "area_sqft", "method": "method"},
    "concrete": {"length": "length_ft", "width": "width_ft", "thickness": "thickness_in"},
    "topsoil": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "fertilizer": {"area": "area_sqft", "rate": "rate_per_1000", "bag": "bag_lb",
                   "nitrogen": "nitrogen_pct"},
    "sand": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "compost": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "bark": {"length": "length_ft", "width": "width_ft", "depth": "depth_in"},
    "sod": {"length": "length_ft", "width": "width_ft", "waste": "waste_pct"},
}


def compute(kind: str, inputs: dict, units: str = "imperial") -> dict:
    """Compute ``kind`` for ``inputs`` in the given unit system.

    ``units="imperial"`` (the default, and what stored articles use) takes feet,
    inches, square feet and pounds. ``units="metric"`` takes metres, centimetres,
    square metres and kilograms and returns litres/tonnes. The default is imperial
    so every existing caller and every stored article keeps its current numbers.
    """
    if units == "metric":
        fn = METRIC_REGISTRY.get(kind)
        if not fn:
            raise KeyError(f"unknown calculator: {kind}")
        mapping = METRIC_PARAM_MAP.get(kind, {})
    else:
        fn = REGISTRY.get(kind)
        if not fn:
            raise KeyError(f"unknown calculator: {kind}")
        mapping = PARAM_MAP.get(kind, {})
    clean = {}
    for key, val in inputs.items():
        target = mapping.get(key, key)
        clean[target] = float(val) if isinstance(val, str) and _is_num(val) else val
    return fn(**clean)


def _is_num(v: str) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def worked_example(kind: str, inputs: dict) -> str:
    """Human-readable worked example for embedding in an article."""
    out = compute(kind, inputs)
    lines = [f"- Inputs: " + ", ".join(f"{k} = {v}" for k, v in inputs.items())]
    for k, v in out.items():
        lines.append(f"- {k.replace('_', ' ').title()}: **{v}**")
    return "\n".join(lines)


if __name__ == "__main__":
    import json
    import sys
    kind = sys.argv[1] if len(sys.argv) > 1 else "mulch"
    args = {}
    for pair in sys.argv[2:]:
        k, v = pair.split("=", 1)
        args[k] = float(v) if _is_num(v) else v
    print(json.dumps(compute(kind, args), indent=2))
