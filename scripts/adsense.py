"""AdSense readiness: insertion is handled by the site config, this checks compliance.

AdSense rejects sites with thin content, missing policy pages, or no clear navigation.
The cheap, high-value move is to prove the site passes those checks BEFORE applying, since
a rejection costs weeks. This module reports readiness and the exact gaps.
"""
from __future__ import annotations

import json

from common import DATA, SITE, load_json, save_json, site_config

REQUIRED_PAGES = ["about", "contact", "privacy-policy", "terms", "disclaimer"]
MIN_PUBLISHED_ARTICLES = 8
MIN_WORDS_PER_ARTICLE = 900


def readiness() -> dict:
    site = site_config()
    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]
    checks: dict[str, dict] = {}

    checks["policy_pages"] = {
        "ok": all((SITE / p / "index.html").exists() for p in REQUIRED_PAGES),
        "detail": f"{sum((SITE / p / 'index.html').exists() for p in REQUIRED_PAGES)}/{len(REQUIRED_PAGES)} present",
    }
    checks["adsense_configured"] = {
        "ok": bool(site.get("adsense_client")),
        "detail": site.get("adsense_client") or "set site.json adsense_client (ca-pub-...)",
    }
    checks["analytics_configured"] = {
        "ok": bool(site.get("analytics_id")),
        "detail": site.get("analytics_id") or "set site.json analytics_id (G-...)",
    }
    checks["contact_email"] = {
        "ok": bool(site.get("contact_email")) and "example.com" not in site.get("contact_email", ""),
        "detail": site.get("contact_email", ""),
    }
    checks["article_count"] = {
        "ok": len(arts) >= MIN_PUBLISHED_ARTICLES,
        "detail": f"{len(arts)}/{MIN_PUBLISHED_ARTICLES} published",
    }
    thin = [a["slug"] for a in arts if a.get("word_count", 0) < MIN_WORDS_PER_ARTICLE]
    checks["no_thin_pages"] = {"ok": not thin, "detail": f"thin: {thin}" if thin else "all >= 900 words"}
    checks["sitemap"] = {"ok": (SITE / "sitemap.xml").exists(), "detail": "sitemap.xml"}
    checks["robots"] = {"ok": (SITE / "robots.txt").exists(), "detail": "robots.txt"}
    checks["rss"] = {"ok": (SITE / "rss.xml").exists(), "detail": "rss.xml"}

    ready = sum(1 for c in checks.values() if c["ok"])
    total = len(checks)
    result = {
        "ready": ready == total,
        "passed": ready,
        "total": total,
        "checks": checks,
        "blocking": [k for k, v in checks.items() if not v["ok"]],
    }
    save_json(DATA / "adsense.json", result)
    return result


if __name__ == "__main__":
    r = readiness()
    print(json.dumps(r, indent=2))
