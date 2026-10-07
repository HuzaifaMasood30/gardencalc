"""Internal linking.

Builds a link graph between articles: same-cluster siblings plus the cluster pillar.
Adds contextual links into the body and keeps a map in data/links.json. Also sweeps
older articles so new pages receive links from existing ones.
"""
from __future__ import annotations

import re

from common import DATA, load_json, save_json, seo_config


def _published(arts: list[dict]) -> list[dict]:
    # Link to every live article, including drafts. Links are built before the gates
    # run, and the pipeline iterates link->gate to convergence, so any article that is
    # later rejected is dropped as a target on the next round (and never rendered).
    return [a for a in arts if a.get("status") != "rejected"]


def build_for(art: dict, arts: list[dict]) -> list[dict]:
    """Choose up to max_internal_links targets for this article."""
    seo = seo_config()
    hi = seo["limits"]["max_internal_links_per_article"]
    others = [a for a in _published(arts) if a["slug"] != art["slug"]]
    same = [a for a in others if a.get("cluster") == art.get("cluster")]
    other_c = [a for a in others if a.get("cluster") != art.get("cluster")]

    def key(a):
        return (0 if a.get("is_pillar") else 1, -a.get("quality", {}).get("score", 0))

    chosen = sorted(same, key=key)[:hi]
    if len(chosen) < min(3, hi):
        chosen += sorted(other_c, key=key)[:hi - len(chosen)]

    links = []
    for t in chosen[:hi]:
        anchor = _anchor_for(t)
        links.append({"to": t["slug"], "anchor": anchor, "title": t["title"]})
    return links


def _anchor_for(target: dict) -> str:
    """Natural anchor text, not 'click here' and not exact-match spam."""
    kw = target.get("primary_keyword", "").strip()
    if kw:
        return kw if len(kw) <= 45 else kw[:42].rsplit(" ", 1)[0]
    return target["title"][:45]


def inject(art: dict, site_url: str) -> str:
    """Append an internal 'Related guides' block and inline links where natural."""
    body = art.get("body_markdown", "")
    links = art.get("internal_links", [])
    if not links:
        return body

    # Inline: link the first natural mention of each related keyword if present.
    for link in links:
        anchor = link["anchor"]
        if not anchor:
            continue
        pattern = re.compile(r"(?<!\[)(?<!>)(" + re.escape(anchor) + r")(?!\]|\()", re.I)
        if pattern.search(body):
            body = pattern.sub(
                f"[{anchor}]({{{{url:{link['to']}}}}})", body, count=1)

    lines = ["\n## Related Guides\n"]
    for link in links:
        lines.append(f"- [{link['title']}]({{{{url:{link['to']}}}}})")
    return body + "\n" + "\n".join(lines) + "\n"


def link_all(arts: list[dict]) -> list[dict]:
    for art in arts:
        if art.get("status") == "rejected":
            art["internal_links"] = []
            continue
        art["internal_links"] = build_for(art, arts)
    graph = {
        a["slug"]: [l["to"] for l in a.get("internal_links", [])]
        for a in arts if a.get("status") != "rejected"
    }
    save_json(DATA / "links.json", {"graph": graph})
    return arts


def orphans(arts: list[dict]) -> list[str]:
    """Published articles with no inbound links — a real SEO problem."""
    published = _published(arts)
    inbound = {t for a in published for t in
               [l["to"] for l in a.get("internal_links", [])]}
    return [a["slug"] for a in published if a["slug"] not in inbound]


if __name__ == "__main__":
    items = load_json(DATA / "articles.json", default=[])
    link_all(items)
    save_json(DATA / "articles.json", items)
    for a in items:
        n = len(a.get("internal_links", []))
        print(f"{a.get('status'):9s} links={n}  {a['slug']}")
    print("orphans:", orphans(items))
