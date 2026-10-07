"""Quality gates. An article that fails is quarantined, never published."""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from common import DATA, load_json, seo_config, word_count

AI_CLICHES = [
    "in today's fast-paced world", "in the ever-evolving", "it is important to note",
    "delve into", "tapestry", "navigate the complexities", "unlock the secrets",
    "game-changer", "in conclusion,", "furthermore, it is", "when it comes to",
    "at the end of the day", "elevate your", "seamless", "leverage the power",
    "embark on a journey", "treasure trove", "in the realm of", "testament to",
    "it goes without saying", "needless to say",
]

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.M)

# Set by evaluate() so gates can see the whole article set without changing every
# gate signature.
_CURRENT_ARTS: list[dict] = []


def _all_articles() -> list[dict]:
    return _CURRENT_ARTS


def _text(body: str) -> str:
    t = re.sub(r"```.*?```", "", body, flags=re.S)
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.M)
    # Collapse whitespace so markdown/table spacing differences do not hide duplicates.
    t = re.sub(r"\s+", " ", t)
    return t


def gate_thin(art: dict, seo: dict) -> tuple[bool, str]:
    wc = art.get("word_count") or word_count(art.get("body_markdown", ""))
    ok = wc >= seo["limits"]["min_word_count"]
    return ok, f"word count {wc} (min {seo['limits']['min_word_count']})"


def gate_duplicate(art: dict, arts: list[dict], seo: dict) -> tuple[bool, str]:
    body = _text(art.get("body_markdown", "")).lower()
    worst, worst_slug = 0.0, ""
    for other in arts:
        if other["slug"] == art["slug"]:
            continue
        ratio = SequenceMatcher(None, body[:6000],
                                _text(other.get("body_markdown", "")).lower()[:6000]).ratio()
        if ratio > worst:
            worst, worst_slug = ratio, other["slug"]
    return worst < 0.55, f"max similarity {worst:.2f} vs {worst_slug or 'n/a'}"


def gate_stuffing(art: dict, seo: dict) -> tuple[bool, str]:
    body = _text(art.get("body_markdown", "")).lower()
    words = re.findall(r"\b[\w'-]+\b", body)
    if not words:
        return False, "empty body"
    kw = art.get("primary_keyword", "").lower()
    hits = body.count(kw) if kw else 0
    density = (hits * len(kw.split())) / max(len(words), 1) * 100
    # 3% is natural-language spam territory; tables legitimately repeat the material
    # name, so allow up to 4%. Real stuffing runs far higher than this.
    return density <= 4.0, f"keyword density {density:.2f}%"


def gate_cliches(art: dict, seo: dict) -> tuple[bool, str]:
    body = _text(art.get("body_markdown", "")).lower()
    found = [c for c in AI_CLICHES if c in body]
    return len(found) <= 2, f"cliches: {found or 'none'}"


def gate_readability(art: dict, seo: dict) -> tuple[bool, str]:
    body = _text(art.get("body_markdown", ""))
    sentences = [s for s in re.split(r"[.!?]+", body) if s.strip()]
    if not sentences:
        return False, "no sentences"
    avg = sum(len(s.split()) for s in sentences) / len(sentences)
    return avg <= 28, f"avg sentence length {avg:.1f} words"


def gate_headings(art: dict, seo: dict) -> tuple[bool, str]:
    heads = HEADING_RE.findall(art.get("body_markdown", ""))
    h2 = [h for lvl, h in heads if lvl == "##"]
    h3 = [h for lvl, h in heads if lvl == "###"]
    # Require a real hierarchy of h2 sections and forbid an in-body h1 (the page
    # template supplies the single h1). h3 is optional.
    ok = len(h2) >= 3 and not re.search(r"^#\s", art.get("body_markdown", ""), re.M)
    return ok, f"h2={len(h2)} h3={len(h3)} (no h1 in body)"


def gate_data(art: dict, seo: dict) -> tuple[bool, str]:
    ok = bool(art.get("calculator")) and bool(art.get("calculator_output"))
    return ok, "has calculator + computed output" if ok else "missing calculator data"


