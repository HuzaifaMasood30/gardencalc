/* Client-side calculators. Mirrors scripts/calculators.py exactly. */
(function () {
  "use strict";

  var TONS_PER_CUYD = 1.4;

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
    }
  };

  function r(x, p) { var f = Math.pow(10, p); return Math.round((x + 1e-9) * f) / f; }

  function readForm(form) {
    var out = {};
    form.querySelectorAll("input").forEach(function (i) {
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
      run(form);
    });
  });
})();
