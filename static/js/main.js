/* Client-side calculators. Mirrors scripts/calculators.py exactly. */
(function () {
  "use strict";

  var TONS_PER_CUYD = 1.4;
  var BASE = (typeof window !== "undefined" && window.GC_BASE) || "";

  var CALCS = {
    mulch: function (v) {
      var sqft = v.length * v.width, cuft = sqft * (v.depth / 12), cuyd = cuft / 27;
      return [["Square feet", r(sqft, 1)], ["Cubic feet", r(cuft, 1)],
              ["Cubic yards", r(cuyd, 2)], ["2 cu ft bags", Math.ceil(cuft / 2)]];
    },
    soil: function (v) {
      var cuft = v.length * v.width * (v.height / 12);
      return [["Cubic feet", r(cuft, 1)], ["Cubic yards", r(cuft / 27, 2)],
              ["1.5 cu ft bags", Math.ceil(cuft / 1.5)]];
    },
    gravel: function (v) {
      var sqft = v.length * v.width, cuft = sqft * (v.depth / 12), cuyd = cuft / 27;
      return [["Square feet", r(sqft, 1)], ["Cubic yards", r(cuyd, 2)],
              ["Tons", r(cuyd * TONS_PER_CUYD, 2)]];
    },
    paint: function (v) {
      var wall = 2 * (v.length + v.width) * v.height;
      var ceiling = v.length * v.width;
      var openings = v.doors * 21 + v.windows * 15;
      var paintable = Math.max(wall - openings, 0);
      var total = paintable * v.coats + ceiling * v.coats;
      return [["Wall area (sq ft)", r(wall, 1)], ["Paintable area (sq ft)", r(paintable, 1)],
              ["Gallons", r(total / 350, 2)]];
    },
    tile: function (v) {
      var floor = v.length * v.width;
      var tarea = (v.tile_w / 12) * (v.tile_h / 12);
      var tiles = floor / tarea;
      return [["Floor area (sq ft)", r(floor, 1)], ["Tiles", Math.ceil(tiles)],
              ["With " + v.waste + "% waste", Math.ceil(tiles * (1 + v.waste / 100))]];
    },
    grass_seed: function (v) {
      var rate = Number(v.method) === 1 ? 4.5 : 2.0;
      var lb = v.area / 1000 * rate;
      return [["Rate per 1000 sq ft", rate], ["Pounds", r(lb, 2)],
              ["3 lb bags", Math.ceil(lb / 3)]];
    },
    concrete: function (v) {
      var cuft = v.length * v.width * (v.thickness / 12);
      return [["Cubic feet", r(cuft, 1)], ["Cubic yards", r(cuft / 27, 2)],
              ["60 lb bags", Math.ceil(cuft / 0.45)], ["80 lb bags", Math.ceil(cuft / 0.60)]];
    },
    topsoil: function (v) {
      var sqft = v.length * v.width, cuft = sqft * (v.depth / 12), cuyd = cuft / 27;
      return [["Square feet", r(sqft, 1)], ["Cubic feet", r(cuft, 1)],
              ["Cubic yards", r(cuyd, 2)], ["40 lb bags", Math.ceil(cuft / 0.75)]];
    },
    fertilizer: function (v) {
      var bag = v.bag || 40;
      var lb = v.area / 1000 * v.rate;
      return [["Pounds", r(lb, 2)], ["Bags", Math.ceil(lb / bag)]];
    }
  };

  function r(x, p) { var f = Math.pow(10, p); return Math.round((x + 1e-9) * f) / f; }

  function track(name, params) {
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", name, params || {});
      }
    } catch (e) { /* analytics must never break the page */ }
  }

  function readForm(form) {
    var out = {};
    form.querySelectorAll("input, select").forEach(function (i) {
      if (!i.name) return;
      out[i.name] = parseFloat(i.value);
    });
    return out;
  }

  function calcName(form) { return form.getAttribute("data-calc") || "unknown"; }

  // Reflected query params keep the URL shareable while the canonical stays clean.
  function writeQuery(form) {
    if (!window.history || !window.history.replaceState) return;
    var v = readForm(form);
    var qs = Object.keys(v).map(function (k) {
      return encodeURIComponent(k) + "=" + encodeURIComponent(v[k]);
    }).join("&");
    var url = location.pathname + (qs ? "?" + qs : "");
    try { history.replaceState(null, "", url); } catch (e) { /* ignore */ }
  }

  function applyQuery(form) {
    var p = new URLSearchParams(location.search);
    var any = false;
    form.querySelectorAll("input, select").forEach(function (i) {
      if (!i.name || !p.has(i.name)) return;
      i.value = p.get(i.name);
      any = true;
    });
    return any;
  }

  function buildShareUrl(form) {
    var v = readForm(form);
    var qs = Object.keys(v).map(function (k) {
      return encodeURIComponent(k) + "=" + encodeURIComponent(v[k]);
    }).join("&");
    return location.origin + location.pathname + (qs ? "?" + qs : "");
  }

  var LAST_RESULT = "";

  function run(form, opts) {
    var key = form.getAttribute("data-calc");
    var fn = CALCS[key];
    if (!fn) return;
    var v = readForm(form);
    for (var k in v) { if (!isFinite(v[k])) { v[k] = 0; } }
    var rows = fn(v);
    var box = form.parentNode.querySelector(".calc-result");
    var html = "";
    var plain = [];
    rows.forEach(function (row) {
      html += '<div class="row"><span>' + row[0] + '</span><b>' + row[1] + "</b></div>";
      plain.push(row[0] + ": " + row[1]);
    });
    box.innerHTML = html;
    LAST_RESULT = plain.join("\n");
    if (opts && opts.write !== false) writeQuery(form);
  }

  function initToc() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    var byId = {};
    links.forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      if (el) byId[id] = a;
    });
    var heads = links.map(function (a) {
      return document.getElementById(a.getAttribute("href").slice(1));
    }).filter(Boolean);
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (l) { l.classList.remove("active"); });
          var a = byId[e.target.id];
          if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
    heads.forEach(function (h) { obs.observe(h); });
  }

  function initSearch() {
    var input = document.getElementById("q");
    var out = document.getElementById("results");
    if (!input || !out) return;
    var data = [];
    fetch(BASE + "/static/search-index.json").then(function (r) { return r.json(); })
      .then(function (d) { data = d; input.focus(); run(input.value); })
      .catch(function () { out.innerHTML = "<li>Search index unavailable.</li>"; });
    var pre = new URLSearchParams(location.search).get("q");
    if (pre) input.value = pre;
    function run(q) {
      q = (q || "").trim().toLowerCase();
      var hits = !q ? [] : data.filter(function (a) {
        return (a.t + " " + a.k + " " + a.d + " " + a.c).toLowerCase().indexOf(q) > -1;
      }).slice(0, 40);
      out.innerHTML = hits.length ? hits.map(function (a) {
        return '<li><span><a href="' + BASE + "/" + a.s + '/">' + a.t +
               '</a><span class="excerpt">' + a.d + '</span></span>' +
               '<span class="when">' + a.c + '</span></li>';
      }).join("") : (q ? "<li>No matches. Try 'mulch', 'concrete' or 'seed'.</li>" : "");
    }
    input.addEventListener("input", function () { run(input.value); });
  }

  function initCalcActions(form) {
    applyQuery(form);
    run(form, { write: false });
    var shell = form.parentNode;
    var copy = shell.querySelector(".calc-copy");
    var print = shell.querySelector(".calc-print");
    var share = shell.querySelector(".calc-share");
    if (copy) copy.addEventListener("click", function () {
      track("copy_result", { calculator_name: calcName(form) });
      copyText(LAST_RESULT || "GardenCalc");
    });
    if (print) print.addEventListener("click", function () {
      track("print_result", { calculator_name: calcName(form) });
      window.print();
    });
    if (share) share.addEventListener("click", function () {
      track("share_click", { calculator_name: calcName(form), network: "link" });
      var u = buildShareUrl(form);
      copyText(u);
      if (navigator.share) { navigator.share({ url: u }).catch(function () {}); }
    });
  }

  function copyText(text) {
    try {
      if (navigator.clipboard) { navigator.clipboard.writeText(text); return; }
    } catch (e) { /* fall through */ }
    var ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  function initShare() {
    document.querySelectorAll("[data-share]").forEach(function (el) {
      el.addEventListener("click", function () {
        var net = el.getAttribute("data-share");
        track(net === "pinterest" ? "pin_save_click" : "share_click", { network: net });
        if (net === "copy") {
          copyText(el.getAttribute("data-url") || location.href);
          el.textContent = "Copied!";
          setTimeout(function () { el.textContent = "Copy link"; }, 1500);
        }
      });
    });
  }

  function initEmbedCopy() {
    document.querySelectorAll("[data-copy-embed]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var ta = btn.parentElement.querySelector("textarea");
        if (!ta) return;
        copyText(ta.value);
        track("embed_code_copy", { page: location.pathname });
        var old = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(function () { btn.textContent = old; }, 1500);
      });
    });
  }

  // Which calculator links inside a page actually get clicked - tells us where to add
  // more internal links and which tools people look for next.
  function initInternalCalcClicks() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("-calculator/") === -1) return;
      track("internal_calculator_click", { calculator: href, from: location.pathname });
    });
  }

  function initGuidesFilter() {
    var input = document.getElementById("guides-q");
    if (!input) return;
    var groups = document.querySelectorAll("[data-group]");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      groups.forEach(function (g) {
        var shown = 0;
        g.querySelectorAll("[data-guide]").forEach(function (li) {
          var hit = !q || li.textContent.toLowerCase().indexOf(q) > -1;
          li.style.display = hit ? "" : "none";
          if (hit) shown++;
        });
        g.style.display = shown ? "" : "none";
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var tog = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    if (tog && nav) {
      tog.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        tog.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
    document.querySelectorAll("form.calc-form").forEach(function (form) {
      var go = form.querySelector(".calc-go");
      if (go) go.addEventListener("click", function () {
        track("calculate_click", { calculator_name: calcName(form) });
        run(form);
      });
      form.addEventListener("input", function () { run(form); });
      form.addEventListener("change", function () { run(form); });
      initCalcActions(form);
    });
    initToc();
    initSearch();
    initShare();
    initEmbedCopy();
    initInternalCalcClicks();
    initGuidesFilter();
  });
})();
