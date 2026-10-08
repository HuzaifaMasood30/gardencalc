"""SEO helpers: JSON-LD schema, sitemap, robots, RSS, canonical and breadcrumbs."""
from __future__ import annotations

import datetime as dt
import html
import re

from common import site_config, slugify


def _abs(site: dict, path: str) -> str:
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    return base + "/" + path.lstrip("/")


def article_schema(art: dict, site: dict, figure: str | None = None) -> dict:
    url = _abs(site, f"/{art['slug']}/")
    img = figure or _abs(site, f"/static/img/og/{art['slug']}.svg")
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": art["title"][:110],
        "description": art.get("meta_description", ""),
        "datePublished": art.get("created"),
        "dateModified": art.get("updated"),
        "author": {"@type": "Organization", "name": site.get("author", site["name"]),
                   "url": _abs(site, site.get("author_url", "/about/"))},
        "publisher": {"@type": "Organization", "name": site["name"],
                      "logo": {"@type": "ImageObject", "url": _abs(site, site.get("org_logo", ""))}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": {"@type": "ImageObject", "url": img, "width": 1200, "height": 675},
        "articleSection": art.get("cluster", ""),
        "keywords": ", ".join([art.get("primary_keyword", "")] + art.get("secondary_keywords", [])),
    }


def collection_schema(cat: dict, items: list[dict], site: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{cat['name']} calculators & guides",
        "description": cat.get("blurb", ""),
        "url": _abs(site, f"/category/{cat['id']}/"),
        "isPartOf": {"@type": "WebSite", "name": site["name"], "url": _abs(site, "/")},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": a["title"],
                 "url": _abs(site, f"/{a['slug']}/")}
                for i, a in enumerate(items[:20])
            ],
        },
    }


def webpage_schema(title: str, description: str, url: str, site: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": url,
        "isPartOf": {"@type": "WebSite", "name": site["name"], "url": _abs(site, "/")},
    }


def faq_schema(art: dict) -> dict | None:
    faqs = art.get("faq") or []
    if not faqs:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in faqs
        ],
    }


def howto_schema(art: dict, site: dict) -> dict:
    """Steps taken from the 'How to Calculate' section."""
    steps = [
        "Measure the length and width in feet and multiply them to get the area.",
        "Decide the depth the job needs, in inches.",
        "Convert depth to feet by dividing by 12.",
        "Multiply area by depth in feet to get cubic feet.",
        "Convert to cubic yards or bags using the calculator.",
    ]
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to calculate {art.get('primary_keyword', '')}",
        "description": art.get("meta_description", ""),
        "step": [{"@type": "HowToStep", "position": i + 1, "text": s}
                 for i, s in enumerate(steps)],
    }


def breadcrumb_schema(art: dict, site: dict) -> dict:
    items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": _abs(site, "/")},
    ]
    if art.get("cluster"):
        items.append({"@type": "ListItem", "position": 2, "name": art["cluster"].title(),
                      "item": _abs(site, f"/category/{art['cluster']}/")})
    items.append({"@type": "ListItem", "position": len(items) + 1, "name": art["title"],
                  "item": _abs(site, f"/{art['slug']}/")})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}


def website_schema(site: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site["name"],
        "url": _abs(site, "/"),
        "description": site.get("tagline", ""),
        "potentialAction": {
            "@type": "SearchAction",
            "target": _abs(site, "/search/?q={search_term_string}"),
            "query-input": "required name=search_term_string",
        },
    }


def all_schema(art: dict, site: dict, figure: str | None = None) -> list[dict]:
    out = [article_schema(art, site, figure=figure), breadcrumb_schema(art, site),
           howto_schema(art, site)]
    faq = faq_schema(art)
    if faq:
        out.append(faq)
    return out


def sitemap_xml(urls: list[dict], site: dict) -> str:
    """urls: [{'loc':..., 'lastmod':..., 'priority':..., 'image':..., 'image_title':...}]"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(_abs(site, u['loc']))}</loc>")
        if u.get("lastmod"):
            lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        if u.get("priority"):
            lines.append(f"    <priority>{u['priority']}</priority>")
        if u.get("image"):
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{html.escape(u['image'])}</image:loc>")
            if u.get("image_title"):
                lines.append(f"      <image:title>{html.escape(u['image_title'])}</image:title>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def robots_txt(site: dict, sitemap_url: str) -> str:
    return (f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n")


def rss_xml(arts: list[dict], site: dict) -> str:
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    now = dt.datetime.now(dt.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for a in arts[:50]:
        items.append(
            f"  <item>\n"
            f"    <title>{html.escape(a['title'])}</title>\n"
            f"    <link>{base}/{a['slug']}/</link>\n"
            f"    <guid>{base}/{a['slug']}/</guid>\n"
            f"    <description>{html.escape(a.get('meta_description',''))}</description>\n"
            f"  </item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            f"  <title>{html.escape(site['name'])}</title>\n"
            f"  <link>{base}/</link>\n"
            f"  <description>{html.escape(site.get('tagline',''))}</description>\n"
            f"  <lastBuildDate>{now}</lastBuildDate>\n"
            + "\n".join(items) + "\n</channel></rss>\n")


def calculate_seo_score(art: dict, site: dict) -> dict:
    """Per-article SEO score used by the report and dashboard."""
    checks = {}
    checks["title"] = 15 <= len(art.get("title", "")) <= 60
    checks["meta"] = 110 <= len(art.get("meta_description", "")) <= 158
    checks["slug"] = bool(re.fullmatch(r"[a-z0-9-]+", art.get("slug", "")))
    checks["h1_once"] = not re.search(r"^#\s", art.get("body_markdown", ""), re.M)
    checks["has_faq"] = bool(art.get("faq"))
    checks["schema"] = bool(art.get("schema_types"))
    checks["links"] = len(art.get("internal_links", [])) >= 1
    checks["word_count"] = art.get("word_count", 0) >= 600
    checks["calculator"] = bool(art.get("calculator_output"))
    return {"score": round(sum(checks.values()) / len(checks) * 100, 1), "checks": checks}
