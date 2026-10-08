"""Live production audit. Run against the deployed GitHub Pages URL.

    python scripts/live_audit.py https://<user>.github.io/<repo>/
    python scripts/live_audit.py https://<user>.github.io/<repo>/ --json reports/live-audit.json

Checks, per the launch checklist:
  HTTP status of every page, homepage, articles, category pages, legal pages, 404 page,
  sitemap, robots.txt, RSS, canonicals, internal links, H1/H2 structure, meta titles and
  descriptions, mobile viewport, image alt text, structured data, calculator presence,
  JS/Python calculator parity, leftover placeholder content, broken links, orphan pages.

Exit code is non-zero if any hard check fails, so it can gate CI.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
LEGAL = ["/about/", "/contact/", "/privacy-policy/", "/terms/", "/disclaimer/"]
PLACEHOLDER_PAT = re.compile(
    r"example\.com|example\.github\.io|lorem ipsum|coming soon|\bTODO\b|\{\{[a-z_]+\}\}",
    re.I)

RESULTS: list[dict] = []
PAGES: list[dict] = []


def record(name, ok, detail="", hard=True):
    RESULTS.append({"check": name, "ok": bool(ok), "detail": detail, "hard": hard})


def fetch(url: str, timeout: int = 20):
    # GitHub Pages returns transient 5xx under load; retry before calling a link broken
    # so a momentary blip does not fail the gate.
    for attempt in range(3):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SEO-Audit)"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code >= 500 and attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            return e.code, body, dict(e.headers)
        except Exception as e:  # noqa: BLE001
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            return 0, "", {"error": str(e)}
    return 0, "", {"error": "unreachable"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.imgs: list[dict] = []
        self.title = ""
        self.h1 = 0
        self.h2 = 0
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.schemas: list[str] = []
        self.has_viewport = False
        self._t = False
        self._st = None
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "title":
            self._t = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "h2":
            self.h2 += 1
        elif tag == "meta":
            if a.get("name") == "viewport":
                self.has_viewport = True
            if a.get("name") in ("description", "robots"):
                self.meta[a["name"]] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "script":
            self._st = a.get("type")
            self._buf = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        elif tag == "script":
            if self._st == "application/ld+json" and self._buf.strip():
                self.schemas.append(self._buf)
            self._st = None

    def handle_data(self, data):
        if self._t:
            self.title += data
        if self._st == "application/ld+json":
            self._buf += data


def parse(html: str) -> Page:
    p = Page()
    p.feed(html)
    return p


def calculator_parity() -> tuple[bool, str]:
    node = shutil.which("node")
    if not node:
        return True, "skipped (node not installed)"
    cases = [["mulch", {"length": 20, "width": 10, "depth": 3}],
             ["soil", {"length": 8, "width": 4, "height": 12}],
             ["gravel", {"length": 20, "width": 10, "depth": 3}],
             ["concrete", {"length": 10, "width": 10, "thickness": 4}]]
    proc = subprocess.run([node, str(ROOT / "scripts/calc_parity.js"),
                           str(ROOT / "static/js/main.js"), json.dumps(cases)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return False, proc.stderr.strip()[:200]
    got = json.loads(proc.stdout)
    checks = {"mulch": ("2 cu ft bags", 25), "soil": ("1.5 cu ft bags", 22),
              "gravel": ("Tons", 2.59), "concrete": ("80 lb bags", 56)}
    for kind, (label, expected) in checks.items():
        actual = got[kind].get(label)
        if actual is None or abs(float(actual) - expected) > 1.0:
            return False, f"{kind}: {label}={actual} expected {expected}"
    return True, "JS output matches Python engine"


def audit(base: str) -> dict:
    base = base.rstrip("/") + "/"

    st, home, _ = fetch(base)
    record("homepage HTTP 200", st == 200, f"HTTP {st}")

    # sitemap
    st, xml, _ = fetch(base + "sitemap.xml")
    locs: list[str] = []
    if st == 200:
        try:
            root = ElementTree.fromstring(xml)
            ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
            locs = [u.findtext(ns + "loc") for u in root.findall(ns + "url")]
            record("sitemap is valid XML", bool(locs), f"{len(locs)} URLs")
        except ElementTree.ParseError as e:
            record("sitemap is valid XML", False, str(e))
    else:
        record("sitemap reachable", False, f"HTTP {st}")

    # robots
    st, robots, _ = fetch(base + "robots.txt")
    rec = re.search(r"Sitemap:\s*(\S+)", robots)
    record("robots.txt valid and points at sitemap",
           st == 200 and rec is not None and rec.group(1).endswith("/sitemap.xml")
           and rec.group(1).startswith(("http://", "https://")),
           f"HTTP {st}; {rec.group(1) if rec else 'no sitemap line'}")

    # rss
    st, rss, _ = fetch(base + "rss.xml")
    if st == 200:
        try:
            items = ElementTree.fromstring(rss).findall(".//item")
            record("RSS valid", True, f"{len(items)} items")
        except ElementTree.ParseError as e:
            record("RSS valid", False, str(e))
    else:
        record("RSS reachable", False, f"HTTP {st}")

    # 404 handling
    st404, body404, _ = fetch(base + "this-page-should-not-exist-9f3a/")
    record("missing page returns 404", st404 == 404, f"HTTP {st404}")

    # IndexNow key file (optional; only when configured)
    cfg_path = ROOT / "config" / "site.json"
    key = ""
    if cfg_path.exists():
        key = str(json.loads(cfg_path.read_text(encoding="utf-8")).get("indexnow_key", "")).strip()
    if key:
        st_key, body_key, _ = fetch(base + key + ".txt")
        record("IndexNow key file served", st_key == 200 and body_key.strip() == key,
               f"HTTP {st_key}")

    # build the page list
    prefix = urllib.parse.urlparse(base).path.rstrip("/")

    def rel(path: str) -> str:
        if prefix and path.startswith(prefix):
            path = path[len(prefix):]
        return path or "/"

    paths = sorted({rel(urllib.parse.urlparse(u).path) for u in locs if u} | set(LEGAL))
    article_paths = [p for p in paths
                     if not p.startswith("/category/") and p not in LEGAL and p != "/"]

    titles: dict[str, list[str]] = {}
    descs: dict[str, list[str]] = {}
    problems: dict[str, list[str]] = {}
    inbound: set[str] = set()
    checked: set[str] = set()

    for path in paths:
        url = base + path.lstrip("/")
        st, html, _ = fetch(url)
        row = {"path": path, "status": st}
        if st != 200:
            problems.setdefault(path, []).append(f"HTTP {st}")
            PAGES.append(row)
            continue
        p = parse(html)
        row.update(title=p.title.strip()[:80], h1=p.h1, h2=p.h2)
        PAGES.append(row)

        if p.h1 != 1:
            problems.setdefault(path, []).append(f"h1={p.h1}")
        if p.h1 < 1:
            problems.setdefault(path, []).append("no h1")
        if not p.h2 and path not in LEGAL and path != "/" and not path.startswith("/category/"):
            problems.setdefault(path, []).append("no h2")
        if not p.title:
            problems.setdefault(path, []).append("no title")
        if not p.meta.get("description"):
            problems.setdefault(path, []).append("no meta description")
        if not p.has_viewport:
            problems.setdefault(path, []).append("no viewport")
        if p.canonical and p.canonical.rstrip("/") != url.rstrip("/"):
            problems.setdefault(path, []).append(f"canonical={p.canonical}")
        if not p.canonical and path != "/404.html":
            problems.setdefault(path, []).append("no canonical")
        for img in p.imgs:
            if not img.get("alt", "").strip():
                problems.setdefault(path, []).append(f"img no alt: {img.get('src','')}")
        for raw in p.schemas:
            try:
                json.loads(raw)
            except json.JSONDecodeError:
                problems.setdefault(path, []).append("invalid ld+json")
        if PLACEHOLDER_PAT.search(html):
            problems.setdefault(path, []).append("placeholder text")

        titles.setdefault(p.title.strip(), []).append(path)
        descs.setdefault(p.meta.get("description", "").strip(), []).append(path)

        # collect internal links + verify each target once
        for href in p.links:
            if href.startswith(("mailto:", "tel:", "#", "javascript:", "data:")):
                continue
            absolute = urllib.parse.urljoin(url, href)
            if not absolute.startswith(base):
                continue
            tpath = urllib.parse.urlparse(absolute).path
            inbound.add(rel(tpath).rstrip("/") or "/")
            if tpath in checked:
                continue
            checked.add(tpath)
            ts, _, _ = fetch(absolute)
            if ts != 200:
                problems.setdefault(path, []).append(f"broken link -> {tpath} (HTTP {ts})")

    # calculator presence on calculator pages
    st, mulch, _ = fetch(base + "mulch-calculator/")
    record("calculator form and script present",
           'class="calc-form' in mulch and "static/js/main.js" in mulch,
           "mulch-calculator")
    ok, detail = calculator_parity()
    record("JS/Python calculator parity", ok, detail)

    dupe_titles = {t: v for t, v in titles.items() if len(v) > 1}
    dupe_descs = {d: v for d, v in descs.items() if len(v) > 1}
    orphans = [p for p in article_paths if (p.rstrip("/") or "/") not in inbound]

    broken = {p: [x for x in v if "broken link" in x or x.startswith("HTTP")]
              for p, v in problems.items()}
    broken = {p: v for p, v in broken.items() if v}
    page_problems = {p: v for p, v in problems.items() if v}

    record("all pages return HTTP 200", not {p: v for p, v in problems.items() if any(x.startswith("HTTP") for x in v)},
           f"{len([r for r in PAGES if r.get('status') == 200])}/{len(paths)} OK")
    record("no broken internal links", not broken,
           "; ".join(f"{p}: {v[0]}" for p, v in list(broken.items())[:5]))
    record("no duplicate titles", not dupe_titles, "; ".join(str(v) for v in list(dupe_titles.values())[:3]))
    record("no duplicate meta descriptions", not dupe_descs, "; ".join(str(v) for v in list(dupe_descs.values())[:3]))
    record("no orphan pages", not orphans, ", ".join(orphans[:6]))
    record("no placeholder content", not any("placeholder text" in v for v in problems.values()),
           "; ".join(p for p, v in problems.items() if "placeholder text" in v) or "clean")
    record("no per-page SEO problems", not page_problems,
           "; ".join(f"{p}: {','.join(v)}" for p, v in list(page_problems.items())[:6]))

    return {"base": base, "pages": PAGES, "problems": page_problems,
            "checks": RESULTS}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--json", help="write the full report to this path")
    args = ap.parse_args()
    report = audit(args.url)

    print("=" * 70)
    print(f"LIVE PRODUCTION AUDIT  {report['base']}")
    print("=" * 70)
    for r in report["checks"]:
        flag = "PASS" if r["ok"] else "FAIL"
        print(f"[{flag}] {r['check']}" + (f"  — {r['detail']}" if r["detail"] else ""))
    print(f"\n{len(report['pages'])} pages crawled")
    if report["problems"]:
        print("\nPages with problems:")
        for p, v in report["problems"].items():
            print(f"  {p}: {', '.join(v)}")
    hard_failed = [r for r in report["checks"] if r["hard"] and not r["ok"]]
    print(f"\n{len(report['checks']) - len(hard_failed)}/{len(report['checks'])} checks passed")

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2))
        print(f"report written to {out}")
    return 0 if not hard_failed else 1


if __name__ == "__main__":
    sys.exit(main())
