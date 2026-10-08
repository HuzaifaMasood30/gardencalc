# AGENTS.md — repository memory (GardenCalc)

## What this is
Automated static SEO site: home & garden calculators + how-to guides.
Live: https://huzaifamasood30.github.io/gardencalc/  (GitHub Pages, project site)
Repo: HuzaifaMasood30/gardencalc. Deploy = GitHub Actions `SEO pipeline`.

## Pipeline
`python scripts/run_all.py --limit N` runs the whole chain:
generate -> internal links -> quality gates -> build -> monitor -> dashboard -> report.
- `scripts/generate.py` needs `GEMINI_API_KEY`. Without it, long-tail articles are
  deliberately SKIPPED (templated fallbacks would be thin/duplicate). Pillars still use
  the curated fallback text.
- `scripts/llm.py` uses a MODEL_CHAIN fallback. gemini-3.6-flash frequently returns
  HTTP 429/503, so gemini-3.1-flash-lite is the usual effective model.
- Workflows: `.github/workflows/pipeline.yml` (daily 06:17 UTC, also workflow_dispatch
  with input `limit`), `.github/workflows/health.yml` (daily 07:43 UTC).
- There is no push trigger; changes to scripts/data only redeploy after a dispatch or
  the scheduled run. Dispatch: POST /actions/workflows/pipeline.yml/dispatches.

## Conventions / gotchas
- Cluster assignment lives in `scripts/keywords.py` (`guess_cluster`, `CLUSTER_HINTS`)
  and is reused by `scripts/cluster.py`. Matching is word-boundary based so "topsoil"
  is not captured by the "soil" cluster.
- Off-topic autosuggest results are blocked in `NOISE` (board games, aquariums, etc.).
  Add new distractors there rather than deleting pages after the fact.
- Calculators are implemented twice and MUST stay in sync:
  `scripts/calculators.py` (Python) and `static/js/main.js` (browser).
  Parity is tested in `scripts/tests.py` via `scripts/calc_parity.js`.
- `data/articles.json` is the source of truth for published pages; status must be
  `approved` to publish. Internal links are rebuilt every run (do not clear links on
  rejection — that caused a permanent re-reject loop).

## Validation
```bash
python3 scripts/tests.py                 # 7 unit/parity tests
python3 scripts/live_audit.py https://huzaifamasood30.github.io/gardencalc/
```

## Access notes
- Actions Secrets API is not reachable by the agent token (403); the repo secret
  GEMINI_API_KEY must be added by the user in the GitHub UI.
- Google/Bing console verification and sitemap submission require the user's account.
