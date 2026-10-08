# GardenCalc — Phase 0 audit

Generated 2026-10-08T15:40:20+00:00. Report only; no edits made.

## How the site is built
- `scripts/run_all.py` runs the pipeline: generate -> interlink -> quality -> build -> verify.
- `scripts/build.py` renders Jinja templates in `templates/` to `site/`.
- Articles live in `data/articles.json`; charts/planners/seasonal are generated in `scripts/{charts,planners,seasonal}.py`.
- Deploy: GitHub Actions `deploy.yml` (push) and `pipeline.yml` (cron).

## Page counts
- Articles: 86 total, 68 live (merged stubs excluded)
- Categories: 9; Charts: 8; Planners: 4; Seasonal: 4
- Mean article length: 841 words

## Near-duplicate pages (same intent, similarity >= 0.80)
These pairs share a searcher intent and should merge or be differentiated. Pairs that differ only by a sizing number are legitimate long-tail pages, listed separately below.
| similarity | cluster | page A | page B |
|---|---|---|---|
| 0.80 | soil | raised-bed-soil-calculator | how-much-soil-for-a-4x8-raised-bed |
| 0.80 | soil | raised-bed-soil-calculator | how-much-soil-do-i-need-for-a-raised-bed |
| 0.80 | topsoil | how-much-topsoil-do-i-need-for-a-garden-bed | how-much-topsoil-do-i-need-for-my-raised-garden-bed |

## Long-tail sizing pages kept separate (28)
Same wording, different measurement — distinct queries, no action needed.

- how-many-bags-of-concrete-do-i-need-for-a-10x10-slab <> how-many-bags-of-concrete-do-i-need-for-a-4x8-slab
- how-much-mulch-do-i-need-for-300-square-feet <> how-much-mulch-do-i-need-for-200-square-feet
- how-much-mulch-do-i-need-for-300-square-feet <> how-much-mulch-do-i-need-for-400-square-feet
- how-much-mulch-do-i-need-for-300-square-feet <> how-much-mulch-do-i-need-for-1000-square-feet
- how-much-mulch-do-i-need-for-300-square-feet <> how-much-mulch-do-i-need-for-600-square-feet
- how-much-mulch-do-i-need-for-300-square-feet <> how-much-mulch-do-i-need-for-32-square-feet
- how-much-mulch-do-i-need-for-200-square-feet <> how-much-mulch-do-i-need-for-400-square-feet
- how-much-mulch-do-i-need-for-200-square-feet <> how-much-mulch-do-i-need-for-1000-square-feet
- how-much-mulch-do-i-need-for-200-square-feet <> how-much-mulch-do-i-need-for-600-square-feet
- how-much-mulch-do-i-need-for-200-square-feet <> how-much-mulch-do-i-need-for-32-square-feet
- how-many-bags-of-concrete-do-i-need-for-a-4x8-slab <> how-many-bags-of-concrete-do-i-need-for-a-4x4-slab
- how-many-bags-of-concrete-do-i-need-for-a-4x8-slab <> how-many-bags-of-concrete-do-i-need-for-a-8x8-slab
- how-much-mulch-do-i-need-for-400-square-feet <> how-much-mulch-do-i-need-for-1000-square-feet
- how-much-mulch-do-i-need-for-400-square-feet <> how-much-mulch-do-i-need-for-600-square-feet
- how-much-mulch-do-i-need-for-400-square-feet <> how-much-mulch-do-i-need-for-32-square-feet
- how-many-tiles-do-i-need-for-100-square-feet <> how-many-tiles-do-i-need-for-20-square-feet
- how-many-tiles-do-i-need-for-100-square-feet <> how-many-tiles-do-i-need-for-120-square-feet
- how-many-bags-of-concrete-do-i-need-for-a-4x4-slab <> how-many-bags-of-concrete-do-i-need-for-a-10x12-slab
- how-many-bags-of-concrete-do-i-need-for-a-4x4-slab <> how-many-bags-of-concrete-do-i-need-for-a-20x20-slab
- how-many-bags-of-concrete-do-i-need-for-a-4x4-slab <> how-many-bags-of-concrete-do-i-need-for-a-8x8-slab
- ... and 8 more

## Recommended merges (overlapping intent)

| cluster | URL | recommendation |
|---|---|---|
| soil | how-much-soil-for-raised-bed-calculator-uk | Merge metric/unit variants into the main calculator page. |
| grass-seed | how-much-grass-seed-per-square-foot-canada | Metric/local-unit variant; keep only if it uses metric and local terms. |
| paint | how-much-paint-do-i-need-for-a-door | Door vs front door overlap; merge the generic into the front-door page. |
| topsoil | how-much-topsoil-do-i-need-for-a-lawn | New-lawn vs lawn overlap; merge into the new-lawn page. |
| fertilizer | how-much-fertilizer-per-1000-sq-ft-calculator | Calculator-intent duplicate of the fertilizer pillar. |
| paint | how-much-paint-do-i-need-calculator-sq-ft | Calculator-intent duplicate of the paint pillar. |
| tile | how-many-tiles-do-i-need-for-my-floor | Generic floor page; merge into the room page or pillar. |
| tile | how-many-tiles-do-i-need-for-my-room | Generic room page; merge into the room-size pages. |

## Weak titles / slugs

| slug | title | reason |
|---|---|---|

## Missing SEO elements

| slug | gaps |
|---|---|

## Sitemap issues

- none