def gate_meta(art: dict, seo: dict) -> tuple[bool, str]:
    m = art.get("meta_description", "")
    ok = seo["meta_min"] <= len(m) <= seo["meta_max"]
    return ok, f"meta length {len(m)}"


def gate_title(art: dict, seo: dict) -> tuple[bool, str]:
    t = art.get("title", "")
    ok = 15 <= len(t) <= seo["title_max"] and not t.endswith(" ")
    return ok, f"title length {len(t)}"


def gate_links(art: dict, seo: dict) -> tuple[bool, str]:
    n = len(art.get("internal_links", []))
    lo = seo["limits"]["min_internal_links_per_article"]
    hi = seo["limits"]["max_internal_links_per_article"]
    # Cold start: a young site has few articles to link to, so scale the minimum
    # down to however many others exist rather than failing every early article.
    available = len([a for a in _all_articles() if a.get("status") in ("published", "approved")
                     and a["slug"] != art.get("slug", "")])
    eff_lo = min(lo, available)
    return eff_lo <= n <= hi, f"internal links {n} (want {eff_lo}-{hi}, {available} available)"


def gate_schema(art: dict, seo: dict) -> tuple[bool, str]:
    ok = bool(art.get("schema_types"))
    return ok, f"schema: {art.get('schema_types')}"


def gate_alt(art: dict, seo: dict) -> tuple[bool, str]:
    # The hero image alt is derived from the title at build time; require a title.
    ok = len(art.get("title", "")) > 10
    return ok, "hero alt derivable from title"


GATES = {
    "thin_content": gate_thin,
    "duplicate_content": gate_duplicate,
    "keyword_stuffing": gate_stuffing,
    "ai_cliches": gate_cliches,
    "readability": gate_readability,
    "heading_structure": gate_headings,
    "has_calculator_or_data": gate_data,
    "meta_length": gate_meta,
    "title_length": gate_title,
    "internal_links": gate_links,
    "schema_present": gate_schema,
    "alt_text": gate_alt,
}

WEIGHTS = {
    "thin_content": 20, "duplicate_content": 15, "keyword_stuffing": 10,
    "ai_cliches": 10, "readability": 5, "heading_structure": 8,
    "has_calculator_or_data": 12, "meta_length": 5, "title_length": 5,
    "internal_links": 5, "schema_present": 3, "alt_text": 2,
}


def evaluate(art: dict, arts: list[dict]) -> dict:
    global _CURRENT_ARTS
    _CURRENT_ARTS = arts
    seo = seo_config()
    gates, score, total = {}, 0.0, sum(WEIGHTS.values())
    for name, fn in GATES.items():
        if not seo["gates"].get(name, True):
            gates[name] = {"pass": True, "detail": "disabled"}
            score += WEIGHTS[name]
            continue
        try:
            ok, detail = fn(art, arts, seo) if name == "duplicate_content" else fn(art, seo)
        except Exception as e:  # a broken gate must not crash the run
            ok, detail = False, f"gate error: {e}"
        gates[name] = {"pass": bool(ok), "detail": detail}
        if ok:
            score += WEIGHTS[name]
    pct = round(score / total * 100, 1)
    passed = all(g["pass"] for g in gates.values())
    return {"score": pct, "passed": passed, "gates": gates}


def apply(arts: list[dict]) -> list[dict]:
    seo = seo_config()
    min_score = seo["limits"]["min_quality_score"]
    for art in arts:
        if art.get("status") in ("published",) and art.get("quality", {}).get("passed"):
            continue
        q = evaluate(art, arts)
        art["quality"] = q
        if q["passed"] and q["score"] >= min_score:
            art["status"] = "approved"
        else:
            art["status"] = "rejected"
    return arts


if __name__ == "__main__":
    from common import save_json
    items = load_json(DATA / "articles.json", default=[])
    apply(items)
    save_json(DATA / "articles.json", items)
    for a in items:
        q = a["quality"]
        print(f"{a['status']:9s} {q['score']:5.1f}  {a['slug']}")
        for name, g in q["gates"].items():
            if not g["pass"]:
                print(f"           FAIL {name}: {g['detail']}")
