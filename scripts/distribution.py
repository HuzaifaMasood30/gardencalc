"""Distribution: generate the exact copy for legitimate off-site promotion, and track
what has been submitted where.

A sandbox cannot create accounts or post on the user's behalf, so this module removes all
the thinking and typing from the parts only the account owner can do: it writes ready-to-paste
titles, descriptions, citation text, and the precise submission URL for each legitimate
channel. It then records completion so the state survives across runs.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re

from common import DATA, REPORTS, load_json, save_json, site_config

import charts
import planners
import seasonal


def channels() -> list[dict]:
    site = site_config()
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    name = site["name"]
    niche = "free home and garden calculators"

    return [
        {
            "id": "google-search-console",
            "title": "Verify the site in Google Search Console",
            "why": "Primary source of indexing, impressions, CTR and ranking data. Nothing else matters as much.",
            "url": "https://search.google.com/search-console",
            "template": "Property: " + base + "/  — verify with the HTML tag in config/site.json, then submit " + base + "/sitemap.xml",
        },
        {
            "id": "bing-webmaster",
            "title": "Add the site to Bing Webmaster Tools",
            "why": "Bing/DuckDuckGo traffic; can import the verified property from Search Console in one click.",
            "url": "https://www.bing.com/webmasters",
            "template": "Import from Google Search Console, then submit " + base + "/sitemap.xml",
        },
        {
            "id": "github-pages",
            "title": "Enable GitHub Pages on the repository",
            "why": "Hosts the static site for free from .github/workflows/deploy.yml.",
            "url": "https://github.com/settings/pages",
            "template": "Settings > Pages > Source: GitHub Actions (the workflow already deploys site/)",
        },
        {
            "id": "cloudflare-pages",
            "title": "Add a custom domain via Cloudflare (optional)",
            "why": "Custom domain improves credibility and lets you set canonical URLs on your own domain.",
            "url": "https://dash.cloudflare.com",
            "template": "Point a domain at GitHub Pages, then set site.json custom_domain and rebuild.",
        },
        {
            "id": "reddit-diy",
            "title": "Answer relevant r/DIY and r/landscaping questions",
            "why": "Real, non-spam answers to real questions; link only where the calculator directly answers the question.",
            "url": "https://www.reddit.com/r/DIY/",
            "template": (
                "Look for 'how much mulch/soil/gravel' questions. Reply with the actual calculation "
                "for their numbers, then add: 'I put the formula and a calculator here -> " + base + "/<page>/'. "
                "Only link when it genuinely answers the post."
            ),
        },
        {
            "id": "stackexchange",
            "title": "Answer Gardening & Landscaping Stack Exchange questions",
            "why": "High-trust domain; answers rank and can send steady referral traffic.",
            "url": "https://gardening.stackexchange.com/questions",
            "template": "Give the full method in the answer body; cite the calculator as a supporting tool, not the whole answer.",
        },
        {
            "id": "wikipedia-cite",
            "title": "Propose citations where a calculator genuinely supports a claim",
            "why": "Strongest possible citation, but only where the page is a suitable source.",
            "url": "https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources",
            "template": "Do NOT add promotional links. Only cite if the page supports a specific numeric claim, e.g. mulch depth guidance.",
        },
        {
            "id": "quora",
            "title": "Answer Quora questions about material quantities",
            "why": "Quora answers surface in Google and can hold a relevant link.",
            "url": "https://www.quora.com",
            "template": "Search 'how much mulch do I need'. Answer with the worked formula; link the matching calculator once.",
        },
        {
            "id": "pinterest",
            "title": "Create Pinterest boards per calculator",
            "why": "Home and garden is a large Pinterest niche; each article's OG image can be pinned.",
            "url": "https://www.pinterest.com",
            "template": "Pin the OG image for each article with the title as the pin text and a link to the page.",
        },
        {
            "id": "directory-diy",
            "title": "Submit to reputable niche directories and blog roundups",
            "why": "Legitimate citations from real sites; skip any paid PBN-style directory.",
            "url": "https://www.google.com/search?q=best+home+improvement+calculator+blogs+submit",
            "template": "Pitch a 2-line intro: what the tool does and who it helps. Offer genuinely useful tools, not a link swap.",
        },
        {
            "id": "rss-aggregators",
            "title": "Submit the RSS feed to aggregators",
            "why": "Free redistribution of new posts; can surface them to relevant readers.",
            "url": base + "/rss.xml",
            "template": "Feed URL: " + base + "/rss.xml",
        },
        {
            "id": "seasonal-social",
            "title": "Share a seasonal timing guide each season",
            "why": "Timing searches spike every spring/autumn; the evergreen guides are the natural asset to push.",
            "url": base + "/when-to-mulch/",
            "template": ("Rotate " + base + "/when-to-mulch/, " + base
                         + "/when-to-overseed-a-lawn/, " + base
                         + "/spring-garden-bed-checklist/ and " + base
                         + "/fall-lawn-fertilizer-timing/ on Pinterest/Threads/X with a UTM link "
                         "so the traffic is attributable."),
        },
        {
            "id": "schema-validate",
            "title": "Validate structured data",
            "why": "Confirms the Article/FAQ/WebApplication/Breadcrumb markup will be eligible for rich results.",
            "url": "https://search.google.com/test/rich-results",
            "template": "Paste each article URL after deploy and confirm no errors.",
        },
    ]


def material(art: dict) -> dict:
    """Ready-to-paste promotion copy for one article."""
    site = site_config()
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    return {
        "slug": art["slug"],
        "url": f"{base}/{art['slug']}/",
        "title": art["title"],
        "meta": art.get("meta_description", ""),
        "reddit_answer": (
            f"Here's the arithmetic for your job: multiply length x width to get the area, "
            f"then x depth in feet to get the volume. {art.get('meta_description','')} "
            f"I wrote the formula and a calculator here: {base}/{art['slug']}/"
        ),
        "pitch": (
            f"Hi — I built a free {art.get('primary_keyword','')} calculator that shows the "
            f"formula and a worked example rather than just an answer. Might be useful for your "
            f"readers: {base}/{art['slug']}/"
        ),
    }


def export_titles() -> dict:
    """Write docs/titles.csv so the owner can review every title/description in bulk.

    The growth brief asks for a url,current_title,proposed_title,current_description,
    proposed_description export. Proposed values are the tightened targets; the owner
    approves or edits them here.
    """
    from common import ROOT
    site = site_config()
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    rows = [["url", "current_title", "proposed_title", "current_description", "proposed_description"]]
    special = {
        "/": ("Home & Garden Calculators: Free & Instant | " + site["name"],
              "Free home and garden calculators for mulch, soil, gravel, paint, tile, "
              "seed and concrete. Instant answers that show the formula used."),
    }
    seen = set()
    for a in arts:
        url = f"/{a['slug']}/"
        if url in seen:
            continue
        seen.add(url)
        cur_t = a.get("title", "")
        des = a.get("meta_description", "")
        rows.append([base + url, cur_t, suggest_title(cur_t), des, suggest_desc(des, a)])
    for url, (t, d) in special.items():
        rows.append([base + url, "", t, "", d])

    # Charts, planners and seasonal guides are generated pages, not articles, so they
    # are pulled straight from their modules to keep this export complete.
    extra_sets = [
        [{"slug": c["slug"], "title": c["title"], "meta_description": c["description"]}
         for c in charts.CHARTS],
        [{"slug": p["slug"], "title": p["title"], "meta_description": p["description"]}
         for p in planners.PLANNERS],
        [{"slug": s["slug"], "title": s["title"], "meta_description": s["description"]}
         for s in seasonal.SEASONAL],
    ]
    for group in extra_sets:
        for a in group:
            url = f"/{a['slug']}/"
            if url in seen:
                continue
            seen.add(url)
            rows.append([base + url, a["title"], suggest_title(a["title"]),
                         a["meta_description"], suggest_desc(a["meta_description"], a)])
    path = docs / "titles.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerows(rows)
    return {"titles_csv": str(path), "rows": len(rows) - 1}


# "Free Calculator & Guide" and "Free Calculator" tails take 21+ characters of the
# ~60 Google shows. Tighten them to "(Free)" so the keyword stays first and the tag
# does not get truncated mid-word.
_TITLE_FIXES = [
    (" : Free Calculator & Guide", " (Free)"),
    (": Free Calculator & Guide", " (Free)"),
    (" Free Calculator & Guide", " (Free)"),
    ("Free Calculator &", "Free"),
    ("Calculator & Guide", "Calculator"),
]


def suggest_title(title: str) -> str:
    out = title
    for old, new in _TITLE_FIXES:
        out = out.replace(old, new)
    out = re.sub(r"\s+", " ", out).strip()
    if len(out) > 60:
        # Last resort: drop a trailing parenthetical rather than truncate mid-word.
        out = re.sub(r"\s*\([^)]*\)\s*$", "", out).strip()
    return out


def suggest_desc(desc: str, art: dict) -> str:
    """Ensure the description opens with the answer and ends with a mini CTA."""
    d = re.sub(r"\s+", " ", desc).strip()
    if "calculat" not in d.lower():
        d = (d + " Free calculator with the formula shown.").strip()
    return d


def material_page(item: dict) -> dict:
    """Promotion copy for a generated page (chart, planner, seasonal guide)."""
    site = site_config()
    base = (site.get("custom_domain") or site["base_url"]).rstrip("/")
    slug = item["slug"]
    kw = item.get("primary_keyword", "") or item.get("keyword", "")
    desc = item.get("meta_description") or item.get("description", "")
    return {
        "slug": slug,
        "url": f"{base}/{slug}/",
        "title": item["title"],
        "meta": desc,
        "reddit_answer": (
            f"Here's the arithmetic for your job: multiply length x width to get the area, "
            f"then x depth in feet to get the volume. {desc} "
            f"I put the formula and full reference tables here: {base}/{slug}/"
        ),
        "pitch": (
            f"Hi — I built a free {kw or 'garden material'} reference page that shows the "
            f"formula and worked examples rather than just an answer. Might be useful for your "
            f"readers: {base}/{slug}/"
        ),
    }


def write_pack() -> dict:
    site = site_config()
    arts = [a for a in load_json(DATA / "articles.json", default=[])
            if a.get("status") in ("published", "approved")]
    state = load_json(DATA / "distribution.json", default=None)
    done_ids = set(state.get("completed", [])) if state else set()

    items = []
    for c in channels():
        items.append({**c, "done": c["id"] in done_ids})

    generated = (
        [dict(c, meta_description=c["description"]) for c in charts.CHARTS]
        + [dict(p, meta_description=p["description"]) for p in planners.PLANNERS]
        + [dict(s, meta_description=s["description"]) for s in seasonal.SEASONAL]
    )

    pack = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(),
        "site": site["name"],
        "base_url": (site.get("custom_domain") or site["base_url"]),
        "channels": items,
        "articles": [material(a) for a in arts] + [material_page(g) for g in generated],
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "distribution-pack.md").write_text(_to_markdown(pack), encoding="utf-8")

    state = {
        "completed": sorted(done_ids),
        "actions": [{"id": c["id"], "title": c["title"], "done": c["done"]} for c in items],
        "done": len(done_ids),
        "total": len(items),
    }
    save_json(DATA / "distribution.json", state)
    return pack


def mark(channel_id: str, done: bool = True) -> None:
    state = load_json(DATA / "distribution.json", default=None)
    completed = set(state.get("completed", [])) if state else set()
    completed.add(channel_id) if done else completed.discard(channel_id)
    save_json(DATA / "distribution.json", {"completed": sorted(completed)})
    write_pack()


def _to_markdown(pack: dict) -> str:
    lines = [f"# Distribution pack — {pack['site']}", "", f"Base URL: {pack['base_url']}", ""]
    lines += ["## Submission checklist", ""]
    for c in pack["channels"]:
        mark = "x" if c["done"] else " "
        lines.append(f"- [{mark}] **{c['title']}** — {c['why']}")
        lines.append(f"  - Open: {c['url']}")
        lines.append(f"  - Do: {c['template']}")
    lines += ["", "## Ready-to-paste copy per article", ""]
    for a in pack["articles"]:
        lines.append(f"### {a['slug']}")
        lines.append(f"- URL: {a['url']}")
        lines.append(f"- Title: {a['title']}")
        lines.append(f"- Meta: {a['meta']}")
        lines.append(f"- Forum answer: {a['reddit_answer']}")
        lines.append(f"- Outreach pitch: {a['pitch']}")
        lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", help="channel id to mark done")
    ap.add_argument("--undo", help="channel id to mark not done")
    args = ap.parse_args()
    if args.mark:
        mark(args.mark, True)
        print("marked", args.mark)
    elif args.undo:
        mark(args.undo, False)
        print("unmarked", args.undo)
    else:
        p = write_pack()
        export_titles()
        print(json.dumps({"channels": len(p["channels"]), "articles": len(p["articles"])}, indent=2))
