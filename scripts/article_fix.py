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
        if area:
            return {**base, "area": float(area.group(1).replace(",", ""))}
        if "1000" in kw or "per square foot" in kw:
            return {**base, "area": 1000}
        return base
    return base


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
    if key in ("grass_seed", "fertilizer"):
        return f"{int(inputs.get('area', 0)):,} sq ft"
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
        return (f"{where} needs about {_g(out['pounds'])} lb of product "
                f"({out['bags']} bag) at {_g(out.get('rate_per_1000', 1))} lb per 1,000 sq ft.")
    return art.get("meta_description", "")


def _intro_paragraph(art: dict) -> str:
    for line in art.get("body_markdown", "").split("\n"):
        s = line.strip()
        if s and s[0] not in "#|*-" and not s[0].isdigit() and not s.startswith(">"):
            return s
    return art.get("meta_description", "")


def _intro_index(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        s = line.strip()
        if s and s[0] not in "#|*-" and not s[0].isdigit() and not s.startswith(">"):
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
    "fertilizer": ["Pounds", "Bags"],
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
    bullets = ["*   " + " = ".join([k, _g(v)]) for k, v in ins.items()]
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


def fix_article(art: dict) -> list[str]:
    if art.get("is_pillar") or not art.get("calculator"):
        art.setdefault("answer", "")
        return []
    if art["slug"] in SPECIAL_SLUGS:
        # The box calculator cannot model this query; keep the hand-written prose
        # and widget defaults untouched and only fill the answer box.
        art["answer"] = answer_text(art)
        return ["answer box (special-case page)"]
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
    import json

    path = Path(__file__).resolve().parent.parent / "data" / "articles.json"
    arts = json.load(open(path))
    rep = run(arts)
    json.dump(arts, open(path, "w"), indent=2, ensure_ascii=False)
    for slug, ch in rep.items():
        print(slug)
        for c in ch:
            print("   ", c)
    print(f"\n{len(rep)} articles changed")
