"""Original figure generation for articles.

Every article gets a purpose-built diagram rather than a stock photo: a labelled
cross-section for volume calculations (mulch, soil, topsoil, gravel, concrete) or a
coverage/rate chart for the others. Drawing them programmatically keeps the site
free of third-party image licences and gives each page a genuinely relevant visual
that also earns image-search placement.

Pillow is optional at runtime: if it is missing the build simply skips figures and
the templates fall back to an abstract CSS pattern, so a deploy can never break.
"""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except Exception:  # pragma: no cover - Pillow is installed in CI via requirements
    HAVE_PIL = False

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"

W, H = 1200, 675
TW, TH = 480, 270

INK = (21, 42, 29)
INK_SOFT = (68, 88, 74)
MUTED = (104, 121, 109)
LINE = (219, 230, 221)
WHITE = (255, 255, 255)

HEADER_H = 128
FOOTER_H = 96
PANEL_TOP = HEADER_H + 44
PANEL_BOTTOM = H - FOOTER_H - 8

# Per-cluster presentation: category label, accent colour, diagram kind.
CLUSTERS = {
    "mulch":      ("Mulch",             (22, 101, 52),   "layer"),
    "soil":       ("Soil & Raised Beds",(30, 90, 60),    "layer"),
    "topsoil":    ("Topsoil & Fill",    (74, 63, 42),    "layer"),
    "gravel":     ("Gravel & Stone",    (90, 96, 102),   "layer"),
    "concrete":   ("Concrete",          (100, 116, 139), "layer"),
    "paint":      ("Paint",             (37, 99, 235),   "bars"),
    "tile":       ("Tile",              (13, 148, 136),  "grid"),
    "grass-seed": ("Grass Seed",        (77, 124, 15),   "bars"),
    "fertilizer": ("Fertilizer",        (180, 83, 9),    "bars"),
}


def _font(name: str, size: int):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except Exception:
        return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _num(v, default=1.0):
    try:
        f = float(v)
        return f if f > 0 else default
    except Exception:
        return default


def _r(v, p=1):
    return round(v, p)


def _cluster_meta(cluster):
    return CLUSTERS.get(cluster, ("Guide", (22, 101, 52), "layer"))


# --------------------------------------------------------------------------- panels
def _layer_panel(d, box, cluster, art):
    """Cross-section: an area slab with a depth layer drawn to scale."""
    x0, y0, x1, y1 = box
    accent = _cluster_meta(cluster)[1]
    cd = art.get("calculator_defaults") or {}
    length = _num(cd.get("length"), 20)
    width = _num(cd.get("width"), 10)
    depth_key = next((k for k in ("depth", "height", "thickness") if k in cd), "depth")
    depth = _num(cd.get(depth_key), 3)
    label_key = {"depth": "depth", "height": "fill height",
                 "thickness": "thickness"}[depth_key]

    area = length * width
    # Ground line near the lower third; leave a caption strip below.
    ground_y = y1 - 92
    slab_h = 34
    d.rectangle([x0, ground_y, x1, ground_y + slab_h], fill=(233, 225, 208))
    d.line([x0, ground_y, x1, ground_y], fill=(176, 156, 116), width=3)

    lx0, lx1 = x0 + 30, x1 - 190
    max_layer = ground_y - y0 - 76
    layer_h = int(min(max_layer, 30 + depth * 30))
    d.rounded_rectangle([lx0, ground_y - layer_h, lx1, ground_y], radius=8, fill=accent)
    for i in range(1, 4):
        yy = ground_y - layer_h + i * layer_h / 4
        d.line([lx0 + 14, yy, lx1 - 14, yy], fill=(255, 255, 255), width=1)

    # Depth dimension on the right of the layer.
    ax = lx1 + 34
    d.line([ax, ground_y, ax, ground_y - layer_h], fill=INK, width=3)
    d.polygon([(ax, ground_y), (ax - 8, ground_y - 12), (ax + 8, ground_y - 12)], fill=INK)
    d.polygon([(ax, ground_y - layer_h), (ax - 8, ground_y - layer_h + 12),
               (ax + 8, ground_y - layer_h + 12)], fill=INK)
    mid = ground_y - layer_h / 2
    d.text((ax + 16, mid - 34), f'{_r(depth,1):g}"', font=_font(BOLD, 30), fill=INK)
    d.text((ax + 16, mid - 2), label_key, font=_font(REG, 20), fill=MUTED)

    # Area caption below the ground strip.
    d.text((x0, ground_y + slab_h + 12),
           f"{_r(length,0):g} ft x {_r(width,0):g} ft  =  {_r(area,0):g} sq ft",
           font=_font(BOLD, 30), fill=INK)


