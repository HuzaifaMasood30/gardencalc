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
    # Merged pages are stubs, so they are never a link target or source.
    return [a for a in arts if a.get("status") not in ("rejected", "merged")]


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


_STOPWORDS = {
    "a", "an", "and", "are", "at", "by", "do", "does", "for", "from", "i", "in",
    "is", "it", "my", "of", "on", "or", "per", "the", "to", "what", "with", "your",
}


def _anchor_variants(anchor: str) -> list[str]:
    """Candidate phrases for inline matching, longest first.

    Anchors are long-tail keywords ('how much mulch do i need for 500 sq ft') that
    rarely appear verbatim in a sibling's body, so fall back to progressively shorter
    prefixes. Two rules keep the fallbacks clean: a phrase keeps at least three words
    (or the whole anchor when it is shorter), and trailing stop words are trimmed so a
    link never ends mid-phrase on 'for'/'of'/'the'.
    """
    words = re.sub(r"[\[\]()<>`*_]", "", anchor).split()
    floor = min(3, len(words))
    out: list[str] = []
    for n in range(len(words), floor - 1, -1):
        phrase = words[:n]
        while len(phrase) > floor and phrase[-1].lower() in _STOPWORDS:
            phrase = phrase[:-1]
        text = " ".join(phrase)
        if text.lower() not in {v.lower() for v in out}:
            out.append(text)
    return out


def _link(text: str, slug: str) -> str:
    return f"[{text}]({{{{url:{slug}}}}})"


def inject(art: dict) -> str:
    """Return the body with a contextual internal link at each target's first mention.

    Uses the persisted ``internal_links`` graph. Each target is linked at most once,
    at the first *non-overlapping* natural mention of its anchor (or an anchor prefix),
    keeping the visible text on-topic instead of 'click here'. Targets whose phrase
    never appears are skipped here and still reachable via the page's related grid,
    project links and breadcrumbs.
    """
    body = art.get("body_markdown", "")
    links = art.get("internal_links", [])
    if not body or not links:
        return body

    used: set[str] = set()
    spans: list[tuple[int, int, str]] = []
    placed: list[str] = []
    # Place the most specific anchors first so a long-tail target wins the spot over
    # a vaguer sibling whose anchor is only a prefix of it.
    for link in sorted(links, key=lambda l: -len((l.get("anchor") or "").split())):
        slug = link.get("to", "")
        anchor = (link.get("anchor") or "").strip()
        if not slug or not anchor or slug in used:
            continue
        for variant in _anchor_variants(anchor):
            vlow = variant.lower()
            # Skip a phrase nested inside one already placed (either direction): the
            # shorter form would add a second, vaguer link over the same words instead
            # of a distinct one. Long-tail targets are matched first, so the specific
            # anchor keeps the spot.
            if any(vlow.startswith(p) or p.startswith(vlow) for p in placed):
                continue
            for m in re.finditer(
                    r"(?<![\[\w/])(" + re.escape(variant) + r")(?![\w\]])", body, re.I):
                s, e = m.span()
                if any(not (e <= a or s >= b) for a, b, _ in spans):
                    continue  # overlaps a link already placed
                spans.append((s, e, f"[{m.group(0)}]({{{{url:{slug}}}}})"))
                placed.append(vlow)
                used.add(slug)
                break
            else:
                continue
            break

    for s, e, rep in sorted(spans, key=lambda t: t[0], reverse=True):
        body = body[:s] + rep + body[e:]

    # Fallback for pages whose prose never names a sibling using the anchor's words
    # (the generic pillar calculators, where plenty of sibling coverage exists and a
    # reader needs the entry point). One plain in-content sentence guarantees the page
    # still carries a contextual link rather than only template chrome.
    if not spans:
        extra = [l for l in links if l.get("to") not in used and l.get("title")]
        if extra:
            name = extra[0]["title"].rstrip(".")
            body += f"\n\nFor coverage at other sizes, see {_link(name, extra[0]['to'])}.\n"
    return body


def link_all(arts: list[dict], persist: bool = True) -> list[dict]:
    # Always rebuild links, even for articles currently rejected. Zeroing them made the
    # links gate re-reject an article forever: a rejected page had no links, so it could
    # never pass and never recover once its other gates were fixed. Rejected articles
    # are still excluded as link *targets* (see _published) and are never rendered.
    for art in arts:
        art["internal_links"] = build_for(art, arts)
    _repair_orphans(arts)
    graph = {
        a["slug"]: [l["to"] for l in a.get("internal_links", [])]
        for a in arts if a.get("status") not in ("rejected", "merged")
    }
    if persist:
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
