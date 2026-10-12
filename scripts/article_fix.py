"""Deterministic content repair for guide pages.

The calculators are the single source of truth. This module makes the prose,
tables and the answer box agree with ``calculators.py`` instead of trusting the
numbers an LLM typed:

* headline dimensions come from the page's own keyword (so "600 square feet"
  becomes a round 20 x 30 ft bed, not 24.5 x 24.5),
* the intro's numeric claim is replaced with a computed short answer,
* the "Worked Example" bullet block is regenerated from the computed output,
* every standard size-table row is recomputed so bags = ceil(cubic feet / bag
  size) and cubic yards = round(cubic feet / 27, 2),
* the answer box gets a page-specific answer rather than the first FAQ answer.

Pages whose query the box-shaped calculator cannot model (a post hole, a door,
a whole-house exterior, a metric area, a trench) keep their hand-written intro,
which is the accurate answer; only the answer box is filled from it.

Run directly to repair ``data/articles.json`` in place.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calculators  # noqa: E402

BAG_SIZE = {"1.5": 1.5, "2": 2.0, "60 lb": 0.45, "80 lb": 0.60, "40": 0.75, "3 lb": 3.0}

# The box-shaped calculator cannot model these queries, so the hand-written intro
# is the accurate answer: leave the prose alone, use it only for the answer box.
SPECIAL_SLUGS = {
    "how-many-bags-of-concrete-do-i-need-for-a-fence-post",
    "how-much-gravel-do-i-need-for-a-french-drain",
    "how-much-gravel-do-i-need-for-a-backfill-retaining-wall",
    "how-much-gravel-do-i-need-per-square-metre",
    "how-much-paint-do-i-need-for-a-front-door",
    "how-much-paint-do-i-need-for-1800-sq-ft-house",
    "how-much-paint-do-i-need-for-a-12x16-shed",
    "how-much-paint-do-i-need-for-a-small-bathroom",
}


def _first_sentence(text: str) -> str:
    text = " ".join((text or "").split())
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def _answer_sentence(text: str) -> str:
    """First sentence that carries a figure, so the answer box gives a number."""
    text = " ".join((text or "").split())
    sentences = re.findall(r"[^.!?]+[.!?]", text)
    for s in sentences:
        if re.search(r"\d", s):
            return s.strip()
    return _first_sentence(text)


def _num(text: str) -> float | None:
    m = re.search(r"([\d.,]+)", text.replace(",", ""))
    return float(m.group(1).rstrip(".")) if m else None


def _g(x) -> str:
    return f"{x:g}" if isinstance(x, float) else str(x)


def nice_pair(area: float) -> tuple[int, int]:
    """Round length x width for an area, preferring familiar sizes."""
    a = int(round(area))
    for w in (20, 25, 30, 15, 10, 40, 50, 4, 5, 6, 8, 12):
        if a % w == 0:
            l = a // w
            if l >= w and l / w <= 4 and l <= 200:
                return l, w
    s = math.isqrt(a)
    return s, (a // s if a % s == 0 else s)


def _kw_dims(kw: str):
    """(l, w) from '20x30' or '600 square feet', or None."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)", kw)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return (max(a, b), min(a, b))
    m = re.search(r"([\d,]+)\s*(?:sq\.?\s*ft|square feet|square foot)", kw)
    if m:
        return nice_pair(float(m.group(1).replace(",", "")))
    return None


