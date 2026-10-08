"""Static site build. Reads data/articles.json + config, writes site/."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

import images
import mdrender
import seo as seolib
from common import (CONFIG, CONTENT, DATA, SITE, STATIC, TEMPLATES, load_json,
                    save_json, seo_config, site_config, topics_config)

YEAR = dt.date.today().year

# Inline SVG icon id for each project category (symbols live in base.html).
CATEGORY_ICONS = {
    "mulch": "mulch", "soil": "soil", "gravel": "gravel", "paint": "paint",
    "tile": "tile", "grass-seed": "seed", "concrete": "concrete",
    "topsoil": "topsoil", "fertilizer": "fertilizer",
}
BLURBS = {
    "mulch": "Work out bags or cubic yards of mulch for any bed size and depth.",
    "soil": "Fill raised beds with the right amount of soil mix.",
    "gravel": "Calculate cubic yards and tons of gravel for paths and drives.",
    "paint": "Estimate gallons of paint per room, coats and openings.",
    "tile": "Count tiles and waste allowance for floors and walls.",
    "grass-seed": "Seed a new lawn or overseed an existing one at the right rate.",
    "concrete": "Get cubic yards and bag counts for slabs and footings.",
    "topsoil": "Estimate cubic yards or bags of topsoil to fill or level any area.",
    "fertilizer": "Find pounds and bags of fertilizer for your lawn at the right rate.",
}
# What the figure shows, per category — used for the caption and image alt text.
FIG_CAPTION = {
    "mulch": "Cross-section of a mulched bed: area x depth gives the volume to order.",
    "soil": "Cross-section of a raised bed being filled to its working height.",
    "topsoil": "Cross-section of an area being levelled with topsoil.",
    "gravel": "Cross-section of a gravel layer at the chosen depth.",
    "concrete": "Cross-section of a concrete slab at the chosen thickness.",
    "paint": "How the number of coats multiplies the paint you need.",
    "grass-seed": "Sowing rates per 1,000 sq ft for new lawns and overseeding.",
    "fertilizer": "Application rates per 1,000 sq ft at light, standard and heavy doses.",
    "tile": "Tile layout showing the waste allowance added for cuts and breakage.",
}


def _env() -> Environment:
    return Environment(loader=FileSystemLoader(str(TEMPLATES)),
                       autoescape=select_autoescape(["html", "xml"]))


def _base(site: dict) -> str:
    return (site.get("custom_domain") or site["base_url"]).rstrip("/")


def _abs(site: dict, path: str) -> str:
    return _base(site) + "/" + path.lstrip("/")


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _contact_block(site: dict) -> str:
    """Honest contact route: a real email if configured, otherwise the repo issues page."""
    email = site.get("contact_email", "").strip()
    if email and "example.com" not in email:
        return f"Email us at **{email}** and we will reply within a few working days."
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if repo:
        return (f"The fastest way to reach us is to open an issue on the project's "
                f"[GitHub repository](https://github.com/{repo}/issues). We reply within "
                f"a few working days.")
    return ("Contact details will be published here shortly. In the meantime, please use "
            "the repository's issue tracker if you found this project through GitHub.")


def _reading_time(words: int) -> int:
    return max(1, round(words / 220))


def _thumb(site: dict, art: dict) -> str:
    """Article thumbnail URL (theme figure), with a CSS fallback if images were skipped."""
    return _abs(site, f"/static/img/thumb/{art['slug']}.webp")


def _fig(site: dict, art: dict) -> str:
    return _abs(site, f"/static/img/fig/{art['slug']}.webp")


def _card_meta(site: dict, art: dict, category: str | None = None) -> dict:
    return {
        "slug": art["slug"],
        "title": art["title"],
        "desc": art.get("meta_description", "")[:120],
        "thumb": _thumb(site, art),
        "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        "category": category,
    }


def _calc_context(art: dict, cfg: dict, site: dict) -> dict | None:
    calc_key = art.get("calculator")
    defs = cfg.get("calculators", {}).get(calc_key)
    if not defs:
        return None
    inputs = []
    for inp in defs.get("inputs", []):
        d = dict(inp)
        d.setdefault("step", "0.1")
        inputs.append(d)
    return {
        "key": calc_key,
        "title": art.get("calculator_title") or defs.get("title", "Calculator"),
        "sub": "Change any value and the answer updates instantly. Nothing is sent anywhere — it runs in your browser.",
        "hint": "Estimates only. Round up when ordering and check with your supplier.",
        "inputs": inputs,
    }


def build() -> dict:
    site = site_config()
    tcfg = topics_config()
    arts = load_json(DATA / "articles.json", default=[])
    published = [a for a in arts
                 if a.get("status") in ("published", "approved")
                 and a.get("quality", {}).get("passed")]
    published.sort(key=lambda a: a.get("created", ""), reverse=True)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    base = _base(site)
    categories = tcfg.get("clusters", [])
    for c in categories:
        c["blurb"] = BLURBS.get(c["id"], "Free calculators and practical guides.")
        c["icon"] = CATEGORY_ICONS.get(c["id"], "leaf")
    cat_map = {c["id"]: c for c in categories}
    nav_categories = [{"id": c["id"], "name": c["name"]} for c in categories]

    env = _env()
    env.globals.update(base_url=base, site=site, year=YEAR,
                       nav_categories=nav_categories, calc_defs=tcfg.get("calculators", {}))

    default_og = _thumb(site, published[0]) if published else _abs(site, "/static/img/og-default.svg")

    def common(title, description, canonical, og_type="website", og_image=None,
               schemas=None, robots=None, keywords=None):
        return dict(title=title, description=description, canonical=canonical,
                    og_type=og_type, og_image=og_image or default_og,
                    schemas=schemas or [],
                    robots=robots or "index, follow, max-snippet:-1, max-image-preview:large",
                    keywords=keywords, base_url=base)

    # Index for prev/next within each cluster, ordered by creation date.
    by_cluster: dict[str, list[dict]] = {}
    for a in sorted(published, key=lambda x: x.get("created", "")):
        by_cluster.setdefault(a.get("cluster", ""), []).append(a)
    order_index = {a["slug"]: i for lst in by_cluster.values() for i, a in enumerate(lst)}

    # --- articles ---
    for art in published:
        body_html, toc = mdrender.render_with_toc(art.get("body_markdown", ""),
                                                  {x["slug"]: f"{base}/{x['slug']}/" for x in published})
        figure = {
            "src": _fig(site, art),
            "alt": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
            "caption": FIG_CAPTION.get(art.get("cluster", ""), art["title"]),
        }
        ct = cat_map.get(art.get("cluster", ""), {})
        category_name = ct.get("name", "Guides")

        # Related: sibling articles in the same cluster, excluding self.
        cl = by_cluster.get(art.get("cluster", ""), [])
        sib = [a for a in cl if a["slug"] != art["slug"]]
        pos = next((i for i, a in enumerate(cl) if a["slug"] == art["slug"]), 0)
        prev_art = cl[pos - 1] if pos > 0 else None
        next_art = cl[pos + 1] if pos + 1 < len(cl) else None
        related = [_card_meta(site, a, category_name) for a in sib[:3]]

        schemas = [json.dumps(s, ensure_ascii=False) for s in
                   seolib.all_schema(art, site, figure=_fig(site, art))]
        ctx = common(title=art["title"], description=art["meta_description"],
                     canonical=_abs(site, f"/{art['slug']}/"), og_type="article",
                     og_image=_fig(site, art), schemas=schemas,
                     keywords=", ".join([art.get("primary_keyword", "")] +
                                        art.get("secondary_keywords", [])))
        ctx.update(article=art, body_html=body_html, toc=toc, figure=figure,
                   calc=_calc_context(art, tcfg, site), faq=art.get("faq") or [],
                   category_name=category_name, reading_time=_reading_time(art.get("word_count", 0)),
                   related=related,
                   pager={"prev": {"slug": prev_art["slug"], "title": prev_art["title"]} if prev_art else None,
                          "next": {"slug": next_art["slug"], "title": next_art["title"]} if next_art else None})
        _write(SITE / art["slug"] / "index.html",
               env.get_template("article.html").render(**ctx))

    # --- categories ---
    for c in categories:
        items = [a for a in published if a.get("cluster") == c["id"]]
        pillars = [a for a in items if a.get("is_pillar")]
        others = [a for a in items if not a.get("is_pillar")]
        og = _thumb(site, pillars[0]) if pillars else (_thumb(site, items[0]) if items else _abs(site, "/static/img/og-default.png"))
        ctx = common(title=f"{c['name']} Calculator & Guides | {site['name']}",
                     description=(c["blurb"] + " Free, instant calculators with the formula shown.")[:155],
                     canonical=_abs(site, f"/category/{c['id']}/"), og_image=og,
                     schemas=[json.dumps(seolib.collection_schema(
                         c, items, site), ensure_ascii=False)])
        ctx.update(category=c,
                   pillars=[_card_meta(site, a, c["name"]) for a in pillars],
                   others=[_card_meta(site, a, c["name"]) for a in others])
        _write(SITE / "category" / c["id"] / "index.html",
               env.get_template("category.html").render(**ctx))

    # --- homepage ---
    pillars = [a for a in published if a.get("is_pillar")][:8]
    ctx = common(title=f"{site['name']} — Free Home & Garden Calculators",
                 description=("Free mulch, soil, topsoil, gravel, fertilizer, paint, tile, seed and "
                              "concrete calculators. Instant answers with the formula shown."),
                 canonical=_abs(site, "/"),
                 schemas=[json.dumps(seolib.website_schema(site), ensure_ascii=False)])
    ctx.update(categories=categories, articles=published[:12],
               article_count=len(published), category_count=len(categories),
               pillar_cards=[_card_meta(site, a) for a in pillars])
    _write(SITE / "index.html", env.get_template("index.html").render(**ctx))

    # --- legal / info pages ---
    pages = [
        ("about", "About", "Who we are and how our calculators work."),
        ("contact", "Contact", "Get in touch with the team."),
        ("privacy-policy", "Privacy Policy", "How we handle data and cookies."),
        ("terms", "Terms of Use", "The terms for using this site."),
        ("disclaimer", "Disclaimer", "Important limitations of our calculators."),
    ]
    for slug, title, desc in pages:
        src = CONTENT / "pages" / f"{slug}.md"
        body = src.read_text(encoding="utf-8") if src.exists() else f"# {title}\n\nComing soon."
        body = (body.replace("{{SITE_NAME}}", site["name"])
                    .replace("{{CONTACT_EMAIL}}", site.get("contact_email", ""))
                    .replace("{{CONTACT_BLOCK}}", _contact_block(site)))
        body = re.sub(r"\A\s*#\s+.*?\n", "", body)
        ctx = common(title=f"{title} | {site['name']}", description=desc[:155],
                     canonical=_abs(site, f"/{slug}/"),
                     schemas=[json.dumps(seolib.webpage_schema(title, desc, _abs(site, f"/{slug}/"), site),
                                         ensure_ascii=False)])
        ctx.update(page={"title": title, "html": mdrender.render(body)})
        _write(SITE / slug / "index.html", env.get_template("page.html").render(**ctx))

    # --- search (client-side; backs the WebSite SearchAction) ---
    search_index = [{"t": a["title"], "s": a["slug"], "k": a.get("primary_keyword", ""),
                     "c": cat_map.get(a.get("cluster", ""), {}).get("name", ""),
                     "d": a.get("meta_description", "")} for a in published]
    ctx = common(title=f"Search | {site['name']}",
                 description="Search GardenCalc's mulch, soil, gravel and other calculators.",
                 canonical=_abs(site, "/search/"), robots="noindex, follow")
    ctx.update(page={"title": "Search calculators & guides",
                     "html": '<div id="search-ui"><input type="search" id="q" '
                             'placeholder="Search calculators and guides…" aria-label="Search">'
                             '<ul id="results" class="post-list"></ul></div>',
                     "search": True})
    _write(SITE / "search" / "index.html", env.get_template("page.html").render(**ctx))

    # --- 404 ---
    ctx = common(title=f"Page not found | {site['name']}",
                 description="The page you requested was not found.",
                 canonical=_abs(site, "/404.html"), robots="noindex, follow")
    ctx.update(page={"title": "Page not found",
                     "html": "<p>That page does not exist. Try the <a href='/'>homepage</a>.</p>"})
    _write(SITE / "404.html", env.get_template("page.html").render(**ctx))

    # --- static (copied first so generated figures sit in site/static) ---
    static_dest = SITE / "static"
    if static_dest.exists():
        shutil.rmtree(static_dest)
    shutil.copytree(STATIC, static_dest)

    # Generate original figures into the copied static dir so pages can link them.
    img_stats = images.generate(published, static_dest)
    _write(static_dest / "search-index.json", json.dumps(search_index, ensure_ascii=False))

    # --- sitemap, robots, rss, CNAME ---
    urls = [{"loc": "/", "priority": "1.0", "lastmod": dt.date.today().isoformat(),
             "image": _thumb(site, published[0]) if published else None,
             "image_title": site["name"]}]
    urls += [{"loc": f"/category/{c['id']}/", "priority": "0.8"} for c in categories]
    urls += [{"loc": f"/{a['slug']}/", "priority": "0.9", "lastmod": a.get("updated"),
              "image": _fig(site, a), "image_title": a["title"]} for a in published]
    urls += [{"loc": f"/{s}/", "priority": "0.3"} for s, _, _ in pages]
    _write(SITE / "sitemap.xml", seolib.sitemap_xml(urls, site))
    _write(SITE / "robots.txt", seolib.robots_txt(site, _abs(site, "/sitemap.xml")))
    _write(SITE / "rss.xml", seolib.rss_xml(published, site))
    if site.get("custom_domain"):
        _write(SITE / "CNAME", site["custom_domain"] + "\n")
    _write(SITE / ".nojekyll", "")

    _generate_og_images(published, site)

    indexnow_key = str(site.get("indexnow_key", "")).strip()
    if indexnow_key:
        _write(SITE / f"{indexnow_key}.txt", indexnow_key)

    stats = {
        "built": dt.datetime.now(dt.timezone.utc).isoformat(),
        "articles": len(published),
        "categories": len(categories),
        "pages": len(pages) + 1,
        "urls": len(urls),
        "figures": img_stats.get("figures", 0),
    }
    save_json(DATA / "build.json", stats)
    print(f"[build] {stats}")
    return stats


def _generate_og_images(arts: list[dict], site: dict) -> None:
    """Lightweight SVG social images (no external service, no cost)."""
    out = SITE / "static" / "img" / "og"
    out.mkdir(parents=True, exist_ok=True)

    def card(title: str, sub: str) -> str:
        t = title[:70].replace("&", "&amp;").replace("<", "&lt;")
        s = sub[:90].replace("&", "&amp;").replace("<", "&lt;")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">'
                f'<rect width="1200" height="630" fill="#14532d"/>'
                f'<rect x="40" y="40" width="1120" height="550" fill="#166534" rx="24"/>'
                f'<text x="90" y="300" font-family="Georgia,serif" font-size="54" fill="#f0fdf4">{t}</text>'
                f'<text x="90" y="380" font-family="Arial" font-size="30" fill="#bbf7d0">{s}</text>'
                f'<text x="90" y="540" font-family="Arial" font-size="26" fill="#86efac">{site["name"]}</text>'
                f'</svg>')

    _write(out / ".." / "og-default.svg", card(site["name"], site.get("tagline", "")))
    for a in arts:
        _write(out / f"{a['slug']}.svg", card(a["title"], a["meta_description"]))


if __name__ == "__main__":
    build()
