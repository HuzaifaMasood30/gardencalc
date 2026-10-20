"""Curated long-tail articles: the offline, hand-authored content path.

The generator only writes quality prose with an LLM key; without one it deliberately
skips long-tail pages so the site never fills up with templated thin content. This
runner adds hand-written articles from ``curated_articles.py``, each backed by the same
calculators engine the live tools use.

Numbers are never typed in the source. The body carries the worked-example bullets, and
article_fix recomputes them (and the intro claim) from ``calculator_defaults``, so a
change to a formula cannot leave a page quoting a stale figure. Run this module, then
the pipeline, to add the records:

    python scripts/add_articles.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_json, save_json, slugify, word_count  # noqa: E402
from curated_articles import ARTICLES, TODAY  # noqa: E402


def _source_hash(entry: dict) -> str:
    """Stable hash of the hand-written fields, so a re-run that changes nothing is a
    no-op even after article_fix has rewritten the stored body."""
    import hashlib
    payload = json.dumps({
        "title": entry["title"],
        "body": entry["body"],
        "meta": entry["meta_description"],
        "faq": entry["faq"],
        "defaults": entry["calculator_defaults"],
        "secondary": entry["secondary_keywords"],
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _record(entry: dict) -> dict:
    import calculators
    import generate

    body = entry["body"]
    calc = entry["calculator"]
    defaults = entry["calculator_defaults"]
    output = calculators.compute(calc, defaults)
    return {
        "id": entry["slug"],
        "slug": entry["slug"],
        "title": entry["title"],
        "cluster": entry["cluster"],
        "primary_keyword": entry["primary_keyword"],
        "secondary_keywords": entry["secondary_keywords"],
        "intent": "calculator",
        "is_pillar": False,
        "calculator": calc,
        "calculator_title": entry.get("calculator_title", calc.replace("_", " ").title()),
        "calculator_defaults": defaults,
        "calculator_output": output,
        "meta_description": generate._clip_meta(entry["meta_description"]),
        "body_markdown": body,
        "faq": [{"q": q, "a": a} for q, a in entry["faq"]],
        "status": "draft",
        "created": TODAY,
        "updated": TODAY,
        "revision": 1,
        "internal_links": [],
        "schema_types": ["Article", "BreadcrumbList", "FAQPage"],
        "quality": {},
        "metrics": {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0},
        "word_count": word_count(body),
        "curated_hash": _source_hash(entry),
    }


def main() -> None:
    arts = load_json(DATA / "articles.json", default=[])
    by_slug = {a["slug"]: a for a in arts}
    added = updated = 0
    for entry in ARTICLES:
        slug = entry["slug"]
        assert slug == slugify(entry["primary_keyword"]), (
            slug, slugify(entry["primary_keyword"]))
        record = _record(entry)
        existing = by_slug.get(slug)
        if existing is None:
            arts.append(record)
            by_slug[slug] = record
            added += 1
            continue
        # The stored body has been through article_fix, so compare the source hash,
        # not the body itself. A no-op run must leave the record untouched.
        if existing.get("curated_hash") == record["curated_hash"]:
            continue
        record["created"] = existing.get("created", TODAY)
        record["revision"] = existing.get("revision", 1) + 1
        # Keep the status and gate result the pipeline assigned; this module only owns
        # the content fields.
        record["status"] = existing.get("status", "draft")
        record["quality"] = existing.get("quality", {})
        existing.update(record)
        updated += 1
    save_json(DATA / "articles.json", arts)
    print(f"[add_articles] added {added}, updated {updated} ({len(arts)} total)")


if __name__ == "__main__":
    main()