def headline_inputs(art: dict) -> dict:
    """Calculator inputs matching the page's keyword, with round dimensions."""
    key = art.get("calculator") or ""
    kw = (art.get("primary_keyword") or "").lower()
    base = dict(art.get("calculator_defaults") or {})
    dims = _kw_dims(kw)
    d3 = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)", kw)
    area = re.search(r"([\d,]+)\s*(?:sq\.?\s*ft|square feet|square foot)", kw)

    if key in ("mulch", "gravel", "topsoil"):
        depth = 4 if "driveway" in kw else base.get("depth", 3)
        if dims:
            return {**base, "length": dims[0], "width": dims[1], "depth": depth}
        return base
    if key == "soil":
        if d3:
            l, w, h = (float(d3.group(i)) for i in (1, 2, 3))
            return {**base, "length": max(l, w), "width": min(l, w),
                    "height": h * 12 if h <= 3 else h}
        if dims:
            return {**base, "length": dims[0], "width": dims[1], "height": base.get("height", 12)}
        return base
    if key == "concrete":
        if dims:
            return {**base, "length": dims[0], "width": dims[1],
                    "thickness": base.get("thickness", 4)}
        return base
    if key == "paint":
        if dims:
            return {**base, "length": dims[0], "width": dims[1], "height": base.get("height", 8)}
        return base
    if key == "tile":
        if dims:
            return {**base, "length": dims[0], "width": dims[1],
                    "tile_w": base.get("tile_w", 12), "tile_h": base.get("tile_h", 12),
                    "waste": base.get("waste", 10)}
        return base
    if key == "grass_seed":
        method = 2 if "overseed" in kw else base.get("method", 1)
        if area:
            return {**base, "area": float(area.group(1).replace(",", "")), "method": method}
        if "1000" in kw or "per square foot" in kw:
            return {**base, "area": 1000, "method": method}
        return base
    if key == "fertilizer":
        out = dict(base)
        out["nitrogen"] = _nitrogen_from_keyword(kw)
        if art.get("is_pillar"):
            return out
        if area:
            out["area"] = float(area.group(1).replace(",", ""))
        elif "1000" in kw or "per square foot" in kw:
            out["area"] = 1000
        return out
    return base


def _nitrogen_from_keyword(kw: str) -> float:
    """Nitrogen percentage implied by the page's keyword.

    "10-10-10" -> 10, "20-0-0" -> 20, otherwise the common 20% starter/lawn bag.
    """
    m = re.search(r"\b(\d{1,2})[-\s](\d{1,2})[-\s](\d{1,2})\b", kw)
    if m:
        return float(m.group(1))
    return 20.0


def describe(art: dict, inputs: dict) -> str:
    """Human phrase for the job size, e.g. '600 sq ft at 3 in'."""
    key = art.get("calculator") or ""
    kw = (art.get("primary_keyword") or "").lower()
    area = re.search(r"([\d,]+)\s*(?:sq\.?\s*ft|square feet|square foot)", kw)
    if key in ("mulch", "gravel", "topsoil"):
        depth = _g(inputs.get("depth", 3))
        if area:
            return f"{int(area.group(1).replace(',', ''))} sq ft at {depth} in"
        return f"{_g(inputs.get('length'))}x{_g(inputs.get('width'))} ft at {depth} in"
    if key == "soil":
        return f"{_g(inputs.get('length'))}x{_g(inputs.get('width'))} ft bed at {_g(inputs.get('height'))} in"
    if key == "concrete":
        return f"{_g(inputs.get('length'))}x{_g(inputs.get('width'))} ft slab at {_g(inputs.get('thickness'))} in"
    if key == "paint":
        return f"{_g(inputs.get('length'))}x{_g(inputs.get('width'))} ft room, 2 coats"
    if key == "tile":
        return f"{_g(inputs.get('length'))}x{_g(inputs.get('width'))} ft with 12 in tiles"
    if key == "grass_seed":
        return f"{int(inputs.get('area', 0)):,} sq ft"
    if key == "fertilizer":
        return (f"{int(inputs.get('area', 0)):,} sq ft at "
                f"{_g(inputs.get('rate', 1))} lb N per 1,000 sq ft")
    return "this job"


def answer_text(art: dict) -> str:
    """A direct answer to the page's own query, computed from the calculator."""
    if art["slug"] in SPECIAL_SLUGS:
        return _answer_sentence(_intro_paragraph(art))
    key = art.get("calculator") or ""
    ins = headline_inputs(art)
    out = calculators.compute(key, ins)
    where = describe(art, ins)
    if key == "mulch":
        return (f"{where} needs {_g(out['cubic_feet'])} cu ft of mulch: "
                f"{out['cubic_yards']} cu yd, or {out['bags_2cf']} two-cu-ft bags.")
    if key == "topsoil":
        return (f"{where} needs {_g(out['cubic_feet'])} cu ft of topsoil: "
                f"{out['cubic_yards']} cu yd, or {out['bags_40lb']} 40-lb bags.")
    if key == "soil":
        return (f"{where} needs {_g(out['cubic_feet'])} cu ft of soil: "
                f"{out['cubic_yards']} cu yd, or {out['bags_1_5cf']} 1.5-cu-ft bags.")
    if key == "gravel":
        return f"{where} needs {out['cubic_yards']} cu yd of gravel, about {out['tons']} tons."
    if key == "concrete":
        return (f"{where} needs {_g(out['cubic_feet'])} cu ft of concrete: about "
                f"{out['bags_80lb']} bags of 80 lb or {out['bags_60lb']} bags of 60 lb.")
    if key == "paint":
        return f"{where} needs about {out['gallons']} gallons of paint."
    if key == "tile":
        return f"{where} needs about {out['tiles_with_waste']} tiles ({out['tiles']} plus 10% waste)."
    if key == "grass_seed":
        return (f"{where} needs about {_g(out['pounds'])} lb of seed "
                f"({out['bags_3lb']} x 3-lb bags) at {_g(out['rate_per_1000'])} lb per 1,000 sq ft.")
    if key == "fertilizer":
        share = _g(ins.get("nitrogen", 20))
        return (f"{where} needs {_g(out['pounds_nitrogen'])} lb of actual nitrogen, "
                f"about {_g(out['pounds'])} lb of product ({out['bags']} bag) "
                f"from a {share}% nitrogen bag.")
    return art.get("meta_description", "")


