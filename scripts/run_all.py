"""Full pipeline: keywords -> clusters -> generate -> link -> quality -> build -> verify
-> adsense -> monitor -> dashboard -> promotion playbook.

This is the single entry point used by the scheduled GitHub Action and by hand.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

import adsense
import build
import cluster
import dashboard
import generate
import interlink
import merges
import monitor
import quality
import verify
from common import DATA, load_json, save_json, seo_config


def run(limit: int | None = None) -> dict:
    seo = seo_config()
    # None means "use the configured default"; an explicit 0 means "generate nothing".
    if limit is None:
        limit = seo["limits"]["max_articles_per_run"]
    steps: dict = {}

    print("== 1/10 generate ==")
    generate.run(limit=limit)

    print("== 2/10 internal links + quality (to convergence) ==")
    arts = load_json(DATA / "articles.json", default=[])
    # Linking and gating are mutually dependent on a young site: an article needs links
    # to pass, but only passing articles are worth linking to. Iterate until the set of
    # accepted articles stops changing, so cold-start articles are not falsely rejected.
    for _ in range(6):
        before = {a["slug"]: a.get("status") for a in arts}
        interlink.link_all(arts)
        quality.apply(arts)
        after = {a["slug"]: a.get("status") for a in arts}
        if before == after:
            break
    # Gate once more, then rebuild links for the final statuses and save. Linking must
    # be the last mutation: quality.apply() can reject an article that was the only
    # inbound link for another, so repairing links *before* the last gate left an
    # orphan behind and aborted the run.
    quality.apply(arts)
    interlink.link_all(arts)
    save_json(DATA / "articles.json", arts)
    orphans = interlink.orphans(arts)
    steps["orphans"] = orphans

    # Merged pages (Phase 2) become stubs after linking/gating so no live page links
    # to them. Re-apply links once more so the graph excludes the merged slugs.
    merges.apply(arts)
    interlink.link_all(arts)
    save_json(DATA / "articles.json", arts)

    print("== 3/10 quality gates ==")
    approved = [a for a in arts if a.get("status") in ("published", "approved")]
    steps["approved"] = len(approved)
    steps["total"] = len(arts)

    print("== 4/10 build ==")
    steps["build"] = build.build()

    print("== 5/10 verify ==")
    steps["health"] = verify.check()

    print("== 6/10 adsense readiness ==")
    steps["adsense"] = adsense.readiness()

    print("== 7/10 monitor ==")
    steps["monitor"] = monitor.snapshot()

    print("== 8/10 dashboard ==")
    dashboard.build()

    print("== 9/10 promotion playbook ==")
    import promotion
    steps["promotion"] = promotion.write()

    print("== 10/10 report ==")
    _write_report(steps)
    return steps


def _write_report(steps: dict) -> None:
    from common import REPORTS
    today = dt.date.today().isoformat()
    lines = [f"# SEO run report — {today}", ""]
    lines.append(f"- Articles generated/approved: {steps.get('approved')}/{steps.get('total')}")
    lines.append(f"- Orphan articles: {steps.get('orphans')}")
    b = steps.get("build", {})
    lines.append(f"- Built: {b.get('articles')} articles, {b.get('urls')} sitemap URLs")
    h = steps.get("health", {})
    lines.append(f"- Health issues: {h.get('issues_total')} across {h.get('pages')} pages")
    a = steps.get("adsense", {})
    lines.append(f"- AdSense readiness: {a.get('passed')}/{a.get('total')} (ready={a.get('ready')})")
    m = steps.get("monitor", {})
    lines.append(f"- Avg SEO score: {m.get('avg_seo_score')}")
    if m.get("regressions"):
        lines.append(f"- Regressions: {m['regressions']}")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"run-{today}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    run(limit=args.limit)
