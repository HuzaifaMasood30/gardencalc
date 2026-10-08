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
    # Always rebuild links, even for articles currently rejected. Zeroing them made the
    # links gate re-reject an article forever: a rejected page had no links, so it could
    # never pass and never recover once its other gates were fixed. Rejected articles
    # are still excluded as link *targets* (see _published) and are never rendered.
    for art in arts:
        art["internal_links"] = build_for(art, arts)
    _repair_orphans(arts)
    graph = {
        a["slug"]: [l["to"] for l in a.get("internal_links", [])]
        for a in arts if a.get("status") != "rejected"
    }
    save_json(DATA / "links.json", {"graph": graph})
    return arts


def _repair_orphans(arts: list[dict]) -> None:
    """Guarantee every published article has at least one inbound internal link.

    The cluster ring covers clusters with two or more members; a keyword that lands
    in a cluster of its own (or a brand-new cluster) would otherwise be orphaned and
    fail the build. Add inbound links from the closest available sources until none
    remain.
    """
    published = _published(arts)
    if len(published) < 2:
        return
    hi = seo_config()["limits"]["max_internal_links_per_article"]
    for _ in range(len(published)):
        inbound = {l["to"] for a in published for l in a.get("internal_links", [])}
        missing = [a for a in published if a["slug"] not in inbound]
        if not missing:
            return
        for orphan in missing:
            # Prefer a source that still has spare link capacity (so we do not push it
            # past the cap and fail its own internal-links gate), then a same-cluster
            # source, then a pillar, then the highest scoring.
            sources = sorted(
                (a for a in published if a["slug"] != orphan["slug"]),
                key=lambda a: (
                    0 if len(a.get("internal_links", [])) < hi else 1,
                    0 if a.get("cluster") == orphan.get("cluster") else 1,
                    0 if a.get("is_pillar") else 1,
                    -a.get("quality", {}).get("score", 0),
                ),
            )
            for src in sources:
                targets = {l["to"] for l in src.get("internal_links", [])}
                if orphan["slug"] in targets:
                    break
                src.setdefault("internal_links", []).append({
                    "to": orphan["slug"],
                    "anchor": _anchor_for(orphan),
                    "title": orphan["title"],
                })
                break


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