def _intro_paragraph(art: dict) -> str:
    return art["body_markdown"].split("\n")[_intro_index(
        art.get("body_markdown", "").split("\n")) or 0] or art.get("meta_description", "")


def _intro_index(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s[0] in "#|->":
            continue
        # A bullet ("* x") is not the intro, but a bold lead sentence ("**x**")
        # is: only skip "*" when it is not the start of "**".
        if s[0] == "*" and not s.startswith("**"):
            continue
        # Skip numbered-list items ("1. Area: ...") but not answers that merely
        # start with a figure ("10x10 ft slab at 4 in needs ...").
        if re.match(r"\d+[.)]\s", s):
            continue
        return i
    return None


_NUMERIC_CLAIM = re.compile(
    r"\b(cubic (?:feet|foot|yards?|yard)|bags?|tons?|gallons?|tiles?|pounds?)\b", re.I)


def fix_intro(md: str, art: dict) -> tuple[str, str | None]:
    if art["slug"] in SPECIAL_SLUGS:
        return md, None
    lines = md.split("\n")
    idx = _intro_index(lines)
    if idx is None or not _NUMERIC_CLAIM.search(lines[idx]):
        return md, None
    new = answer_text(art)
    if lines[idx].strip() == new:
        return md, None
    old = lines[idx].strip()
    lines[idx] = new
    return "\n".join(lines), f"intro: {old[:64]!r} -> {new[:64]!r}"


_FIELD = {
    "Square feet": "square_feet", "Cubic feet": "cubic_feet", "Cubic yards": "cubic_yards",
    "2 cu ft bags": "bags_2cf", "40 lb bags": "bags_40lb", "1.5 cu ft bags": "bags_1_5cf",
    "Tons": "tons", "60 lb bags": "bags_60lb", "80 lb bags": "bags_80lb",
    "Wall area": "wall_area", "Paintable area": "paintable_area", "Gallons": "gallons",
    "Floor area": "floor_area", "Tile area": "tile_area", "Tiles": "tiles",
    "Tiles with waste": "tiles_with_waste", "Rate per 1000": "rate_per_1000",
    "Pounds": "pounds", "3 lb bags": "bags_3lb", "Bags": "bags",
    "Pounds of nitrogen": "pounds_nitrogen", "Pounds of product": "pounds",
}
_LABELS = {
    "mulch": ["Square feet", "Cubic feet", "Cubic yards", "2 cu ft bags"],
    "topsoil": ["Square feet", "Cubic feet", "Cubic yards", "40 lb bags"],
    "soil": ["Cubic feet", "Cubic yards", "1.5 cu ft bags"],
    "gravel": ["Square feet", "Cubic yards", "Tons"],
    "concrete": ["Cubic feet", "Cubic yards", "60 lb bags", "80 lb bags"],
    "paint": ["Wall area", "Paintable area", "Gallons"],
    "tile": ["Floor area", "Tile area", "Tiles", "Tiles with waste"],
    "grass_seed": ["Rate per 1000", "Pounds", "3 lb bags"],
    "fertilizer": ["Pounds of nitrogen", "Pounds of product", "Bags"],
}

# Friendly input names for the auto-generated worked-example bullets. The raw config
# ids ("tile_w", "rate") read badly in prose.
_INPUT_NAMES = {
    "fertilizer": {"area": "Lawn area (sq ft)", "rate": "Nitrogen rate (lb N per 1,000 sq ft)",
                   "nitrogen": "Nitrogen in bag (%)", "bag": "Bag size (lb)"},
}


_DATA_BULLET = re.compile(
    r"(?i)\b(length|width|height|depth|thickness|area|coats?|tile_w|tile_h|waste|rate|"
    r"bags?|square feet|cubic feet|cubic yards|gallons?|tons?|pounds?|tiles?)\b"
    r"[^\n]{0,24}?[:=][^\d\n]{0,6}[\d.,]+")


def _is_bullet(line: str) -> bool:
    return line.lstrip().startswith(("*", "-"))


def _is_data_bullet(line: str) -> bool:
    return _is_bullet(line) and bool(_DATA_BULLET.search(line))


def fix_worked_example(md: str, art: dict) -> tuple[str, str | None]:
    """Regenerate the worked-example bullets (with or without a heading) and the
    dimension phrase in the sentence that introduces them."""
    if art["slug"] in SPECIAL_SLUGS:
        return md, None
    key = art.get("calculator") or ""
    labels = _LABELS.get(key)
    if not labels:
        return md, None
    lines = md.split("\n")
    # Find a run of >= 2 bullet lines that carry input or output figures.
    start = end = None
    i = 0
    while i < len(lines):
        if _is_data_bullet(lines[i]):
            j = i
            while j < len(lines) and _is_bullet(lines[j]):
                j += 1
            if sum(_is_data_bullet(lines[k]) for k in range(i, j)) >= 2:
                start, end = i, j
                break
            i = j
        else:
            i += 1
    if start is None:
        return md, None
    ins = headline_inputs(art)
    out = calculators.compute(key, ins)
    names = _INPUT_NAMES.get(key, {})
    bullets = [f"*   {names.get(k, k)} = {_g(v)}" for k, v in ins.items()]
    for label in labels:
        val = out.get(_FIELD.get(label, ""))
        if val is not None:
            bullets.append(f"*   {label}: {_g(val)}")
    # Rewrite the introducing sentence's dimensions (e.g. "24.5 feet by 24.5 feet").
    p = start - 1
    while p >= 0 and not lines[p].strip():
        p -= 1
    if p >= 0 and re.search(r"(?i)worked example|measuring|feet by|ft by", lines[p]):
        L, W = _g(ins.get("length")), _g(ins.get("width"))
        lines[p] = re.sub(
            r"\d+(?:\.\d+)?\s*(?:feet|ft)\s*by\s*\d+(?:\.\d+)?\s*(?:feet|ft)",
            f"{L} feet by {W} feet", lines[p], flags=re.I)
        lines[p] = re.sub(r"\b\d+(?:\.\d+)?\s*[x×]\s*\d+(?:\.\d+)?\b", f"{L}x{W}", lines[p])
    new_block = bullets
    changed = lines[start:end] != new_block
    lines[start:end] = new_block
    if not changed:
        return md, None
    return "\n".join(lines), f"worked example ({key})"


def fix_prose_dims(md: str, art: dict) -> tuple[str, str | None]:
    """Replace odd worked-example dimensions left in the prose with the round pair,
    and correct any '= N cubic feet/square feet' result on the same line."""
    if art["slug"] in SPECIAL_SLUGS:
        return md, None
    ins = headline_inputs(art)
    L, W = ins.get("length"), ins.get("width")
    if L is None or W is None:
        return md, None
    old = art.get("calculator_defaults") or {}
    oL, oW = old.get("length"), old.get("width")
    if not isinstance(oL, (int, float)) or not isinstance(oW, (int, float)):
        return md, None
    if abs(oL - round(oL)) < 1e-9 and abs(oW - round(oW)) < 1e-9:
        return md, None
    Ls, Ws = _g(float(L)), _g(float(W))
    osL, osW = _g(float(oL)), _g(float(oW))
    pats = [
        (rf"{re.escape(osL)} feet long, {re.escape(osW)} feet wide",
         f"{Ls} feet long, {Ws} feet wide"),
        (rf"{re.escape(osW)} feet wide, {re.escape(osL)} feet long",
         f"{Ws} feet wide, {Ls} feet long"),
        (rf"{re.escape(osL)} feet by {re.escape(osW)} feet", f"{Ls} feet by {Ws} feet"),
        (rf"{re.escape(osW)} feet by {re.escape(osL)} feet", f"{Ws} feet by {Ls} feet"),
        (rf"{re.escape(osL)} \(length\) x {re.escape(osW)} \(width\)",
         f"{Ls} (length) x {Ws} (width)"),
        (rf"\b{re.escape(osL)} x {re.escape(osW)}\b", f"{Ls} x {Ws}"),
        (rf"\b{re.escape(osL)} by {re.escape(osW)}\b", f"{Ls} by {Ws}"),
        (rf"\b{re.escape(osL)}x{re.escape(osW)}\b", f"{Ls}x{Ws}"),
    ]
    lines = md.split("\n")
    out = calculators.compute(art["calculator"], ins)
    changed = False
    for i, line in enumerate(lines):
        new_line = line
        for pat, repl in pats:
            new_line = re.sub(pat, repl, new_line)
        if new_line != line:
            changed = True
            # Fix a stale "= 32.49 cubic feet" result on the same line.
            if "square feet" in new_line.lower() and "square_feet" in out:
                new_line = re.sub(r"=\s*[\d.,]+\s*(?:square|sq\.?)\s*feet",
                                  f"= {_g(out['square_feet'])} square feet", new_line, flags=re.I)
            if "cubic feet" in new_line.lower() and "cubic_feet" in out:
                new_line = re.sub(r"=\s*[\d.,]+\s*cubic feet",
                                  f"= {_g(out['cubic_feet'])} cubic feet", new_line, flags=re.I)
            lines[i] = new_line
    if not changed:
        return md, None
    return "\n".join(lines), "prose dimensions"


_LABEL_FIELD = {
    "square feet": "square_feet", "square foot": "square_feet",
    "cubic feet": "cubic_feet", "cubic foot": "cubic_feet",
    "cubic yards": "cubic_yards", "cubic yard": "cubic_yards",
    "cubic metres": "cubic_yards", "cubic meters": "cubic_yards",
    "bags 2cf": "bags_2cf", "bags 40lb": "bags_40lb", "bags 60lb": "bags_60lb",
    "bags 80lb": "bags_80lb", "bags 1.5cf": "bags_1_5cf", "bags 3lb": "bags_3lb",
    "bags": "bags", "2 cu ft bags": "bags_2cf", "40 lb bags": "bags_40lb",
    "40lb bags": "bags_40lb", "60 lb bags": "bags_60lb", "60lb bags": "bags_60lb",
    "80 lb bags": "bags_80lb", "80lb bags": "bags_80lb", "3 lb bags": "bags_3lb",
    "1.5 cu ft bags": "bags_1_5cf", "1.5 cf bags": "bags_1_5cf",
    "tons": "tons", "gallons": "gallons", "gallons required": "gallons",
    "tiles": "tiles", "tiles with waste": "tiles_with_waste",
    "paintable area": "paintable_area", "wall area": "wall_area",
    "floor area": "floor_area", "pounds": "pounds", "rate per 1000": "rate_per_1000",
}
_LABEL_LINE = re.compile(
    r"^([*\-]\s+)?(?:Inputs:\s*)?([A-Za-z][A-Za-z0-9 .]*?)\s*[:=]\s*([\d.,]+)", re.I)


def fix_worked_region(md: str, art: dict) -> tuple[str, str | None]:
    """Within the worked-example region, set every 'Label: value' line to the
    computed value and round the inline length/width inputs."""
    if art["slug"] in SPECIAL_SLUGS:
        return md, None
    key = art.get("calculator") or ""
    if key not in _LABELS:
        return md, None
    lines = md.split("\n")
    start = None
    for i, line in enumerate(lines):
        if re.search(r"(?i)worked example", line) or re.match(r"(?i)^inputs:\s*length", line.strip()):
            start = i
            break
    if start is None:
        return md, None
    end = min(len(lines), start + 15)
    for i in range(start + 1, end):
        if re.match(r"^#{2,3}\s", lines[i]):
            end = i
            break
    ins = headline_inputs(art)
    if "length" not in ins or "width" not in ins:
        return md, None
    out = calculators.compute(key, ins)
    Ls, Ws = _g(float(ins["length"])), _g(float(ins["width"]))
    changed = False
    for i in range(start, end):
        line = lines[i]
        if line.strip().startswith("|"):
            continue
        new = line
        # Inline inputs: "Inputs: length = 11.0, width = 11.0, thickness = 4"
        if re.search(r"(?i)length\s*=", new):
            new = re.sub(r"(?i)\blength\s*=\s*[\d.]+", f"length = {Ls}", new)
            new = re.sub(r"(?i)\bwidth\s*=\s*[\d.]+", f"width = {Ws}", new)
        m = _LABEL_LINE.match(new.strip())
        if m:
            label = m.group(2).strip().lower()
            field = _LABEL_FIELD.get(label)
            if field and field in out:
                new = re.sub(r"([:=]\s*)[\d.,]+", rf"\g<1>{_g(out[field])}", new, count=1)
        if new != line:
            changed = True
            lines[i] = new
    if not changed:
        return md, None
    return "\n".join(lines), "worked-region figures"


def _table_kind(header: str) -> str:
    h = header.lower()
    # "bag" first: the "2 cu ft bags" heading also contains "cu ft".
    if "bag" in h:
        return "bag"
    if "cubic feet" in h or "cu ft" in h:
        return "cuft"
    if "cubic yard" in h or "cu yd" in h:
        return "cuyd"
    return "other"


def _bag_size(header: str) -> float | None:
    h = header.lower()
    for k, v in BAG_SIZE.items():
        if k in h:
            return v
    return None


def fix_table(md: str, art: dict) -> tuple[str, list[str]]:
    """Recompute any table that carries a cubic-feet column.

    Rows without a cubic-feet column are left alone: deriving the bag count from a
    rounded cubic-yard figure introduces rounding errors the original did not have.
    """
    lines = md.split("\n")
    out_lines: list[str] = []
    corrections: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) \
                and set(lines[i + 1].strip()) <= set("|-: "):
            headers = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            kinds = [_table_kind(h) for h in headers]
            if "cuft" not in kinds:
                out_lines.append(lines[i])
                i += 1
                continue
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            for row in lines[i:j]:
                if row is lines[i] or set(row.strip()) <= set("|-: "):
                    out_lines.append(row)
                    continue
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if len(cells) != len(headers):
                    out_lines.append(row)
                    continue
                cuft = next((_num(c) for c, k in zip(cells, kinds) if k == "cuft"), None)
                if cuft is None:
                    out_lines.append(row)
                    continue
                new_cells = list(cells)
                for n, (c, k, h) in enumerate(zip(cells, kinds, headers)):
                    if k == "cuyd":
                        want = f"{round(cuft / 27.0, 2)}"
                        if _num(c) is None or abs(_num(c) - float(want)) > 1e-9:
                            corrections.append(f"table {cells[0]} {h}: {c} -> {want}")
                        new_cells[n] = want
                    elif k == "bag":
                        size = _bag_size(h)
                        if size:
                            want = str(math.ceil(cuft / size))
                            if _num(c) is None or int(_num(c)) != int(want):
                                corrections.append(f"table {cells[0]} {h}: {c} -> {want}")
                            new_cells[n] = want
                out_lines.append("| " + " | ".join(new_cells) + " |")
            i = j
        else:
            out_lines.append(lines[i])
            i += 1
    return "\n".join(out_lines), corrections