def _bars_panel(d, box, cluster, art):
    """Coverage / rate bars for paint, seed, fertilizer."""
    x0, y0, x1, y1 = box
    accent = _cluster_meta(cluster)[1]
    spec = {
        "paint": ("Gallons scale with the number of coats", [
            ("1 coat", 1.0), ("2 coats", 2.0), ("3 coats", 3.0)]),
        "grass-seed": ("Seeding rate per 1,000 sq ft (lb)", [
            ("Overseed", 2.0), ("New lawn", 4.5), ("Heavy", 6.0)]),
        "fertilizer": ("Application rate per 1,000 sq ft (lb)", [
            ("Light", 0.5), ("Standard", 1.0), ("Heavy", 1.5)]),
    }
    heading, rows = spec.get(cluster, ("Relative amount", [("Low", 1), ("Mid", 2), ("High", 3)]))
    d.text((x0, y0 - 34), heading, font=_font(BOLD, 26), fill=INK_SOFT)
    n = len(rows)
    track_h = y1 - y0
    row_h = track_h / n
    label_w = 190
    value_w = 90
    bar_x0 = x0 + label_w
    bar_max = x1 - label_w - value_w
    maxv = max(v for _, v in rows)
    for i, (label, val) in enumerate(rows):
        cy = y0 + i * row_h + row_h / 2
        d.text((x0, cy - 16), label, font=_font(REG, 25), fill=INK)
        bw = max(26, bar_max * (val / maxv))
        d.rounded_rectangle([bar_x0, cy - 17, bar_x0 + bar_max, cy + 17], radius=9,
                            fill=(238, 244, 238))
        d.rounded_rectangle([bar_x0, cy - 17, bar_x0 + bw, cy + 17], radius=9, fill=accent)
        d.text((bar_x0 + bw + 16, cy - 15), f"{val:g}", font=_font(BOLD, 25), fill=INK)


def _grid_panel(d, box, cluster, art):
    """Tile layout schematic with a waste allowance caption."""
    x0, y0, x1, y1 = box
    accent = _cluster_meta(cluster)[1]
    cd = art.get("calculator_defaults") or {}
    cols, rows = 7, 4
    gap = 10
    caption_h = 46
    avail_w = x1 - x0
    avail_h = (y1 - caption_h) - y0
    cell = min((avail_w - gap * (cols - 1)) / cols, (avail_h - gap * (rows - 1)) / rows)
    grid_w = cell * cols + gap * (cols - 1)
    ox = x0 + (avail_w - grid_w) / 2
    for r in range(rows):
        for c in range(cols):
            bx = ox + c * (cell + gap)
            by = y0 + r * (cell + gap)
            tone = accent if (r + c) % 2 == 0 else (26, 168, 156)
            d.rounded_rectangle([bx, by, bx + cell, by + cell], radius=5, fill=tone)
    d.text((x0, y1 - 34),
           f'Tile {_r(_num(cd.get("tile_w"),12),0):g}" x {_r(_num(cd.get("tile_h"),12),0):g}"'
           f'  ·  add {_r(_num(cd.get("waste"),10),0):g}% for cuts and breakage',
           font=_font(REG, 24), fill=MUTED)


