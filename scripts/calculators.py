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


REGISTRY = {
    "mulch": mulch,
    "soil": soil,
    "gravel": gravel,
    "paint": paint,
    "tile": tile,
    "grass_seed": grass_seed,
    "concrete": concrete,
}

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
}


def compute(kind: str, inputs: dict) -> dict:
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