def _num(v) -> float:
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return 0.0


def worked_example_section(art: dict) -> str:
    """A scannable '## Worked Example' built only from the calculator's own output.

    Long-tail pages that walk through the maths in prose still lack the labelled
    equation block a featured snippet prefers, so this adds one where it is missing.
    """
    key = art.get("calculator") or ""
    ins = headline_inputs(art)
    out = calculators.compute(key, ins)
    g = _g
    L, W = ins.get("length"), ins.get("width")
    if key == "mulch":
        body = (f"{g(L)} ft x {g(W)} ft = {g(out['square_feet'])} sq ft. "
                f"{g(out['square_feet'])} sq ft x {g(ins['depth'])} in (0.25 ft per 3 in) "
                f"= {g(out['cubic_feet'])} cubic feet, which is {out['cubic_yards']} cubic "
                f"yards or {out['bags_2cf']} bags of 2 cu ft.")
    elif key == "topsoil":
        body = (f"{g(L)} ft x {g(W)} ft = {g(out['square_feet'])} sq ft. At {g(ins['depth'])} in "
                f"deep that is {g(out['cubic_feet'])} cubic feet, or {out['cubic_yards']} cubic "
                f"yards, about {out['bags_40lb']} bags of 40 lb.")
    elif key == "soil":
        body = (f"{g(L)} ft x {g(W)} ft x {g(ins['height'])} in = {g(out['cubic_feet'])} cubic "
                f"feet, which is {out['cubic_yards']} cubic yards, about {out['bags_1_5cf']} bags "
                f"of 1.5 cu ft.")
    elif key == "gravel":
        cuft = _num(out["cubic_yards"]) * 27
        body = (f"{g(L)} ft x {g(W)} ft = {g(out['square_feet'])} sq ft. At {g(ins['depth'])} in "
                f"deep that is about {g(cuft)} cubic feet = {out['cubic_yards']} cubic yards, "
                f"roughly {out['tons']} tons.")
    elif key == "concrete":
        body = (f"{g(L)} ft x {g(W)} ft x {g(ins['thickness'])} in = {g(out['cubic_feet'])} cubic "
                f"feet = {out['cubic_yards']} cubic yards. That is about {out['bags_80lb']} bags "
                f"of 80 lb or {out['bags_60lb']} bags of 60 lb.")
    elif key == "paint":
        perim = 2 * (_num(L) + _num(W))
        body = (f"Perimeter = 2 x ({g(L)} + {g(W)}) = {g(perim)} ft. Wall area = {g(perim)} x "
                f"{g(ins['height'])} = {out['wall_area']} sq ft. Less one door and two windows "
                f"= {out['paintable_area']} sq ft. Two coats at about 350 sq ft per gallon "
                f"= {out['gallons']} gallons.")
    elif key == "tile":
        body = (f"{g(L)} ft x {g(W)} ft = {g(out['floor_area'])} sq ft. Each {g(ins['tile_w'])} x "
                f"{g(ins['tile_h'])} in tile covers {g(out['tile_area'])} sq ft, so "
                f"{g(out['floor_area'])} ÷ {g(out['tile_area'])} = {out['tiles']} tiles. "
                f"Add {g(ins['waste'])}% waste = {out['tiles_with_waste']} tiles.")
    elif key == "grass_seed":
        bags = out["bags_3lb"]
        body = (f"{int(ins['area']):,} sq ft at {g(out['rate_per_1000'])} lb per 1,000 sq ft "
                f"= {g(out['pounds'])} lb of seed, about {bags} "
                f"{'bag' if bags == 1 else 'bags'} of 3 lb.")
    elif key == "fertilizer":
        body = (f"{g(ins['area'])} sq ft at {g(ins['rate'])} lb N per 1,000 sq ft needs "
                f"{out['pounds_nitrogen']} lb of actual nitrogen. A {g(ins['nitrogen'])}% bag "
                f"supplies that in {out['pounds']} lb of product, about {out['bags']} bags.")
    else:
        return ""
    return f"## Worked Example\n\n{body}"


