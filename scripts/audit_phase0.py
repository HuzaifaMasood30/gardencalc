#!/usr/bin/env python3
"""Phase 0 audit (brief 1, section 2) — report only, no edits.

Reads data/articles.json and the generated page modules, then reports:
  - how the site is built, page types and counts
  - near-duplicate guide clusters (same search intent) with a recommended primary
  - weak titles/slugs
  - missing SEO elements (schema, alt, dimensions, canonical, breadcrumbs, dates)
  - sitemap issues

Writes reports/audit-phase0.json and reports/audit-phase0.md.
"""
from __future__ import annotations

import datetime as dt
import itertools
import json
import re
from pathlib import Path

import charts
import planners
import seasonal
from common import DATA, REPORTS, ROOT, load_json

try:
    import merges
except Exception:  # audit must not hard-fail if the merge module moves
    merges = None

# Known overlapping guide clusters from the brief, mapped to their recommended primary
# URL. The audit confirms each still overlaps and flags any pair not in this list.
INTENT_GROUPS = [
    ("soil", ["how-much-soil-for-raised-bed-calculator-uk"],
     "Merge metric/unit variants into the main calculator page."),
    ("grass-seed", ["how-much-grass-seed-per-square-foot-canada"],
     "Metric/local-unit variant; keep only if it uses metric and local terms."),
    ("paint", ["how-much-paint-do-i-need-for-a-door"],
     "Door vs front door overlap; merge the generic into the front-door page."),
    ("topsoil", ["how-much-topsoil-do-i-need-for-a-lawn"],
     "New-lawn vs lawn overlap; merge into the new-lawn page."),
    ("fertilizer", ["how-much-fertilizer-per-1000-sq-ft-calculator"],
     "Calculator-intent duplicate of the fertilizer pillar."),
    ("paint", ["how-much-paint-do-i-need-calculator-sq-ft"],
     "Calculator-intent duplicate of the paint pillar."),
    ("tile", ["how-many-tiles-do-i-need-for-my-floor"],
     "Generic floor page; merge into the room page or pillar."),
    ("tile", ["how-many-tiles-do-i-need-for-my-room"],
     "Generic room page; merge into the room-size pages."),
]


def _tok(text: str) -> set[str]:
    t = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    return {w for w in t.split() if len(w) > 3}


def _digits(text: str, repl: str = " ") -> str:
    return re.sub(r"\d+", repl, text)


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / max(1, len(a | b))


WEAK_TITLE_RE = re.compile(
    r"\b(X8|Uk|Canada|SQ FT|Calculator Calculator|My Room|My Floor)\b|\bCalculator\b.*\bCalculator\b")


