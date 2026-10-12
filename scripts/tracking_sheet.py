"""Build a tracking sheet for Search Console.

One row per canonical, indexable URL, pre-filled with the page's target keyword and
title so the same sheet can be pasted straight into Google Search Console's
Performance report. The measurement columns start empty; fill them from GSC (or the
Bing Webmaster Tools API) each week.

    python scripts/tracking_sheet.py
    python scripts/tracking_sheet.py --out reports/tracking-sheet.csv

The sitemap is the source of truth for which URLs are live, so the sheet can never
drift from the deployed site.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from common import DATA, REPORTS, ROOT, site_config

MEASURE_COLUMNS = ["impressions", "clicks", "ctr", "avg_position", "indexed", "notes"]


def _sitemap_urls() -> list[str]:
    sm = ROOT / "site" / "sitemap.xml"
    if not sm.exists():
        return []
    return re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))


def _keyword_map() -> dict[str, str]:
    arts = json.loads((DATA / "articles.json").read_text(encoding="utf-8"))
    return {f"/{a['slug']}/": a.get("primary_keyword", "") for a in arts}


def rows() -> list[dict]:
    base = str(site_config().get("base_url", "")).rstrip("/")
    keywords = _keyword_map()
    out = []
    for url in _sitemap_urls():
        path = "/" + url.split(base, 1)[-1].lstrip("/") if base and base in url else url
        out.append({
            "url": url,
            "path": path,
            "target_keyword": keywords.get(path, ""),
            **{c: "" for c in MEASURE_COLUMNS},
        })
    return out


def write_csv(path: Path) -> int:
    data = rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["url", "path", "target_keyword", *MEASURE_COLUMNS]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(data)
    return len(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPORTS / "tracking-sheet.csv"))
    args = ap.parse_args()
    n = write_csv(Path(args.out))
    print(f"[tracking] wrote {n} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