def _has_worked_block(md: str) -> bool:
    if re.search(r"(?i)^#{2,4}\s+.*worked example", md, re.M):
        return True
    if re.search(r"(?i)^\s*(?:inputs?)\s*:", md, re.M):
        return True
    if re.search(r"\d[\d,\.]*\s*[x*×]\s*[\d\.]+\s*=", md):
        return True
    lines = md.split("\n")
    run = 0
    for line in lines:
        if re.match(r"^\s*(?:\*|-)?\s*[A-Za-z][A-Za-z0-9 .%]{2,30}\s*[:=]\s*[\d.,]+", line):
            run += 1
            if run >= 3:
                return True
        else:
            run = 0
    return False


def ensure_worked_example(md: str, art: dict) -> tuple[str, str | None]:
    """Insert a computed worked example after the first section when the page has none."""
    if art["slug"] in SPECIAL_SLUGS:
        return md, None
    if not art.get("calculator") or _has_worked_block(md):
        return md, None
    section = worked_example_section(art)
    if not section:
        return md, None
    lines = md.split("\n")
    # Insert before the second H2, so it sits right below the intro's first section.
    h2 = [i for i, l in enumerate(lines) if re.match(r"^##\s", l)]
    at = h2[1] if len(h2) >= 2 else len(lines)
    lines[at:at] = section.split("\n") + [""]
    return "\n".join(lines), "worked example section"