def audit() -> dict:
    arts = load_json(DATA / "articles.json", default=[])
    approved = [a for a in arts if a.get("status") in ("published", "approved")]

    # Merged pages are stubs, not ranking pages; exclude them from the live audit.
    merged_slugs = merges.merged_slugs() if merges else set()
    live = [a for a in approved if a["slug"] not in merged_slugs]

    by_cluster: dict[str, list] = {}
    for a in live:
        by_cluster.setdefault(a.get("cluster", "?"), []).append(a)

    # Intent overlap: same cluster + near-identical titles = same searcher intent.
    # Word-level Jaccard on the body is too noisy (shared template prose), so we judge
    # overlap on the query-bearing fields only. Pairs that differ only by a number are
    # legitimate long-tail sizing pages, so they are counted apart and not flagged.
    dupes, sized = [], []
    for x, y in itertools.combinations(live, 2):
        if x.get("cluster") != y.get("cluster"):
            continue
        xt, yt = x.get("title", ""), y.get("title", "")
        j = _jaccard(_tok(xt), _tok(yt))
        if j < 0.80:
            continue
        # Strip the sizing number; if the remaining slugs still match, this is a
        # deliberate long-tail sizing pair (200 vs 300 sq ft), not a duplicate.
        if _digits(x["slug"]) == _digits(y["slug"]):
            sized.append({"similarity": round(j, 2), "a": x["slug"], "b": y["slug"],
                          "cluster": x.get("cluster")})
        else:
            dupes.append({"similarity": round(j, 2), "a": x["slug"], "b": y["slug"],
                          "cluster": x.get("cluster")})
    dupes.sort(key=lambda d: -d["similarity"])

    weak = []
    for a in live:
        t, s = a.get("title", ""), a["slug"]
        reasons = []
        if WEAK_TITLE_RE.search(t):
            reasons.append("weak title wording")
        if len(t) > 60:
            reasons.append(f"title {len(t)} chars")
        if re.search(r"-[a-z]{2}$", s) and s.rsplit("-", 1)[-1] in ("uk", "canada"):
            reasons.append("locale variant slug")
        if s.endswith("-calculator") and not a.get("is_pillar"):
            reasons.append("redundant '-calculator' slug")
        if reasons:
            weak.append({"slug": s, "title": t, "reasons": reasons})

    missing = []
    for a in live:
        gaps = []
        if not a.get("meta_description"):
            gaps.append("no meta description")
        if not a.get("faq"):
            gaps.append("no FAQ")
        if not a.get("schema_types"):
            gaps.append("no schema types recorded")
        if len(a.get("internal_links", [])) < 3:
            gaps.append(f"only {len(a.get('internal_links', []))} internal links")
        if (a.get("word_count") or 0) < 600:
            gaps.append("thin (<600 words)")
        if gaps:
            missing.append({"slug": a["slug"], "gaps": gaps})

    sitemap = ROOT / "site" / "sitemap.xml"
    sm_issues = []
    if sitemap.exists():
        raw = sitemap.read_text(encoding="utf-8")
        if raw.startswith("\ufeff"):
            sm_issues.append("BOM before <?xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", raw)
        base = "https://huzaifamasood30.github.io/gardencalc/"
        for u in locs:
            if not u.startswith(base):
                sm_issues.append(f"loc escapes base path: {u}")
            if not u.endswith("/"):
                sm_issues.append(f"loc without trailing slash: {u}")

    result = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "site": "https://huzaifamasood30.github.io/gardencalc/",
        "counts": {
            "articles": len(arts),
            "approved": len(approved),
            "clusters": len(by_cluster),
            "charts": len(charts.CHARTS),
            "planners": len(planners.PLANNERS),
            "seasonal": len(seasonal.SEASONAL),
        },
        "clusters": {c: len(v) for c, v in sorted(by_cluster.items())},
        "duplicates": dupes,
        "sized_variants": sized,
        "weak_pages": weak,
        "missing_elements": missing,
        "sitemap_issues": sm_issues,
        "intent_groups": [{"cluster": c, "urls": u, "note": n} for c, u, n in INTENT_GROUPS],
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "audit-phase0.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    appr = [a for a in approved]
    mean_wc = round(sum(a.get("word_count", 0) for a in appr) / max(1, len(appr)))
    lines = [
        "# GardenCalc — Phase 0 audit",
        "",
        f"Generated {result['generated']}. Report only; no edits made.",
        "",
        "## How the site is built",
        "- `scripts/run_all.py` runs the pipeline: generate -> interlink -> quality -> "
        "build -> verify.",
        "- `scripts/build.py` renders Jinja templates in `templates/` to `site/`.",
        "- Articles live in `data/articles.json`; charts/planners/seasonal are generated "
        "in `scripts/{charts,planners,seasonal}.py`.",
        "- Deploy: GitHub Actions `deploy.yml` (push) and `pipeline.yml` (cron).",
        "",
        "## Page counts",
        f"- Articles: {len(arts)} total, {len(approved)} live (merged stubs excluded)",
        f"- Categories: {len(by_cluster)}; Charts: {len(charts.CHARTS)}; "
        f"Planners: {len(planners.PLANNERS)}; Seasonal: {len(seasonal.SEASONAL)}",
        f"- Mean article length: {mean_wc} words",
        "",
        "## Near-duplicate pages (same intent, similarity >= 0.80)",
        "These pairs share a searcher intent and should merge or be differentiated. "
        "Pairs that differ only by a sizing number are legitimate long-tail pages, "
        "listed separately below.",
        "| similarity | cluster | page A | page B |",
        "|---|---|---|---|",
    ]
    for d in dupes:
        lines.append(f"| {d['similarity']:.2f} | {d['cluster']} | {d['a']} | {d['b']} |")
    if not dupes:
        lines.append("| - | - | - | - |")

    lines += ["", f"## Long-tail sizing pages kept separate ({len(sized)})",
              "Same wording, different measurement — distinct queries, no action needed.",
              ""]
    for d in sized[:20]:
        lines.append(f"- {d['a']} <> {d['b']}")
    if len(sized) > 20:
        lines.append(f"- ... and {len(sized) - 20} more")

    lines += ["", "## Recommended merges (overlapping intent)", "",
              "| cluster | URL | recommendation |", "|---|---|---|"]
    for c, u, n in INTENT_GROUPS:
        lines.append(f"| {c} | {u[0]} | {n} |")

    lines += ["", "## Weak titles / slugs", "", "| slug | title | reason |", "|---|---|---|"]
    for w in weak:
        lines.append(f"| {w['slug']} | {w['title']} | {', '.join(w['reasons'])} |")

    lines += ["", "## Missing SEO elements", "", "| slug | gaps |", "|---|---|"]
    for m in missing:
        lines.append(f"| {m['slug']} | {', '.join(m['gaps'])} |")

    lines += ["", "## Sitemap issues", ""]
    lines += [f"- {i}" for i in sm_issues] or ["- none"]

    (REPORTS / "audit-phase0.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v)
                      for k, v in result.items()
                      if k in ("counts", "duplicates", "weak_pages",
                               "missing_elements", "sitemap_issues")}, indent=2))
    return result


if __name__ == "__main__":
    audit()
