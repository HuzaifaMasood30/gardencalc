"""Site health checks: broken links, missing tags, duplicates, orphans, sitemap."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from common import DATA, SITE, load_json, save_json, site_config


def _pages() -> list[Path]:
    return [p for p in SITE.rglob("*.html")] if SITE.exists() else []


def check() -> dict:
    site = site_config()
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    host = urlparse(base).netloc
    base_path = urlparse(base).path.rstrip("/")  # e.g. /gardencalc on project pages
    issues: list[dict] = []

    def normalize(path: str) -> str:
        """Strip the base path so URLs compare against site-root-relative paths."""
        if base_path and path.startswith(base_path):
            path = path[len(base_path):]
        path = "/" + path.lstrip("/")
        if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
            path += "/"
        return path

    titles, metas, descs = {}, {}, {}

    # Map of site-root-relative URLs that exist.
    existing = {"/"}
    for p in _pages():
        rel = p.relative_to(SITE).as_posix()
        if rel.endswith("/index.html"):
            existing.add("/" + rel[: -len("index.html")])
        existing.add("/" + rel)

    for p in _pages():
        html = p.read_text(encoding="utf-8")
        rel = "/" + p.relative_to(SITE).as_posix().replace("index.html", "")

        # noindex pages (embed widgets, search, 404) are not canonical landing pages:
        # they are allowed a description-less head and a canonical pointing elsewhere.
        # Merged-page stubs are the same: they canonical to their target by design.
        noindex = 'content="noindex' in html
        is_stub = 'http-equiv="refresh"' in html

        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if not m or not m.group(1).strip():
            issues.append({"type": "missing_title", "page": rel})
        elif not is_stub:
            # Redirect stubs share titles/descriptions with their target by design.
            titles.setdefault(m.group(1).strip(), []).append(rel)

        d = re.search(r'name="description" content="(.*?)"', html, re.S)
        if not d or not d.group(1).strip():
            if not noindex:
                issues.append({"type": "missing_meta_description", "page": rel})
        elif not is_stub:
            metas.setdefault(d.group(1).strip(), []).append(rel)
            descs[rel] = d.group(1).strip()

        c = re.search(r'rel="canonical" href="(.*?)"', html)
        if not c:
            issues.append({"type": "missing_canonical", "page": rel})
        elif not noindex and not is_stub and c.group(1).rstrip("/") != (base + rel.rstrip("/")):
            issues.append({"type": "canonical_mismatch", "page": rel,
                           "canonical": c.group(1)})

        if len(re.findall(r"<h1", html)) != 1:
            issues.append({"type": "h1_count",
                           "page": rel, "count": len(re.findall(r"<h1", html))})

        # internal links
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith("#") or href.startswith("mailto:"):
                continue
            if href.startswith("http"):
                if urlparse(href).netloc != host:
                    continue
                path = urlparse(href).path
            else:
                path = href
            if "/static/" in path or path.endswith((".xml", ".txt")):
                continue
            path = normalize(path)
            if path not in existing:
                issues.append({"type": "broken_internal_link", "page": rel, "href": path})

    # duplicate titles / descriptions
    for t, pages in titles.items():
        if len(pages) > 1:
            issues.append({"type": "duplicate_title", "title": t, "pages": pages})
    for d, pages in metas.items():
        if len(pages) > 1:
            issues.append({"type": "duplicate_meta_description", "description": d[:60],
                           "pages": pages})

    # orphan articles (no inbound internal link)
    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]
    inbound = {l["to"] for a in arts for l in a.get("internal_links", [])}
    for a in arts:
        if a["slug"] not in inbound:
            issues.append({"type": "orphan_article", "page": "/" + a["slug"] + "/"})

    # sitemap present + full Google-compliance checks
    sm = SITE / "sitemap.xml"
    if not sm.exists():
        issues.append({"type": "missing_sitemap", "page": "/sitemap.xml"})
    else:
        xml = sm.read_text(encoding="utf-8")
        # must be well-formed XML with the sitemap namespace and no BOM
        if xml.startswith("\ufeff") or "<urlset" not in xml:
            issues.append({"type": "invalid_sitemap", "page": "/sitemap.xml"})
        try:
            from xml.etree import ElementTree as _ET
            root = _ET.fromstring(xml)
            ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
            if root.tag != ns + "urlset":
                issues.append({"type": "invalid_sitemap_namespace",
                               "page": "/sitemap.xml"})
            sitemap_locs = [e.findtext(ns + "loc") or "" for e in root.iter(ns + "url")]
        except _ET.ParseError:
            issues.append({"type": "malformed_sitemap", "page": "/sitemap.xml"})
            sitemap_locs = []
        if len(sitemap_locs) != len(set(sitemap_locs)):
            issues.append({"type": "duplicate_sitemap_url", "page": "/sitemap.xml"})
        # Every sitemap URL must sit under the deployed base path (never the bare host).
        for loc in sitemap_locs:
            if not (loc == base or loc.startswith(base + "/")):
                issues.append({"type": "sitemap_wrong_host", "url": loc})
            path = urlparse(loc).path
            if path.endswith((".xml", ".txt")):
                continue
            if normalize(path) not in existing:
                issues.append({"type": "sitemap_url_missing", "url": loc})
        # A noindex page must never be advertised in the sitemap.
        for loc in sitemap_locs:
            p = SITE / normalize(urlparse(loc).path).lstrip("/") / "index.html"
            if p.exists() and "noindex" in p.read_text(encoding="utf-8"):
                issues.append({"type": "noindex_url_in_sitemap", "url": loc})

    if not (SITE / "robots.txt").exists():
        issues.append({"type": "missing_robots", "page": "/robots.txt"})

    by_type: dict[str, int] = {}
    for i in issues:
        by_type[i["type"]] = by_type.get(i["type"], 0) + 1

    result = {"pages": len(_pages()), "issues_total": len(issues),
              "by_type": by_type, "issues": issues}
    save_json(DATA / "health.json", result)
    return result


if __name__ == "__main__":
    import sys
    r = check()
    print(json.dumps({k: v for k, v in r.items() if k != "issues"}, indent=2))
    for i in r["issues"][:40]:
        print(" -", i)
    # Non-zero exit so CI gates (health check, deploy) actually block on a bad build.
    sys.exit(1 if r["issues_total"] else 0)