_MISTAKES = {
    "mulch": "**Piling it against stems and trunks.** Keep mulch a few inches clear of bark, "
             "or it holds moisture against the plant and invites rot.",
    "topsoil": "**Filling deeper than the roots need.** Most beds only need 6 to 12 inches; "
               "more soil just costs money and settles.",
    "soil": "**Forgetting that fresh mix settles.** Order about 10 per cent extra, because "
            "loose soil compacts after the first few waterings.",
    "gravel": "**Skipping the sub-base or fabric.** Gravel disappears into soft ground without "
              "a geotextile barrier underneath it.",
    "concrete": "**Mixing too little in one go.** A slab has to be poured as one continuous "
                "batch, so buy a bag or two spare rather than stopping halfway.",
    "paint": "**Planning for a single coat.** One coat rarely covers evenly, so always "
             "calculate for two and buy in the same batch for a colour match.",
    "tile": "**Ignoring the waste allowance.** Cuts, breakage and pattern matching all use "
            "tile, so add 10 per cent for a straight layout and 15 for diagonal.",
    "grass_seed": "**Burying the seed.** Rake it in no more than a quarter inch deep; deeper "
                  "and the seedling runs out of energy before it reaches the light.",
    "fertilizer": "**Guessing the spread rate.** Over-application burns the lawn, so weigh the "
                  "product and set the spreader rather than eyeballing it.",
}