PANELS = {"layer": _layer_panel, "bars": _bars_panel, "grid": _grid_panel}


# --------------------------------------------------------------------------- frames
def _header(d, cluster, art):
    accent = _cluster_meta(cluster)[1]
    d.rectangle([0, 0, W, HEADER_H], fill=accent)
    for i in range(-H, W, 46):
        d.line([i, HEADER_H, i + 90, 0], fill=(255, 255, 255), width=2)
    label = _cluster_meta(cluster)[0].upper()
    chip_f = _font(BOLD, 22)
    tw = d.textlength(label, font=chip_f)
    d.rounded_rectangle([48, 26, 48 + tw + 32, 66], radius=20, fill=WHITE)
    d.text((64, 34), label, font=chip_f, fill=accent)
    title_f = _font(BOLD, 40)
    lines = _wrap(d, art.get("title", ""), title_f, W - 96)[:2]
    ty = HEADER_H - 46 if len(lines) == 1 else HEADER_H - 84
    for ln in lines:
        d.text((48, ty), ln, font=title_f, fill=WHITE)
        ty += 42


def _footer(d, art):
    f = _font(REG, 23)
    text = art.get("meta_description") or art.get("primary_keyword", "")
    lines = _wrap(d, text, f, W - 96)[:2]
    y = H - FOOTER_H + 18
    d.line([48, y - 16, W - 48, y - 16], fill=LINE, width=2)
    for ln in lines:
        d.text((48, y), ln, font=f, fill=INK_SOFT)
        y += 28
    d.text((W - 205, H - 42), "GardenCalc", font=_font(BOLD, 24), fill=CLUSTERS["mulch"][1])


def render_figure(art: dict, size=(W, H)):
    if not HAVE_PIL:
        return None
    img = Image.new("RGB", size, WHITE)
    d = ImageDraw.Draw(img)
    _header(d, art.get("cluster", ""), art)
    box = (48, PANEL_TOP, W - 48, PANEL_BOTTOM)
    PANELS[_cluster_meta(art.get("cluster", ""))[2]](d, box, art.get("cluster", ""), art)
    _footer(d, art)
    if size != (W, H):
        img = img.resize(size, Image.LANCZOS)
    return img


def render_pins(cards: list[dict], static_root: Path) -> dict:
    """Vertical 1000x1500 Pinterest pins for charts and planners.

    One pin per linkable asset, brand-coloured, with the page title, the question it
    answers and the GardenCalc URL so every repin carries a citation back to the page.
    """
    if not HAVE_PIL:
        return {"pins": 0}
    pin_dir = static_root / "img" / "pins"
    pin_dir.mkdir(parents=True, exist_ok=True)
    PW, PH = 1000, 1500
    n = 0
    for card in cards:
        accent = CLUSTERS.get(card.get("cluster", ""), CLUSTERS["mulch"])[1]
        img = Image.new("RGB", (PW, PH), accent)
        d = ImageDraw.Draw(img)
        # diagonal texture, matching the figure/OG house style
        for i in range(-PH, PW, 60):
            d.line([i, PH, i + 160, 0], fill=(accent[0] + 16, accent[1] + 16, accent[2] + 16), width=4)
        d.text((72, 120), "GARDENCALC", font=_font(BOLD, 40), fill=(198, 235, 205))
        title_f = _font(BOLD, 78)
        y = 300
        for ln in _wrap(d, card.get("title", ""), title_f, PW - 144)[:4]:
            d.text((72, y), ln, font=title_f, fill=WHITE)
            y += 92
        q = card.get("question") or ""
        if q:
            qf = _font(REG, 46)
            y += 40
            for ln in _wrap(d, q, qf, PW - 144)[:3]:
                d.text((72, y), ln, font=qf, fill=(225, 245, 230))
                y += 56
        d.text((72, PH - 160), "huzaifamasood30.github.io/gardencalc", font=_font(BOLD, 40), fill=(225, 245, 230))
        d.text((72, PH - 100), "Free calculators that show the formula", font=_font(REG, 38), fill=(198, 235, 205))
        img.save(pin_dir / f"{card['slug']}.png", "PNG")
        n += 1
    print(f"[images] generated {n} pins")
    return {"pins": n}


