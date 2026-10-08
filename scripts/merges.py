"""Duplicate-page merges (brief 1, Phase 2).

GitHub Pages cannot serve server-side redirects, so a merged page is replaced by a
small HTML stub that meta-refreshes and canonicals to its target, stays indexable
(so it passes the canonical signal) and is removed from the sitemap, listings, RSS
and internal links.

Each entry maps a redundant slug to the slug that should rank for the intent.
Keep this list short and evidence-based: only merge pages whose primary keyword and
intent genuinely overlap. Renaming an indexed URL is avoided; the old URL is kept
alive as the stub.
"""
from __future__ import annotations

from common import DATA, load_json

# old_slug -> target_slug
MERGES: dict[str, str] = {
    # Door vs front door: same intent, front-door page is the more specific keeper.
    "how-much-paint-do-i-need-for-a-door":
        "how-much-paint-do-i-need-for-a-front-door",
    # Lawn vs new lawn topsoil: one intent, new-lawn page wins.
    "how-much-topsoil-do-i-need-for-a-lawn":
        "how-much-topsoil-do-i-need-for-a-new-lawn",
    # Metric/locale variant that still used US units and wording.
    "how-much-soil-for-raised-bed-calculator-uk":
        "raised-bed-soil-calculator",
    # Pure "calculator" intent duplicates of their category pillar.
    "how-much-fertilizer-per-1000-sq-ft-calculator": "fertilizer-calculator",
    "how-much-paint-do-i-need-calculator-sq-ft": "paint-calculator",
    # Canada page used US units; merge until a genuinely metric version exists.
    "how-much-grass-seed-per-square-foot-canada":
        "how-much-grass-seed-per-square-foot-for-new-lawn",
    # "My flower bed" vs "a flower bed": identical intent.
    "how-much-mulch-do-i-need-for-my-flower-bed":
        "how-much-mulch-do-i-need-for-a-flower-bed",
    # "Needed per square foot" vs "do I need per square foot": same query.
    "how-much-grass-seed-needed-per-square-foot":
        "how-much-grass-seed-do-i-need-per-square-foot",
    # Calculator-intent duplicate of the grass-seed pillar.
    "how-much-grass-seed-per-square-foot-calculator": "grass-seed-calculator",
    # Raised-bed soil phrased three ways; keep the "do I need" head term.
    "how-much-soil-do-you-need-for-a-raised-bed":
        "how-much-soil-do-i-need-for-a-raised-bed",
    "how-much-soil-for-a-raised-garden-bed":
        "how-much-soil-do-i-need-for-a-raised-bed",
    # Calculator-intent duplicates of their category pillar.
    "how-much-soil-for-a-raised-bed-calculator": "raised-bed-soil-calculator",
    "how-much-topsoil-for-raised-garden-bed-calculator": "topsoil-calculator",
    # 8x4x1 and 4x8 describe the same bed; canonicalise to 4x8.
    "how-much-soil-for-a-8x4x1-raised-bed": "how-much-soil-for-a-4x8-raised-bed",
    # "my driveway" vs "a driveway": same intent.
    "how-much-gravel-do-i-need-for-my-driveway":
        "how-much-gravel-do-i-need-for-a-driveway",
    # Scotts is one brand of the same starter-fertilizer question.
    "how-much-scotts-starter-fertilizer-per-1000-sq-ft":
        "how-much-starter-fertilizer-per-1000-sq-ft",
    # Generic floor/room pages duplicate the tile pillar; sized pages stay.
    "how-many-tiles-do-i-need-for-my-floor": "tile-calculator",
    "how-many-tiles-do-i-need-for-my-room": "tile-calculator",
}


def targets() -> set[str]:
    return set(MERGES.values())


# old_slug -> new_slug for URLs that were cleaned up (not merged, just renamed).
# A rename stub keeps the old URL alive so nothing 404s.
RENAMES: dict[str, str] = {
    "how-many-bags-of-concrete-do-i-need-for-a-4-x8-slab":
        "how-many-bags-of-concrete-do-i-need-for-a-4x8-slab",
}


def rename_stubs(arts: list[dict]) -> list[dict]:
    by = {a["slug"]: a for a in arts}
    out = []
    for old, new in RENAMES.items():
        if old in by:
            continue  # real page still exists under the old slug; nothing to do
        target = by.get(new, {})
        out.append({"slug": old, "target": new,
                    "target_title": target.get("title", new),
                    "old_title": target.get("title", old)})
    return out


def merged_slugs() -> set[str]:
    return set(MERGES)


def apply(arts: list[dict]) -> list[dict]:
    """Mark merged articles as such so build and listings drop them.

    The flag is re-derived every run from MERGES, so removing an entry restores the
    page with no other edits.
    """
    for a in arts:
        tgt = MERGES.get(a["slug"])
        if tgt:
            a["status"] = "merged"
            a["merged_into"] = tgt
            a.setdefault("quality", {})
            a["quality"] = {"score": 100.0, "passed": True, "merged_into": tgt,
                            "gates": {}}
    return arts


def stubs(arts: list[dict]) -> list[dict]:
    """Return {slug, target, title} for every stub to render, target first resolved."""
    by = {a["slug"]: a for a in arts}
    out = []
    for old, tgt in MERGES.items():
        target = by.get(tgt, {})
        out.append({"slug": old, "target": tgt,
                    "target_title": target.get("title", tgt),
                    "old_title": by.get(old, {}).get("title", old)})
    return out


if __name__ == "__main__":
    items = load_json(DATA / "articles.json", default=[])
    apply(items)
    for s in stubs(items):
        print(f"{s['slug']}  ->  {s['target']}  ({s['target_title']})")
