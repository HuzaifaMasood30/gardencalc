"""Static site build. Reads data/articles.json + config, writes site/."""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

import mdrender
import seo as seolib
from common import (CONFIG, CONTENT, DATA, SITE, STATIC, TEMPLATES, load_json,
                    save_json, seo_config, site_config, topics_config)

YEAR = dt.date.today().year


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
    import os
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


def build() -> dict:
    site = site_config()
    seo = seo_config()
    tcfg = topics_config()
    arts = load_json(DATA / "articles.json", default=[])
    published = [a for a in arts
                 if a.get("status") in ("published", "approved")
                 and a.get("quality", {}).get("passed")]
    published.sort(key=lambda a: a.get("created", ""), reverse=True)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    slug_to_url = {a["slug"]: f"{_base(site)}/{a['slug']}/" for a in published}
    base = _base(site)
    categories = tcfg.get("clusters", [])
    cat_map = {c["id"]: c for c in categories}
    nav_categories = [{"id": c["id"], "name": c["name"]} for c in categories]

    # Human-readable blurbs for categories (used on home + category pages).
    blurbs = {
        "mulch": "Work out bags or cubic yards of mulch for any bed size and depth.",
        "soil": "Fill raised beds with the right amount of soil mix.",
        "gravel": "Calculate cubic yards and tons of gravel for paths and drives.",
        "paint": "Estimate gallons of paint per room, coats and openings.",
        "tile": "Count tiles and waste allowance for floors and walls.",
        "grass-seed": "Seed a new lawn or overseed an existing one at the right rate.",
        "concrete": "Get cubic yards and bag counts for slabs and footings.",
    }
    for c in categories:
        c["blurb"] = blurbs.get(c["id"], "Free calculators and practical guides.")

    env = _env()
    env.globals.update(base_url=base, site=site, year=YEAR,
                       nav_categories=nav_categories, calc_defs=tcfg.get("calculators", {}))

    def common(title, description, canonical, og_type="website", og_image=None,
               schemas=None, robots=None, keywords=None):
        return dict(title=title, description=description, canonical=canonical,
                    og_type=og_type, og_image=og_image or _abs(site, "/static/img/og-default.svg"),
                    schemas=schemas or [],
                    robots=robots or "index, follow, max-snippet:-1, max-image-preview:large",
                    keywords=keywords, base_url=base)

    # --- articles ---
    for art in published:
        body_html = mdrender.render(art.get("body_markdown", ""), slug_to_url)
        schemas = [json.dumps(s, ensure_ascii=False)
                   for s in seolib.all_schema(art, site)]
        ctx = common(title=art["title"], description=art["meta_description"],
                     canonical=_abs(site, f"/{art['slug']}/"), og_type="article",
                     og_image=_abs(site, f"/static/img/og/{art['slug']}.svg"),
                     schemas=schemas, keywords=", ".join(
                         [art.get("primary_keyword", "")] + art.get("secondary_keywords", [])))
        ctx.update(article=art, body_html=body_html, breadcrumb=art["title"])
        _write(SITE / art["slug"] / "index.html",
               env.get_template("article.html").render(**ctx))

    # --- categories ---
    for c in categories:
        items = [a for a in published if a.get("cluster") == c["id"]]
        ctx = common(title=f"{c['name']} Calculators & Guides | {site['name']}",
                     description=c["blurb"][:155],
                     canonical=_abs(site, f"/category/{c['id']}/"))
        ctx.update(category=c, articles=items)
        _write(SITE / "category" / c["id"] / "index.html",
               env.get_template("category.html").render(**ctx))

    # --- homepage ---
    ctx = common(title=f"{site['name']} — {site['tagline']}",
                 description=site["tagline"] + " Free, fast calculators for mulch, soil, gravel, paint, tile, seed and concrete.",
                 canonical=_abs(site, "/"),
                 schemas=[json.dumps(seolib.website_schema(site), ensure_ascii=False)])
    ctx.update(categories=categories, articles=published[:12])
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
        # The template supplies the h1; drop a leading markdown h1 to avoid a duplicate.
        body = re.sub(r"\A\s*#\s+.*?\n", "", body)
        ctx = common(title=f"{title} | {site['name']}", description=desc[:155],
                     canonical=_abs(site, f"/{slug}/"))
        ctx.update(page={"title": title, "html": mdrender.render(body)})
        _write(SITE / slug / "index.html", env.get_template("page.html").render(**ctx))

    # --- 404 ---
    ctx = common(title=f"Page not found | {site['name']}",
                 description="The page you requested was not found.",
                 canonical=_abs(site, "/404.html"), robots="noindex, follow")
    ctx.update(page={"title": "Page not found",
                     "html": "<p>That page does not exist. Try the <a href='/'>homepage</a>.</p>"})
    _write(SITE / "404.html", env.get_template("page.html").render(**ctx))

    # --- sitemap, robots, rss, CNAME ---
    urls = [{"loc": "/", "priority": "1.0",
             "lastmod": dt.date.today().isoformat()}]
    urls += [{"loc": f"/category/{c['id']}/", "priority": "0.8"} for c in categories]
    urls += [{"loc": f"/{a['slug']}/", "priority": "0.9", "lastmod": a.get("updated")}
             for a in published]
    urls += [{"loc": f"/{s}/", "priority": "0.3"} for s, _, _ in pages]
    _write(SITE / "sitemap.xml", seolib.sitemap_xml(urls, site))
    _write(SITE / "robots.txt", seolib.robots_txt(site, _abs(site, "/sitemap.xml")))
    _write(SITE / "rss.xml", seolib.rss_xml(published, site))
    if site.get("custom_domain"):
        _write(SITE / "CNAME", site["custom_domain"] + "\n")
    _write(SITE / ".nojekyll", "")

    # --- static ---
    if (SITE / "static").exists():
        shutil.rmtree(SITE / "static")
    shutil.copytree(STATIC, SITE / "static")
    _generate_og_images(published, site)

    stats = {
        "built": dt.datetime.now(dt.timezone.utc).isoformat(),
        "articles": len(published),
        "categories": len(categories),
        "pages": len(pages) + 1,
        "urls": len(urls),
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