def render_brand(static_root: Path) -> dict:
    """Write the publisher logo, favicon and PNG OG fallback.

    These are branding assets rather than per-article figures, but they share the
    Pillow dependency and the copied static root, so they live here.
    """
    if not HAVE_PIL:
        return {"logo": 0, "favicon": 0, "og": 0}
    img_dir = static_root / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    accent = CLUSTERS["mulch"][1]

    logo = Image.new("RGB", (336, 336), WHITE)
    d = ImageDraw.Draw(logo)
    d.rounded_rectangle([0, 0, 335, 335], radius=60, fill=accent)
    cx, cy = 168, 150
    d.line([(cx, cy + 96), (cx, cy - 20)], fill=(134, 239, 172), width=14)
    d.line([(cx, cy + 40), (cx + 82, cy - 30)], fill=(134, 239, 172), width=14)
    d.line([(cx, cy + 62), (cx - 82, cy - 8)], fill=(134, 239, 172), width=14)
    d.line([(cx, cy - 12), (cx, cy - 52)], fill=(255, 212, 121), width=16)
    d.text((70, 268), "GardenCalc", font=_font(BOLD, 40), fill=WHITE)
    logo.save(img_dir / "logo.png", "PNG")

    logo.resize((180, 180), Image.LANCZOS).save(img_dir / "apple-touch-icon.png", "PNG")
    logo.resize((48, 48), Image.LANCZOS).save(img_dir / "favicon.ico", "ICO")

    og = Image.new("RGB", (1200, 630), WHITE)
    od = ImageDraw.Draw(og)
    od.rectangle([0, 0, 1200, 630], fill=accent)
    for i in range(-630, 1200, 46):
        od.line([i, 0, i + 120, 630], fill=(accent[0] + 18, accent[1] + 18, accent[2] + 18), width=3)
    od.text((72, 132), "GardenCalc", font=_font(BOLD, 92), fill=WHITE)
    od.text((74, 244), "Free home & garden calculators", font=_font(REG, 44), fill=(220, 240, 225))
    od.text((74, 304), "and practical how-to guides", font=_font(REG, 44), fill=(220, 240, 225))
    od.text((74, 452), "huzaifamasood30.github.io/gardencalc", font=_font(REG, 30), fill=(190, 232, 200))
    og.save(img_dir / "og-default.png", "PNG")
    return {"logo": 1, "favicon": 2, "og": 1}


def generate(published: list[dict], static_root: Path) -> dict:
    """Write fig/ and thumb/ WebP images. Returns counts for the build report."""
    if not HAVE_PIL:
        print("[images] Pillow not available; skipping figure generation")
        return {"figures": 0, "thumbs": 0}
    fig_dir = static_root / "img" / "fig"
    thumb_dir = static_root / "img" / "thumb"
    fig_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for art in published:
        try:
            big = render_figure(art)
            if big is None:
                continue
            big.save(fig_dir / f"{art['slug']}.webp", "WEBP", quality=82, method=6)
            big.resize((TW, TH), Image.LANCZOS).save(
                thumb_dir / f"{art['slug']}.webp", "WEBP", quality=80, method=6)
            n += 1
        except Exception as exc:  # a bad figure must never fail the build
            print(f"[images] {art.get('slug')}: {exc}")
    print(f"[images] generated {n} figures")
    return {"figures": n, "thumbs": n}


if __name__ == "__main__":
    from common import DATA, STATIC, load_json

    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]
    generate(arts, STATIC)
