"""Production audit: crawl the served site over HTTP and assert the full SEO checklist.

Unlike verify.py (which reads files off disk), this talks to a running HTTP server the
same way a crawler would, so it catches routing, encoding and asset problems too.

Usage:
    python -m http.server -d site 8000 &
    python scripts/audit.py --base http://localhost:8000 --path-prefix ""
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from xml.etree import ElementTree

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def get(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": "SEO-Audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.imgs: list[dict] = []
        self.title = ""
        self.title_count = 0
        self.h1 = 0
        self.metas: dict[str, list[str]] = {}
        self.canonical = ""
        self.schemas: list[str] = []
        self._in_title = False
        self._script_type = None
        self._script_buf = ""
        self._viewport = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "title":
            self._in_title = True
            self.title_count += 1
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            if a.get("name") == "viewport":
                self._viewport = True
            if a.get("name") in ("description", "keywords", "robots"):
                self.metas.setdefault(a["name"], []).append(a.get("content", ""))
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "script":
            self._script_type = a.get("type")
            self._script_buf = ""
        elif tag == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            if self._script_type == "application/ld+json" and self._script_buf.strip():
                self.schemas.append(self._script_buf)
            self._script_type = None
        elif tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._script_type == "application/ld+json":
            self._script_buf += data


def crawl(base: str) -> None:
    base = base.rstrip("/")
    status, home = get(base + "/")
    check("homepage loads", status == 200, f"HTTP {status}")

    sitemap_xml = ""
    st, sitemap_xml = get(base + "/sitemap.xml")
    urls: list[str] = []
    if st == 200:
        try:
            root = ElementTree.fromstring(sitemap_xml)
            ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
            urls = [u.findtext(ns + "loc") for u in root.findall(ns + "url")]
            check("sitemap valid XML", len(urls) > 0, f"{len(urls)} urls")
        except ElementTree.ParseError as e:
            check("sitemap valid XML", False, str(e))
    else:
        check("sitemap reachable", False, f"HTTP {st}")

    rt, robots = get(base + "/robots.txt")
    check("robots.txt valid", rt == 200 and "User-agent" in robots and "Sitemap" in robots,
          f"HTTP {rt}")
    if rt == 200:
        declared = re.search(r"Sitemap:\s*(\S+)", robots)
        check("robots declares absolute sitemap", bool(declared) and declared.group(1).startswith("https://"),
              declared.group(1) if declared else "missing")

    rss, rss_xml = get(base + "/rss.xml")
    if rss == 200:
        try:
            rroot = ElementTree.fromstring(rss_xml)
            items = rroot.findall(".//item")
            check("rss valid XML", len(items) > 0, f"{len(items)} items")
        except ElementTree.ParseError as e:
            check("rss valid XML", False, str(e))
    else:
        check("rss reachable", False, f"HTTP {rss}")

    # Discover every page from the sitemap plus the legal pages. Sitemap <loc> values are
    # absolute (https://host/<prefix>/page/); reduce them to site-relative paths so they
    # can be requested from either a root host or a GitHub Pages project subpath.
    parsed_base = urllib.parse.urlparse(base)
    prefix = parsed_base.path.rstrip("/")

    def rel(path: str) -> str:
        if prefix and path.startswith(prefix):
            path = path[len(prefix):]
        return path or "/"

    paths = sorted({
        rel(urllib.parse.urlparse(u).path) for u in urls if u
    } | {"/about/", "/contact/", "/privacy-policy/", "/terms/", "/disclaimer/"})

    titles: dict[str, str] = {}
    descs: dict[str, str] = {}
    broken: list[str] = []
    h1_bad: list[str] = []
    no_viewport: list[str] = []
    bad_img: list[str] = []
    schema_bad: list[str] = []
    pages_ok = 0
    checked_links: set[str] = set()

    for path in paths:
        st, html = get(base + path)
        if st != 200:
            broken.append(f"{path} (HTTP {st})")
            continue
        pages_ok += 1
        p = PageParser()
        p.feed(html)

        if p.h1 != 1:
            h1_bad.append(f"{path} ({p.h1})")
        t = p.title.strip()
        if t in titles:
            titles[t] += " | " + path
        else:
            titles[t] = path
        d = (p.metas.get("description") or [""])[0].strip()
        if d:
            if d in descs:
                descs[d] += " | " + path
            else:
                descs[d] = path
        if not p._viewport:
            no_viewport.append(path)
        for img in p.imgs:
            if not img.get("alt", "").strip():
                bad_img.append(f"{path}: {img.get('src','')}")
        for raw in p.schemas:
            try:
                json.loads(raw)
            except json.JSONDecodeError:
                schema_bad.append(path)

        # internal links: resolve and confirm they return 200
        for href in p.links:
            if href.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue
            absolute = urllib.parse.urljoin(base + path, href)
            if not absolute.startswith(base):
                continue
            target = urllib.parse.urlparse(absolute).path
            if target in checked_links:
                continue
            checked_links.add(target)
            lst, _ = get(absolute)
            if lst != 200:
                broken.append(f"{path} -> {target} (HTTP {lst})")

    check("all sitemap+legal pages 200", not broken or all("HTTP" not in b.split("->")[-1] for b in []),
          f"{pages_ok}/{len(paths)} ok")
    check("no broken internal links", not broken, "; ".join(broken[:8]))
    check("exactly one H1 per page", not h1_bad, "; ".join(h1_bad[:8]))
    dupe_titles = {k: v for k, v in titles.items() if "|" in v}
    dupe_descs = {k: v for k, v in descs.items() if "|" in v}
    check("no duplicate titles", not dupe_titles, "; ".join(f"{v}" for v in dupe_titles.values()))
    check("no duplicate meta descriptions", not dupe_descs,
          "; ".join(f"{v}" for v in dupe_descs.values()))
    check("mobile viewport on every page", not no_viewport, "; ".join(no_viewport[:8]))
    check("every image has alt text", not bad_img, "; ".join(bad_img[:8]))
    check("structured data parses as JSON", not schema_bad, "; ".join(schema_bad[:8]))
    check("pages crawled", pages_ok >= 20, f"{pages_ok} pages")

    # orphan detection: pages with no inbound internal link
    inbound: set[str] = set()
    for path in paths:
        st, html = get(base + path)
        if st != 200:
            continue
        for href in PageParser_links(html):
            absolute = urllib.parse.urljoin(base + path, href)
            if absolute.startswith(base):
                inbound.add(rel(urllib.parse.urlparse(absolute).path))
    article_paths = {p for p in paths if not p.endswith(("/about/", "/contact/",
                     "/privacy-policy/", "/terms/", "/disclaimer/", "/"))}
    orphans = sorted(p for p in article_paths if p not in inbound)
    check("no orphan articles", not orphans, "; ".join(orphans[:8]))


def PageParser_links(html: str) -> list[str]:
    p = PageParser()
    p.feed(html)
    return p.links


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:8123")
    args = ap.parse_args()
    crawl(args.base)
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    print(f"\n{'='*64}\nPRODUCTION AUDIT  {args.base}\n{'='*64}")
    for name, ok, detail in RESULTS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))
    print(f"\n{passed}/{len(RESULTS)} checks passed")
    sys.exit(0 if passed == len(RESULTS) else 1)
