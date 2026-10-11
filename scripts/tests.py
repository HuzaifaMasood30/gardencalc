"""Pipeline tests. Run with: python -m pytest scripts/tests.py -q  (or python scripts/tests.py)"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import calculators
import article_fix
import keywords
import mdrender
import merges
import promotion
import quality
import seasonal
import seo as seolib
import sources as sources_lib
from common import ROOT, site_config


def test_render_adds_heading_ids_and_toc():
    html, toc = mdrender.render_with_toc("## First section\n\ntext\n\n## Second section\n\nmore")
    assert '<h2 id="first-section">' in html
    assert '<h2 id="second-section">' in html
    assert [t["text"] for t in toc] == ["First section", "Second section"], toc


def test_render_escapes_html_but_keeps_markdown():
    html, _ = mdrender.render_with_toc("## Head\n\n<script>alert(1)</script> **bold**")
    assert "<script>" not in html
    assert "<strong>bold</strong>" in html


def test_sitemap_supports_image_extension():
    site = {"name": "T", "base_url": "https://t.example", "language": "en",
            "author": "A", "locale": "en_US"}
    xml = seolib.sitemap_xml(
        [{"loc": "/a/", "priority": "0.9", "image": "https://t.example/img/a.webp",
          "image_title": "A & B"}], site)
    assert 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"' in xml
    assert "<image:loc>https://t.example/img/a.webp</image:loc>" in xml
    assert "A &amp; B" in xml


def test_collection_schema_lists_items():
    cat = {"id": "mulch", "name": "Mulch", "blurb": "b"}
    items = [{"slug": "a", "title": "A"}, {"slug": "b", "title": "B"}]
    site = {"name": "T", "base_url": "https://t.example"}
    sch = seolib.collection_schema(cat, items, site)
    assert sch["@type"] == "CollectionPage"
    assert sch["mainEntity"]["numberOfItems"] == 2
    assert sch["mainEntity"]["itemListElement"][1]["position"] == 2


def test_images_render_per_cluster():
    import images
    if not images.HAVE_PIL:
        return
    for cluster in images.CLUSTERS:
        art = {"slug": "x", "title": "How Much Something Do I Need", "cluster": cluster,
               "meta_description": "A useful summary of the calculation.",
               "calculator_defaults": {"length": 10, "width": 10, "depth": 3,
                                       "height": 8, "thickness": 4, "tile_w": 12,
                                       "tile_h": 12, "waste": 10, "area": 5000}}
        img = images.render_figure(art)
        assert img is not None and img.size == (images.W, images.H), cluster


def test_brand_assets_render():
    import images
    if not images.HAVE_PIL:
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        stats = images.render_brand(Path(d))
        assert stats["logo"] == 1 and stats["og"] == 1
        for name in ("logo.png", "favicon.ico", "apple-touch-icon.png", "og-default.png"):
            p = Path(d) / "img" / name
            assert p.exists() and p.stat().st_size > 0, name


def test_calculator_results():
    r = calculators.compute("mulch", {"length": 20, "width": 10, "depth": 3})
    assert r["bags_2cf"] == 25, r
    # 600 sq ft at 3 in is 150 cu ft; two-cu-ft bags round to 75, not 76.
    r = calculators.compute("mulch", {"length": 30, "width": 20, "depth": 3})
    assert r["bags_2cf"] == 75, r
    r = calculators.compute("soil", {"length": 8, "width": 4, "height": 12})
    assert r["bags_1_5cf"] == 22, r
    r = calculators.compute("gravel", {"length": 20, "width": 10, "depth": 3})
    assert abs(r["tons"] - 2.59) < 0.01, r
    r = calculators.compute("concrete", {"length": 10, "width": 10, "thickness": 4})
    assert r["bags_60lb"] == 75 and r["bags_80lb"] == 56, r
    # Fertilizer: pounds are the *product* weight, derived from the nitrogen share.
    r = calculators.compute("fertilizer", {"area": 5000, "rate": 1, "bag": 40, "nitrogen": 20})
    assert r == {"pounds_nitrogen": 5.0, "pounds": 25.0, "bags": 1}, r
    r = calculators.compute("fertilizer", {"area": 5000, "rate": 1, "bag": 40, "nitrogen": 10})
    assert r["pounds"] == 50.0 and r["bags"] == 2, r
    # A 1,000 sq ft lawn at 1 lb N with a 20-0-0 bag needs 5 lb of product.
    r = calculators.compute("fertilizer", {"area": 1000, "rate": 1, "bag": 40, "nitrogen": 20})
    assert r["pounds"] == 5.0 and r["pounds_nitrogen"] == 1.0, r


def test_article_fix_is_idempotent():
    import article_fix

    arts = [{"slug": "how-much-mulch-do-i-need-for-600-square-feet", "title": "T",
             "cluster": "mulch", "calculator": "mulch", "status": "published",
             "primary_keyword": "how much mulch do i need for 600 square feet",
             "calculator_defaults": {"length": 30, "width": 20, "depth": 3},
             "body_markdown": "## How Much You Need at Common Sizes\n\n"
                              "| Job size | Cubic feet | Cubic yards | 2 cu ft bags |\n"
                              "|---|---|---|---|\n| 600 sq ft | 150 | 5.56 | 76 |\n"}]
    first = article_fix.run(arts)
    second = article_fix.run(arts)
    assert first and not second, (first, second)
    assert "| 600 sq ft | 150 | 5.56 | 75 |" in arts[0]["body_markdown"]


def test_published_tables_match_the_engine():
    """Every cubic-feet table row must agree with the calculators engine."""
    import re

    import article_fix
    from common import DATA, load_json

    arts = load_json(DATA / "articles.json", default=[])
    checked = 0
    for art in arts:
        if art.get("status") not in ("published", "approved"):
            continue
        md = art.get("body_markdown", "")
        lines = md.split("\n")
        for i, line in enumerate(lines):
            if not line.strip().startswith("|") or i + 1 >= len(lines):
                continue
            if not set(lines[i + 1].strip()) <= set("|-: "):
                continue
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            if not any("cubic feet" in h.lower() for h in headers):
                continue
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                by = dict(zip(headers, cells))
                cuft = by.get("Cubic feet")
                size = cells[0]
                m = re.match(r"([\d,]+)\s*sq ft", size, re.I)
                if not (cuft and m):
                    continue
                area = float(m.group(1).replace(",", ""))
                ins = dict(article_fix.headline_inputs(art))
                if "length" not in ins or "width" not in ins:
                    continue
                ins["length"] = ins["width"] = area ** 0.5
                out = calculators.compute(art["calculator"], ins)
                assert abs(float(cuft) - out["cubic_feet"]) <= 0.1, (art["slug"], row, out)
                for h, v in by.items():
                    field = article_fix._LABEL_FIELD.get(h.lower())
                    if field and field in out:
                        assert abs(float(v) - out[field]) <= 1, (art["slug"], row, out)
                        checked += 1
    assert checked > 0


def test_keyword_relevance_filter():
    assert not keywords.is_relevant("how much gravel for a 10 gallon fish tank",
                                     "how much gravel do i need")
    assert keywords.is_relevant("how much mulch do i need for 500 sq ft",
                                "how much mulch do i need")


def test_markdown_escapes_html_and_resolves_links():
    out = mdrender.render("Hi <script>x</script> [a]({{url:mulch-calculator}}).",
                          {"mulch-calculator": "https://x.test/mulch-calculator/"})
    assert "<script>" not in out
    assert "https://x.test/mulch-calculator/" in out


def test_no_orphans_from_singleton_cluster():
    import interlink

    arts = [
        {"slug": "cluster-a-one", "cluster": "a", "title": "A One",
         "primary_keyword": "a one", "quality": {}, "internal_links": []},
        {"slug": "cluster-a-two", "cluster": "a", "title": "A Two",
         "primary_keyword": "a two", "quality": {}, "internal_links": []},
        # A keyword whose cluster has only this member would otherwise be orphaned.
        {"slug": "cluster-solo", "cluster": "solo", "title": "Solo",
         "primary_keyword": "solo", "quality": {}, "internal_links": []},
    ]
    interlink.link_all(arts, persist=False)
    assert interlink.orphans(arts) == [], interlink.orphans(arts)


def test_inject_links_first_mention_only():
    import interlink

    art = {
        "slug": "a",
        "body_markdown": ("Mulch depth matters. Multiply length by width to get the "
                          "area, then divide by the depth. Mulch depth is the same "
                          "step everywhere."),
        "internal_links": [{"to": "how-much-mulch", "anchor": "mulch depth",
                            "title": "How much mulch"}],
    }
    body = interlink.inject(art)
    assert body.count("[Mulch depth]({{url:how-much-mulch}})") == 1, body


def test_inject_matches_on_topic_prefix():
    import interlink

    art = {
        "slug": "a",
        "body_markdown": "For a bed, how much mulch you spread depends on depth.",
        "internal_links": [{"to": "x", "anchor": "how much mulch for a bed",
                            "title": "How much mulch for a bed"}],
    }
    body = interlink.inject(art)
    # The full anchor is absent, but its on-topic prefix 'how much mulch' should
    # still be linked, rather than dropping the link or emitting an empty anchor.
    assert "[how much mulch]({{url:x}})" in body, body


def test_inject_adds_a_body_link_when_prose_never_mentions_a_sibling():
    import interlink

    art = {
        "slug": "concrete-calculator",
        "body_markdown": "This tool returns cubic yards and the number of bags.",
        "internal_links": [{"to": "how-many-bags", "anchor": "how many bags of concrete",
                            "title": "How many bags of concrete do I need"}],
    }
    body = interlink.inject(art)
    assert "({{url:how-many-bags}})" in body, body


def test_promotion_targets_are_unique_and_each_names_a_real_page():
    opps = promotion.opportunities()
    assert len(opps) >= 12
    uids = [o["uid"] for o in opps]
    assert len(uids) == len(set(uids)), "duplicate promotion uid"
    for o in opps:
        # Every recommended post must name a real GardenCalc page, except the
        # deliberate non-promotional Wikipedia decision entry.
        if o["uid"].startswith("citation:"):
            continue
        assert promotion.BASE in o["promote"] or promotion.BASE in o["copy"], o["uid"]
        assert o["copy"].strip(), o["uid"]
        assert o["requirement"], o["uid"]


def test_promotion_duplicate_check_is_clean():
    assert promotion.check() == []


def test_quality_rejects_thin_content():
    art = {"slug": "t", "title": "T", "primary_keyword": "x",
           "body_markdown": "## A\n\ntiny\n", "word_count": 3}
    report = quality.evaluate(art, [art])
    assert not report["passed"]
    assert not report["gates"]["thin_content"]["pass"]


def test_schema_types_present():
    art = {"slug": "mulch-calculator", "title": "Mulch", "meta_description": "d" * 130,
           "created": "2026-01-01", "updated": "2026-01-01", "cluster": "mulch",
           "primary_keyword": "how much mulch", "secondary_keywords": [],
           "faq": [{"q": "q", "a": "a"}]}
    schemas = seolib.all_schema(art, site_config())
    types = {s["@type"] for s in schemas}
    # HowTo is deliberately not emitted; Article + Breadcrumb + FAQ are the baseline.
    assert {"Article", "BreadcrumbList", "FAQPage"} <= types, types


def test_sitemap_is_valid_xml():
    from xml.etree import ElementTree
    xml = seolib.sitemap_xml([{"loc": "/", "priority": "1.0"}], site_config())
    root = ElementTree.fromstring(xml)
    assert root.tag.endswith("urlset")


def test_sitemap_drops_priority_and_bad_lastmod():
    from xml.etree import ElementTree
    site = {"name": "T", "base_url": "https://t.example"}
    xml = seolib.sitemap_xml(
        [{"loc": "/a/", "lastmod": "not-a-date", "priority": "0.9"},
         {"loc": "/b/", "lastmod": "2099-01-01", "priority": "0.9"}],
        site)
    assert "<priority>" not in xml
    root = ElementTree.fromstring(xml)
    assert root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")[0].find(
        "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod") is None


def test_sitemap_dedupes_and_enforces_base_path():
    site = {"name": "T", "base_url": "https://t.example/gardencalc"}
    xml = seolib.sitemap_xml([{"loc": "/a/"}, {"loc": "/a/"}, {"loc": "/b/"}], site)
    assert xml.count("<loc>https://t.example/gardencalc/a/</loc>") == 1
    assert "<loc>https://t.example/a/</loc>" not in xml


def test_merged_pages_become_stubs_and_leave_the_sitemap():
    """Merged pages must keep their URL (for no-404) but drop out of the live site."""
    arts = [
        {"slug": "how-much-mulch-do-i-need-for-my-flower-bed", "title": "A",
         "status": "approved"},
        {"slug": "how-much-mulch-do-i-need-for-a-flower-bed", "title": "B",
         "status": "approved"},
    ]
    merges.apply(arts)
    by = {a["slug"]: a for a in arts}
    assert by["how-much-mulch-do-i-need-for-my-flower-bed"]["status"] == "merged"
    assert by["how-much-mulch-do-i-need-for-my-flower-bed"]["merged_into"] == \
        "how-much-mulch-do-i-need-for-a-flower-bed"
    assert "how-much-mulch-do-i-need-for-my-flower-bed" in merges.merged_slugs()
    stubs = merges.stubs(arts)
    assert any(s["slug"] == "how-much-mulch-do-i-need-for-my-flower-bed" and
               s["target"] == "how-much-mulch-do-i-need-for-a-flower-bed"
               for s in stubs)


def test_rename_stub_keeps_old_url_alive():
    arts = [{"slug": "how-many-bags-of-concrete-do-i-need-for-a-4x8-slab"}]
    stubs = merges.rename_stubs(arts)
    assert any(s["slug"] == "how-many-bags-of-concrete-do-i-need-for-a-4-x8-slab"
               and s["target"] == "how-many-bags-of-concrete-do-i-need-for-a-4x8-slab"
               for s in stubs)
    # When the old slug still exists, no rename stub is emitted.
    assert merges.rename_stubs(
        [{"slug": "how-many-bags-of-concrete-do-i-need-for-a-4-x8-slab"}]) == []


def test_seasonal_pages_have_reference_tables():
    """Every seasonal guide must ship a real HTML table for featured-snippet value."""
    for item in seasonal.SEASONAL:
        assert item.get("table"), item["slug"]
        assert item["table"]["head"] and len(item["table"]["rows"]) >= 3


def test_robots_is_harmless_and_has_no_sitemap_reliance():
    """A project-site robots.txt is never read at the host root, so it must not
    advertise a Sitemap: line; it only needs to permit crawling."""
    txt = seolib.robots_txt({"base_url": "https://example.github.io/repo"})
    assert "User-agent" in txt and "Disallow" not in txt
    assert "Sitemap:" not in txt


def test_rss_items_have_pubdates():
    """RSS must be a valid fallback sitemap: real items with RFC-822 pubDates."""
    arts = [{"title": "T", "slug": "t", "meta_description": "d", "updated": "2026-10-08"}]
    xml = seolib.rss_xml(arts, {"name": "GardenCalc", "tagline": "x",
                             "base_url": "https://example.github.io/repo"})
    assert "<pubDate>Thu, 08 Oct 2026 00:00:00 +0000</pubDate>" in xml


def test_sitemap_lastmod_is_git_derived():
    """build._stamp must return the file's real git commit date, not today."""
    import build
    stamp = build._stamp(ROOT / "scripts" / "seo.py")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp)
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", "scripts/seo.py"],
                         cwd=ROOT, capture_output=True, text=True)
    assert stamp == out.stdout.strip()


