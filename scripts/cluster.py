"""Group keywords into topic clusters and choose the next articles to write."""
from __future__ import annotations

from common import DATA, load_json, save_json, topics_config


def build_clusters() -> dict:
    cfg = topics_config()
    kws = load_json(DATA / "keywords.json", default=[])
    clusters: dict[str, dict] = {}
    for c in cfg.get("clusters", []):
        clusters[c["id"]] = {
            "id": c["id"],
            "name": c["name"],
            "calculator": c["calculator"],
            "primary": c["primary"],
            "pillar": c["pillar"],
            "keywords": [],
        }
    for k in kws:
        cid = k.get("cluster") or _guess_cluster(k["keyword"], cfg)
        if cid in clusters:
            clusters[cid]["keywords"].append(k)
    for c in clusters.values():
        c["keywords"].sort(key=lambda k: k["score"], reverse=True)
        c["count"] = len(c["keywords"])
        c["top"] = [k["keyword"] for k in c["keywords"][:5]]
    out = {"clusters": list(clusters.values())}
    save_json(DATA / "clusters.json", out)
    return out


def _guess_cluster(keyword: str, cfg: dict) -> str:
    import keywords
    return keywords.guess_cluster(keyword, cfg)


def plan(limit: int = 3) -> list[dict]:
    """Pick the highest-value unwritten keywords, one per cluster for balance."""
    cfg = topics_config()
    kws = load_json(DATA / "keywords.json", default=[])
    arts = load_json(DATA / "articles.json", default=[])
    written = {a["primary_keyword"] for a in arts}
    existing_slugs = {a["slug"] for a in arts}

    # A pillar article per cluster. Collect them first and exclude their keywords and
    # slugs from the supporting-keyword pool, otherwise a pillar's own primary keyword
    # is selected again and the same page is generated under a second URL.
    pillar_picks: list[dict] = []
    for c in cfg.get("clusters", []):
        cid = c["id"]
        have_pillar = any(a.get("cluster") == cid and a.get("is_pillar") for a in arts)
        if not have_pillar:
            pillar_picks.append({
                "cluster": cid, "calculator": c["calculator"], "is_pillar": True,
                "primary_keyword": c["primary"], "slug": c["pillar"], "score": 100.0,
            })
            written.add(c["primary"])
            existing_slugs.add(c["pillar"])

    by_cluster: dict[str, list[dict]] = {}
    for k in sorted(kws, key=lambda x: x["score"], reverse=True):
        if k["keyword"] in written or k.get("used"):
            continue
        if k["slug"] in existing_slugs:
            continue
        by_cluster.setdefault(k.get("cluster", ""), []).append(k)

    picks: list[dict] = list(pillar_picks)
    for cid, items in by_cluster.items():
        if items:
            k = items[0]
            picks.append({
                "cluster": cid, "calculator": _calc_for(cid, cfg), "is_pillar": False,
                "primary_keyword": k["keyword"], "slug": k["slug"], "score": k["score"],
            })
    # de-dupe by slug, keep highest score
    seen, ordered = set(), []
    for p in sorted(picks, key=lambda x: x["score"], reverse=True):
        if p["slug"] not in seen:
            seen.add(p["slug"])
            ordered.append(p)
    chosen = ordered[:limit]
    print(f"[plan] selected {len(chosen)} articles: "
          + ", ".join(p['slug'] for p in chosen))
    return chosen


def _calc_for(cluster_id: str, cfg: dict) -> str:
    for c in cfg.get("clusters", []):
        if c["id"] == cluster_id:
            return c["calculator"]
    return ""


if __name__ == "__main__":
    build_clusters()
    plan()
