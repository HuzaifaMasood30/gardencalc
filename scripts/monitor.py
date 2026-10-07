"""Monitoring: recompute the SEO score per page, track history, and flag regressions."""
from __future__ import annotations

import datetime as dt
import json

from common import DATA, load_json, save_json, seo_config, site_config

import seo as seolib


def snapshot() -> dict:
    site = site_config()
    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]

    per_article = []
    for a in arts:
        s = seolib.calculate_seo_score(a, site)
        per_article.append({"slug": a["slug"], "score": s["score"], "checks": s["checks"],
                            "word_count": a.get("word_count", 0)})

    avg = round(sum(p["score"] for p in per_article) / len(per_article), 1) if per_article else 0.0
    today = dt.date.today().isoformat()
    snap = {
        "date": today,
        "articles": len(per_article),
        "avg_seo_score": avg,
        "total_words": sum(p["word_count"] for p in per_article),
        "per_article": per_article,
    }

    hist = load_json(DATA / "history.json", default=[])
    hist = [h for h in hist if h.get("date") != today]
    hist.append(snap)
    hist.sort(key=lambda h: h["date"])
    save_json(DATA / "history.json", hist)

    # regression check: score dropped vs the previous snapshot
    regressions = []
    if len(hist) >= 2:
        prev = {p["slug"]: p["score"] for p in hist[-2]["per_article"]}
        for p in per_article:
            if p["slug"] in prev and p["score"] < prev[p["slug"]] - 2:
                regressions.append({"slug": p["slug"], "was": prev[p["slug"]], "now": p["score"]})
    snap["regressions"] = regressions
    return snap


def week_over_week() -> dict:
    hist = load_json(DATA / "history.json", default=[])
    if len(hist) < 2:
        return {"available": False}
    first, last = hist[0], hist[-1]
    d1 = dt.date.fromisoformat(first["date"])
    d2 = dt.date.fromisoformat(last["date"])
    days = max((d2 - d1).days, 1)
    return {
        "available": True,
        "days": days,
        "articles_delta": last["articles"] - first["articles"],
        "words_delta": last["total_words"] - first["total_words"],
        "avg_score_delta": round(last["avg_seo_score"] - first["avg_seo_score"], 1),
    }


if __name__ == "__main__":
    print(json.dumps(snapshot(), indent=2))
    print(json.dumps(week_over_week(), indent=2))