def test_js_and_python_calculators_agree():
    """The client-side calculator must produce the same numbers as the Python engine."""
    import json
    import shutil
    import subprocess
    from pathlib import Path as _P

    node = shutil.which("node")
    if not node:
        print("  (skipped: node not installed)")
        return
    root = _P(__file__).resolve().parent.parent
    cases = [
        ["mulch", {"length": 20, "width": 10, "depth": 3}],
        ["soil", {"length": 8, "width": 4, "height": 12}],
        ["gravel", {"length": 20, "width": 10, "depth": 3}],
        ["paint", {"length": 12, "width": 10, "height": 8, "coats": 2, "doors": 1, "windows": 2}],
        ["tile", {"length": 10, "width": 10, "tile_w": 12, "tile_h": 12, "waste": 10}],
        ["grass_seed", {"area": 5000, "method": 1}],
        ["concrete", {"length": 10, "width": 10, "thickness": 4}],
        ["topsoil", {"length": 20, "width": 10, "depth": 2}],
        ["fertilizer", {"area": 5000, "rate": 1, "bag": 40, "nitrogen": 20}],
    ]
    proc = subprocess.run(
        [node, str(root / "scripts/calc_parity.js"), str(root / "static/js/main.js"),
         json.dumps(cases)],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    js_out = json.loads(proc.stdout)

    labels = {
        "square_feet": "Square feet", "cubic_feet": "Cubic feet",
        "cubic_yards": "Cubic yards", "bags_2cf": "2 cu ft bags",
        "bags_1_5cf": "1.5 cu ft bags", "tons": "Tons", "rate_per_1000": "Rate per 1000 sq ft",
        "pounds": "Pounds", "bags_3lb": "3 lb bags", "gallons": "Gallons",
        "bags_60lb": "60 lb bags", "bags_80lb": "80 lb bags",
        "bags_40lb": "40 lb bags", "bags": "Bags",
        "pounds_nitrogen": "Pounds of nitrogen",
    }
    for kind, inputs in cases:
        py = calculators.compute(kind, inputs)
        rows = js_out[kind]
        for py_key, py_val in py.items():
            label = labels.get(py_key)
            if label and label in rows:
                assert abs(float(rows[label]) - float(py_val)) <= 1.0, \
                    (kind, py_key, rows[label], py_val)


def test_homepage_quick_answers_link_to_real_calculators():
    """Every quick-answer row must point at a pillar page that exists.

    The soil row used to build "<calc>-calculator" and fall back to /calculators/
    because the real slug is raised-bed-soil-calculator.
    """
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    home = (root / "site" / "index.html").read_text(encoding="utf-8")
    qa = re.search(r'<ul class="qa-list">(.*?)</ul>', home, re.S)
    assert qa, "no quick-answers list on the homepage"
    links = re.findall(r'<a href="([^"]+)">', qa.group(1))
    assert len(links) >= 6, links
    for href in links:
        path = href.split("/gardencalc", 1)[-1].strip("/")
        assert path, f"quick answer falls back to the calculators index: {href}"
        assert (root / "site" / path / "index.html").exists(), f"dead quick-answer link: {href}"


def test_homepage_lists_every_pillar():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    pillars = [a["slug"] for a in arts if a.get("is_pillar")
               and a.get("status") in ("published", "approved")]
    home = (root / "site" / "index.html").read_text(encoding="utf-8")
    for slug in pillars:
        assert f"/{slug}/" in home, f"pillar {slug} is not linked from the homepage"


def test_no_meta_description_ends_on_a_dangling_word():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    dangling = {"a", "an", "the", "of", "to", "for", "and", "or", "by", "with",
                "in", "on", "at", "as", "is", "are", "was", "were", "be", "been",
                "this", "that", "these", "those", "your", "you", "it", "its",
                "from", "into", "over", "under", "than", "then", "about"}
    bad = []
    for a in arts:
        md = (a.get("meta_description") or "").strip()
        words = re.findall(r"[A-Za-z0-9'%]+", md)
        if md and len(md) <= 158 and words and words[-1].lower() in dangling:
            bad.append(a["slug"])
    assert not bad, f"meta descriptions end mid-phrase: {bad}"


def test_every_calculator_article_has_a_worked_example_and_answer():
    """Task 4: a kept calculator page must show a labelled walk-through and an
    answer-first sentence, or it cannot win a featured snippet."""
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    missing = []
    for a in arts:
        if a.get("status") not in ("published", "approved"):
            continue
        if a["slug"] in merges.MERGES or a["slug"] in article_fix.SPECIAL_SLUGS:
            continue
        if not a.get("calculator"):
            continue
        if not (a.get("answer") or "").strip():
            missing.append(f"{a['slug']} (answer)")
        if not article_fix._has_worked_block(a.get("body_markdown", "")):
            missing.append(f"{a['slug']} (worked example)")
    assert not missing, f"pages missing snippet blocks: {missing}"


def test_calculator_pages_cite_their_sources():
    """Task 5: every calculator page links at least one real source, and the about
    page exposes the methodology the byline points at."""
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    keys = {a.get("calculator") for a in arts if a.get("calculator")}
    for key in keys:
        assert sources_lib.for_key(key), f"no sources mapped for calculator {key}"
    for slug in ("mulch-calculator", "paint-calculator", "concrete-calculator"):
        html = (root / "site" / slug / "index.html").read_text(encoding="utf-8")
        assert 'Sources &amp; method' in html, f"{slug} has no sources section"
        assert "rel=\"nofollow noopener\" target=\"_blank\"" in html, f"{slug} sources are not linked"
    about = (root / "site" / "about" / "index.html").read_text(encoding="utf-8")
    assert 'id="methodology"' in about, "about page has no #methodology anchor"


def test_article_schema_is_well_formed():
    """Task 6: JSON-LD must carry stable @ids, real dates and matching FAQ text."""
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    for slug in ("mulch-calculator", "paint-calculator",
                 "how-many-tiles-do-i-need-for-a-10x10-room"):
        html = (root / "site" / slug / "index.html").read_text(encoding="utf-8")
        blocks = [json.loads(b) for b in
                  re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
        by_type = {b.get("@type"): b for b in blocks}
        art = by_type["Article"]
        assert art["@id"].endswith("#article"), art["@id"]
        assert art["author"]["url"].endswith("/about/"), art["author"]
        assert art["publisher"]["logo"]["width"] and art["publisher"]["url"], art["publisher"]
        assert art["datePublished"] and art["dateModified"], "article dates missing"
        assert art["dateModified"] >= art["datePublished"], f"{slug} modified before published"
        assert art["isAccessibleForFree"] is True
        faq = by_type.get("FAQPage")
        if faq:
            for q in faq["mainEntity"]:
                assert q["name"][:25] in html, f"FAQ not visible on page: {q['name']}"
        webapp = by_type.get("WebApplication")
        if webapp:
            assert webapp["@id"].endswith("#app")
            assert webapp["offers"]["price"] == "0"
    arts_by_slug = {a["slug"]: a for a in arts}
    assert arts_by_slug["mulch-calculator"]["updated"] >= arts_by_slug["mulch-calculator"]["created"]


def test_every_published_page_has_inbound_links_and_shallow_depth():
    """Task 7: no page is more than 3 clicks from the homepage, and each published
    page has at least two inbound links in the rendered site (not just the link graph,
    which the per-article cap can hold at one)."""
    import json
    from collections import Counter, deque
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    site = root / "site"
    arts = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))
    published = {a["slug"] for a in arts
                 if a.get("status") in ("published", "approved") and a["slug"] not in merges.MERGES}

    def outbound(slug: str) -> set[str]:
        html = (site / slug / "index.html").read_text(encoding="utf-8")
        return {m for m in re.findall(r'/gardencalc/([a-z0-9-]+)/', html) if m != slug}

    depth: dict[str, int] = {}
    queue = deque([""])
    while queue:
        cur = queue.popleft()
        page = site / ("index.html" if cur == "" else f"{cur}/index.html")
        if not page.exists():
            continue
        for nxt in outbound(cur) if cur else {
                m for m in re.findall(r'/gardencalc/([a-z0-9-]+)/',
                                      page.read_text(encoding="utf-8"))}:
            if (site / nxt / "index.html").exists() and nxt not in depth:
                depth[nxt] = depth.get(cur, 0) + 1
                queue.append(nxt)
    unreachable = sorted(s for s in published if s not in depth)
    assert not unreachable, f"pages unreachable from the homepage: {unreachable}"
    deep = sorted((s, depth[s]) for s in published if depth[s] > 3)
    assert not deep, f"pages deeper than 3 clicks: {deep}"

    inbound = Counter()
    for page in site.rglob("index.html"):
        source = page.relative_to(site).parent.as_posix()
        html = page.read_text(encoding="utf-8")
        for target in set(re.findall(r'/gardencalc/([a-z0-9-]+)/', html)):
            if target in published and target != source:
                inbound[target] += 1
    weak = sorted(s for s in published if inbound[s] < 2)
    assert not weak, f"pages with fewer than two inbound links: {weak}"


