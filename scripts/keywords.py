"""Keyword discovery, intent classification and prioritisation.

Sources (all free, no API key):
  - Google autosuggest  (suggestqueries.google.com/complete/search?client=firefox)
  - Bing autosuggest    (api.bing.com/osjson.aspx)
  - Alphabet expansion  ("how much mulch do i need a", "... b", ...)

Scoring favours realistic ranking potential (long-tail, low competition) over raw volume,
because a brand-new site cannot rank for head terms.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

from common import DATA, load_json, save_json, slugify, topics_config

UA = {"User-Agent": "Mozilla/5.0 (compatible; GardenCalcBot/1.0)"}

COMMERCIAL = ("cost", "price", "cheap", "buy", "best", "vs", "review", "near me")
CALC = ("calculator", "calculate", "how much", "how many", "how deep", "how thick")
LOCAL = ("near me", "in my area", "store", "home depot", "lowes")


def _get(url: str, timeout: int = 12):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""


def google_suggest(q: str) -> list[str]:
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&q="
           + urllib.parse.quote(q))
    raw = _get(url)
    try:
        return json.loads(raw)[1]
    except Exception:
        return []


def bing_suggest(q: str) -> list[str]:
    url = "https://api.bing.com/osjson.aspx?query=" + urllib.parse.quote(q)
    raw = _get(url)
    try:
        return json.loads(raw)[1]
    except Exception:
        return []


# Off-topic distractors that autosuggest returns for these seeds.
NOISE = [
    "fish tank", "aquarium", "minecraft", "fortnite", "game", "roblox", "lyrics",
    "song", "movie", "meaning", "meme", "recipe", "cake", "guitar", "wedding",
    "car ", "truck", "diesel", "pool filter", "cat litter", "dog", "horse",
    "dollar", "stock", "crypto", "job", "salary", "near me", "tattoo",
]

# The material token each seed is actually about.
MATERIAL = {
    "mulch": "mulch", "soil": "soil", "gravel": "gravel", "paint": "paint",
    "tile": "tile", "grass seed": "grass seed", "concrete": "concrete",
    "fertilizer": "fertilizer", "topsoil": "topsoil", "sand": "sand",
    "compost": "compost", "river rock": "river rock",
}


def is_relevant(keyword: str, primary: str) -> bool:
    k = keyword.lower()
    if any(n in k for n in NOISE):
        return False
    material = next((v for k2, v in MATERIAL.items() if k2 in primary.lower()), "")
    if not material:
        return True
    # Must actually mention the material, and must be about quantity or coverage.
    if material not in k:
        return False
    return True


def expand(seed: str, alphabet: bool = True, limit: int = 40) -> list[str]:
    found: list[str] = []
    for fn in (google_suggest, bing_suggest):
        found += fn(seed)
        time.sleep(0.25)
    if alphabet:
        for ch in "abcdefghij":
            found += google_suggest(f"{seed} {ch}")
            time.sleep(0.2)
            if len(found) >= limit:
                break
    seen, out = set(), []
    for k in found:
        k = k.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


def classify(keyword: str) -> str:
    k = keyword.lower()
    if any(t in k for t in LOCAL):
        return "local"
    if any(t in k for t in COMMERCIAL):
        return "commercial"
    if any(t in k for t in CALC):
        return "calculator"
    if k.startswith(("what", "why", "when", "where", "who", "is ", "are ", "does ")):
        return "informational"
    return "informational"


def score(keyword: str, cluster_primary: str = "") -> float:
    """0-100 realistic-opportunity score. Long-tail + calc intent score highest."""
    words = len(keyword.split())
    s = 30.0
    s += min(words, 8) * 6.0                      # longer tail ranks more easily
    if any(t in keyword for t in CALC):
        s += 12
    if any(t in keyword for t in ("sq ft", "square feet", "square foot", "per ", "for a", "for my")):
        s += 10
    if cluster_primary and cluster_primary in keyword:
        s += 8
    if any(t in keyword for t in COMMERCIAL):
        s -= 8                                    # higher competition
    if words <= 2:
        s -= 15                                   # head terms: too competitive
    return max(0.0, min(100.0, round(s, 1)))


def discover(seeds: list[str] | None = None) -> list[dict]:
    cfg = topics_config()
    seeds = seeds or cfg.get("seed_topics", [])
    clusters = {c["primary"]: c["id"] for c in cfg.get("clusters", [])}
    known = {k["keyword"] for k in load_json(DATA / "keywords.json", default=[])}

    results: list[dict] = []
    for seed in seeds:
        primary = seed
        cluster_id = next((cid for p, cid in clusters.items() if p in seed or seed in p), "")
        for kw in [seed] + expand(seed, alphabet=True):
            if kw in known or any(r["keyword"] == kw for r in results):
                continue
            if not is_relevant(kw, primary):
                continue
            results.append({
                "keyword": kw,
                "slug": slugify(kw),
                "cluster": cluster_id,
                "intent": classify(kw),
                "score": score(kw, primary),
                "source": "autosuggest",
                "used": False,
            })
        print(f"[keywords] {seed}: {len(results)} total so far")

    results.sort(key=lambda r: r["score"], reverse=True)
    merged = load_json(DATA / "keywords.json", default=[]) + results
    save_json(DATA / "keywords.json", merged)
    print(f"[keywords] discovered {len(results)} new, {len(merged)} total")
    return results


if __name__ == "__main__":
    discover()