def ensure_common_mistakes(md: str, art: dict) -> tuple[str, str | None]:
    """Add a short, calculator-specific mistakes section when the page has none."""
    if art["slug"] in SPECIAL_SLUGS or not art.get("calculator"):
        return md, None
    if re.search(r"(?i)^#{2,4}\s+.*(mistake|error|confus|pitfall|avoid|wrong)", md, re.M):
        return md, None
    line = _MISTAKES.get(art["calculator"])
    if not line:
        return md, None
    section = f"## Common Mistakes to Avoid\n\n{line}"
    lines = md.split("\n")
    h2 = [i for i, l in enumerate(lines) if re.match(r"^##\s", l)]
    at = h2[-1] if h2 else len(lines)
    lines[at:at] = section.split("\n") + [""]
    return "\n".join(lines), "common mistakes section"


def fix_article(art: dict) -> list[str]:
    if not art.get("calculator"):
        art.setdefault("answer", "")
        return []
    if art.get("is_pillar"):
        # Pillar pages keep their curated prose, but the answer box still prefers the
        # computed sentence for a featured snippet, so fill it when it is missing.
        if not (art.get("answer") or "").strip():
            art["answer"] = answer_text(art)
            return ["answer box (pillar)"]
        return []
    if art["slug"] in SPECIAL_SLUGS:
        # The box calculator cannot model this query; keep the hand-written prose
        # and widget defaults untouched and only fill the answer box.
        new = answer_text(art)
        changed = new != art.get("answer")
        art["answer"] = new
        return ["answer box (special-case page)"] if changed else []
    changes: list[str] = []
    ins = headline_inputs(art)
    # Prose fixes compare against the *old* defaults, so run them before the swap.
    md = art.get("body_markdown", "")
    for fn in (fix_intro, fix_worked_example, fix_prose_dims):
        md, c = fn(md, art)
        if c:
            changes.append(c)
    md, c = fix_worked_region(md, art)
    if c:
        changes.append(c)
    md, c = ensure_worked_example(md, art)
    if c:
        changes.append(c)
    md, c = ensure_common_mistakes(md, art)
    if c:
        changes.append(c)
    md, cs = fix_table(md, art)
    changes += cs
    if ins != (art.get("calculator_defaults") or {}):
        changes.append(f"defaults {art.get('calculator_defaults')} -> {ins}")
        art["calculator_defaults"] = ins
    art["calculator_output"] = calculators.compute(art["calculator"], ins)
    art["body_markdown"] = md
    art["answer"] = answer_text(art)
    art["word_count"] = len(md.split())
    return changes


def run(arts: list[dict]) -> dict:
    report = {}
    for art in arts:
        if art.get("status") not in ("published", "approved"):
            continue
        changes = fix_article(art)
        if changes:
            report[art["slug"]] = changes
    return report


if __name__ == "__main__":
    from common import load_json, save_json

    path = Path(__file__).resolve().parent.parent / "data" / "articles.json"
    arts = load_json(path, default=[])
    rep = run(arts)
    save_json(path, arts)
    for slug, ch in rep.items():
        print(slug)
        for c in ch:
            print("   ", c)
    print(f"\n{len(rep)} articles changed")