def test_autumn_guides_carry_regional_and_current_timing():
    """Task 8: the two autumn guides must answer the regional and 'this month'
    questions a searcher asks, and be surfaced on the homepage while in season."""
    import datetime as dt
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    for slug in ("when-to-overseed-a-lawn", "fall-lawn-fertilizer-timing"):
        html = (root / "site" / slug / "index.html").read_text(encoding="utf-8")
        assert "by region" in html, f"{slug} has no regional table"
        assert "season-now" in html, f"{slug} has no current-timing line"
        assert "<h2" in html and html.count("<h1") == 1
    item = next(i for i in seasonal.SEASONAL if i["slug"] == "when-to-overseed-a-lawn")
    assert item["updated"] >= "2026-09-01", "autumn guide not refreshed for the season"
    assert "October" in " ".join(p for s in item["sections"] for p in s["paras"])
    assert any("October" in q for q, _ in item["faqs"])
    # The homepage seasonal feature is month-gated, so it must be present in October.
    if dt.date.today().month in item["season_months"]:
        home = (root / "site" / "index.html").read_text(encoding="utf-8")
        assert "when-to-overseed-a-lawn" in home and "In season right now" in home


def test_every_indexable_page_has_a_real_og_image():
    """Task 9: social previews must resolve to a page-specific card, not a
    broken path, and the article hero image must be preloaded for LCP."""
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    site = root / "site"
    bad = []
    for page in site.rglob("index.html"):
        rel = page.relative_to(site).parent.as_posix()
        if rel.startswith("embed"):  # noindex iframes, not shared as pages
            continue
        html = page.read_text(encoding="utf-8")
        m = re.search(r'property="og:image" content="([^"]+)"', html)
        assert m, f"{rel} has no og:image"
        rel_img = m.group(1).split("/gardencalc/")[-1]
        if not (site / rel_img).exists():
            bad.append((rel, rel_img))
    assert not bad, f"og:image paths do not exist: {bad}"
    hero = (site / "mulch-calculator" / "index.html").read_text(encoding="utf-8")
    assert 'rel="preload" as="image"' in hero, "article hero image is not preloaded"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
