"""Pipeline tests. Run with: python -m pytest scripts/tests.py -q  (or python scripts/tests.py)"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import calculators
import keywords
import mdrender
import quality
import seo as seolib
from common import site_config


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
    r = calculators.compute("soil", {"length": 8, "width": 4, "height": 12})
    assert r["bags_1_5cf"] == 22, r
    r = calculators.compute("gravel", {"length": 20, "width": 10, "depth": 3})
    assert abs(r["tons"] - 2.59) < 0.01, r
    r = calculators.compute("concrete", {"length": 10, "width": 10, "thickness": 4})
    assert r["bags_60lb"] == 75 and r["bags_80lb"] == 56, r


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
        ["fertilizer", {"area": 5000, "rate": 1, "bag": 40}],
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
    }
    for kind, inputs in cases:
        py = calculators.compute(kind, inputs)
        rows = js_out[kind]
        for py_key, py_val in py.items():
            label = labels.get(py_key)
            if label and label in rows:
                assert abs(float(rows[label]) - float(py_val)) <= 1.0, \
                    (kind, py_key, rows[label], py_val)


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
