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

  function readForm(form) {
    var out = {};
    form.querySelectorAll("input, select").forEach(function (i) {
      if (!i.name) return;
      out[i.name] = parseFloat(i.value);
    });
    return out;
  }

  function run(form) {
    var key = form.getAttribute("data-calc");
    var fn = CALCS[key];
    if (!fn) return;
    var v = readForm(form);
    for (var k in v) { if (!isFinite(v[k])) { v[k] = 0; } }
    var rows = fn(v);
    var box = form.parentNode.querySelector(".calc-result");
    var html = "";
    rows.forEach(function (row) {
      html += '<div class="row"><span>' + row[0] + '</span><b>' + row[1] + "</b></div>";
    });
    box.innerHTML = html;
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
      if (go) go.addEventListener("click", function () { run(form); });
      form.addEventListener("input", function () { run(form); });
      form.addEventListener("change", function () { run(form); });
      run(form);
    });
    initToc();
    initSearch();
  });
})();
