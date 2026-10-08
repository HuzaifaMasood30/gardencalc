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
      // Fall back to the same defaults the full calculator ships with, so a form that
      // omits doors/windows (the compact homepage tool) cannot produce NaN.
      var doors = isFinite(v.doors) ? v.doors : 1;
      var windows = isFinite(v.windows) ? v.windows : 2;
      var openings = doors * 21 + windows * 15;
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

  // "Show working": the same numbers the engine used, written out as the formula, so a
  // visitor can check the maths. Text only — no results are recomputed here.
  var WORKING = {
    mulch: function (v) {
      var sf = v.length * v.width, df = v.depth / 12, cf = sf * df;
      return "Square feet = " + v.length + " x " + v.width + " = " + r(sf, 1) +
        " ft². Depth in feet = " + v.depth + " / 12 = " + r(df, 4) +
        ". Cubic feet = " + r(sf, 1) + " x " + r(df, 4) + " = " + r(cf, 1) +
        ". Cubic yards = " + r(cf, 1) + " / 27 = " + r(cf / 27, 2) +
        ". 2 cu ft bags = " + r(cf, 1) + " / 2 = " + Math.ceil(cf / 2) + ".";
    },
    soil: function (v) {
      var hf = v.height / 12, cf = v.length * v.width * hf;
      return "Cubic feet = " + v.length + " x " + v.width + " x (" + v.height + " / 12) = " + r(cf, 1) +
        " ft³. Cubic yards = " + r(cf, 1) + " / 27 = " + r(cf / 27, 2) +
        ". 1.5 cu ft bags = " + r(cf, 1) + " / 1.5 = " + Math.ceil(cf / 1.5) + ".";
    },
    gravel: function (v) {
      var sf = v.length * v.width, df = v.depth / 12, cy = sf * df / 27;
      return "Square feet = " + v.length + " x " + v.width + " = " + r(sf, 1) +
        " ft². Cubic yards = " + r(sf, 1) + " x " + r(df, 4) + " / 27 = " + r(cy, 2) +
        ". Tons = " + r(cy, 2) + " x " + TONS_PER_CUYD + " = " + r(cy * TONS_PER_CUYD, 2) + ".";
    },
    concrete: function (v) {
      var tf = v.thickness / 12, cf = v.length * v.width * tf, cy = cf / 27;
      return "Cubic feet = " + v.length + " x " + v.width + " x (" + v.thickness + " / 12) = " + r(cf, 1) +
        " ft³. Cubic yards = " + r(cf, 1) + " / 27 = " + r(cy, 2) +
        ". 80 lb bags = " + r(cf, 1) + " / 0.60 = " + Math.ceil(cf / 0.6) +
        "; 60 lb bags = " + r(cf, 1) + " / 0.45 = " + Math.ceil(cf / 0.45) + ".";
    },
    paint: function (v) {
      var wall = 2 * (v.length + v.width) * v.height;
      var d = isFinite(v.doors) ? v.doors : 1, w = isFinite(v.windows) ? v.windows : 1;
      var paintable = wall - 21 * d - 15 * w, gallons = paintable * v.coats / 350;
      return "Wall area = 2 x (" + v.length + " + " + v.width + ") x " + v.height + " = " + r(wall, 1) +
        " ft². Less 21 ft² per door x " + d + " and 15 ft² per window x " + w + " = " + r(paintable, 1) +
        " ft² paintable. Gallons = " + r(paintable, 1) + " x " + v.coats + " / 350 = " + r(gallons, 2) + ".";
    },
    tile: function (v) {
      var floor = v.length * v.width;
      var tileArea = (v.tile_w / 12) * (v.tile_h / 12);
      var tiles = floor / tileArea, waste = isFinite(v.waste) ? v.waste : 0;
      return "Floor area = " + v.length + " x " + v.width + " = " + r(floor, 1) + " ft². Tile area = (" +
        v.tile_w + " / 12) x (" + v.tile_h + " / 12) = " + r(tileArea, 4) + " ft². Tiles = " + r(floor, 1) +
        " / " + r(tileArea, 4) + " = " + Math.ceil(tiles) + ". With " + waste + "% waste = " +
        Math.ceil(tiles * (1 + waste / 100)) + ".";
    },
    grass_seed: function (v) {
      var rate = (v.method === 2 ? 2 : 4.5), lb = v.area / 1000 * rate;
      return "Rate = " + rate + " lb per 1,000 ft² for " + (v.method === 2 ? "overseeding" : "a new lawn") +
        ". Pounds = " + v.area + " / 1,000 x " + rate + " = " + r(lb, 1) +
        " lb. 3 lb bags = " + r(lb, 1) + " / 3 = " + Math.ceil(lb / 3) + ".";
    },
    fertilizer: function (v) {
      var lb = v.area / 1000 * v.rate;
      return "Pounds of nitrogen = " + v.area + " / 1,000 x " + v.rate + " = " + r(lb, 1) +
        " lb N. Pounds of product = lb N / (N share of the bag). Bags = pounds of product / " + v.bag + " lb.";
    },
    topsoil: function (v) {
      var sf = v.length * v.width, df = v.depth / 12, cf = sf * df;
      return "Square feet = " + v.length + " x " + v.width + " = " + r(sf, 1) +
        " ft². Cubic feet = " + r(sf, 1) + " x " + r(df, 4) + " = " + r(cf, 1) +
        ". Cubic yards = " + r(cf, 1) + " / 27 = " + r(cf / 27, 2) + ".";
    },
  };

  function showWorking(form) {
    var key = form.getAttribute("data-calc");
    var shell = form.closest(".calc");
    var box = shell && shell.querySelector("[data-working]");
    if (!box) return;
    var fn = WORKING[key];
    if (!fn) { box.textContent = ""; return; }
    box.textContent = fn(readForm(form));
  }

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
    if (opts && opts.animate) {
      document.dispatchEvent(new CustomEvent("gc:result", { detail: { box: box, form: form } }));
    }
    if (opts && opts.write !== false && !form.closest("[data-quick]")) writeQuery(form);
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

  // Homepage quick calculator: one shared engine, tabbed panels, preset chips.
  function initQuickCalc() {
    var root = document.querySelector("[data-quick]");
    if (!root) return;
    var tabs = Array.prototype.slice.call(root.querySelectorAll("[data-qtab]"));
    var panels = Array.prototype.slice.call(root.querySelectorAll("[data-qpanel]"));
    var tablist = root.querySelector(".quick-tabs");

    function activate(key, focusTab) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-qtab") === key;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.setAttribute("tabindex", on ? "0" : "-1");
        if (on && focusTab) t.focus();
      });
      panels.forEach(function (p) {
        var on = p.getAttribute("data-qpanel") === key;
        p.classList.toggle("is-hidden", !on);
        if (on) { p.removeAttribute("hidden"); } else { p.setAttribute("hidden", ""); }
      });
      var form = root.querySelector('[data-qpanel="' + key + '"] form.calc-form');
      if (form) { run(form, { write: false }); showWorking(form); }
    }

    // Wire each panel's own Calculate, Copy and Share buttons. These controls live in the
    // hero on every page view, so the generic calc wiring deliberately skips this subtree.
    root.querySelectorAll("[data-qpanel]").forEach(function (panel) {
      var form = panel.querySelector("form.calc-form");
      if (!form) return;
      var shell = panel.querySelector(".calc");
      var go = form.querySelector(".calc-go");
      if (go) go.addEventListener("click", function () {
        track("calculate_click", { calculator_name: calcName(form), location: "quick" });
        run(form, { write: false, animate: true });
        showWorking(form);
        var out = shell && shell.querySelector(".calc-result");
        if (out) { out.setAttribute("tabindex", "-1"); out.focus({ preventScroll: true }); }
      });
      form.addEventListener("input", function () { run(form, { write: false }); showWorking(form); });
      form.addEventListener("change", function () { run(form, { write: false }); showWorking(form); });
      var copy = shell && shell.querySelector(".calc-copy");
      if (copy) copy.addEventListener("click", function () {
        track("copy_result", { calculator_name: calcName(form) });
        copyText(LAST_RESULT || "GardenCalc");
      });
      var share = shell && shell.querySelector(".calc-share");
      if (share) share.addEventListener("click", function () {
        track("share_click", { calculator_name: calcName(form), network: "link" });
        var v = readForm(form);
        var qs = Object.keys(v).map(function (k) {
          return encodeURIComponent(k) + "=" + encodeURIComponent(v[k]);
        }).join("&");
        var u = location.origin + location.pathname + (qs ? "?" + qs : "");
        copyText(u);
        if (navigator.share) { navigator.share({ url: u }).catch(function () {}); }
      });
    });

    tabs.forEach(function (t) {
      t.addEventListener("click", function () { activate(t.getAttribute("data-qtab"), false); });
    });
    if (tablist) tablist.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      var i = tabs.findIndex(function (t) { return t.getAttribute("aria-selected") === "true"; });
      var n = e.key === "ArrowRight" ? (i + 1) % tabs.length : (i - 1 + tabs.length) % tabs.length;
      e.preventDefault();
      activate(tabs[n].getAttribute("data-qtab"), true);
    });

    root.querySelectorAll("[data-preset]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var panel = btn.closest("[data-qpanel]");
        var form = panel && panel.querySelector("form.calc-form");
        if (!form) return;
        var vals;
        try { vals = JSON.parse(btn.getAttribute("data-preset")); } catch (e) { return; }
        Object.keys(vals).forEach(function (k) {
          var field = form.querySelector('[name="' + k + '"]');
          if (field) field.value = vals[k];
        });
        track("quick_preset", { calculator_name: calcName(form), preset: btn.textContent.trim() });
        run(form, { write: false });
        showWorking(form);
      });
    });

    var firstTab = tabs.length ? tabs[0].getAttribute("data-qtab") : null;
    if (firstTab) activate(firstTab, false);
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

  // Click-to-load YouTube facade: no third-party request until the user asks for it,
  // and youtube-nocookie keeps the page privacy-friendly.
  function initVideoFacade() {
    document.querySelectorAll(".video-facade").forEach(function (box) {
      var btn = box.querySelector(".video-load");
      if (!btn) return;
      btn.addEventListener("click", function () {
        var id = box.getAttribute("data-video-id");
        if (!id || !/^[A-Za-z0-9_-]{6,20}$/.test(id)) return;
        var title = box.getAttribute("data-title") || "Video";
        var frame = document.createElement("iframe");
        frame.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
        frame.title = title;
        frame.loading = "lazy";
        frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        frame.setAttribute("allowfullscreen", "");
        frame.className = "video-frame";
        box.innerHTML = "";
        box.appendChild(frame);
        track("video_play", { calculator_name: title });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var tog = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    var mega = document.querySelector(".mega");
    if (mega) {
      // Native <details> keeps the menu usable without JS; add the conveniences:
      // only one panel open, close on outside click, and Escape returns focus.
      document.addEventListener("click", function (e) {
        if (mega.open && !mega.contains(e.target)) mega.open = false;
      });
      mega.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
          mega.open = false;
          var s = mega.querySelector("summary");
          if (s) s.focus();
        }
      });
    }
    if (tog && nav) {
      var setOpen = function (open) {
        nav.classList.toggle("open", open);
        tog.setAttribute("aria-expanded", open ? "true" : "false");
      };
      tog.addEventListener("click", function () {
        setOpen(!nav.classList.contains("open"));
      });
      // Escape closes the mobile drawer and returns focus to the toggle.
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && nav.classList.contains("open")) {
          setOpen(false);
          tog.focus();
        }
      });
    }
    document.querySelectorAll("form.calc-form").forEach(function (form) {
      // The homepage quick calculator is wired by initQuickCalc, which adds its own
      // tab/preset handling and keeps the shared URL clean. Skip it here.
      if (form.closest("[data-quick]")) return;
      var go = form.querySelector(".calc-go");
      if (go) go.addEventListener("click", function () {
        track("calculate_click", { calculator_name: calcName(form) });
        run(form, { animate: true });
        showWorking(form);
        // On narrow screens the result sits below the inputs, so bring it into view.
        if (window.innerWidth < 821) {
          var out = form.parentNode.querySelector(".calc-result");
          if (out) { out.setAttribute("tabindex", "-1"); out.focus({ preventScroll: true }); out.scrollIntoView({ block: "nearest", behavior: "smooth" }); }
        }
      });
      form.addEventListener("input", function () { run(form); showWorking(form); });
      form.addEventListener("change", function () { run(form); showWorking(form); });
      form.parentElement.querySelectorAll(".calc-presets .chip").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var vals;
          try { vals = JSON.parse(btn.getAttribute("data-preset")); } catch (e) { return; }
          Object.keys(vals).forEach(function (k) {
            var field = form.querySelector('[name="' + k + '"]');
            if (field) field.value = vals[k];
          });
          track("preset_click", { calculator_name: calcName(form), preset: btn.textContent.trim() });
          run(form);
          showWorking(form);
        });
      });
      initCalcActions(form);
      showWorking(form);
      // "Save to Pinterest" on the calculator card points at the page image + result.
      var pin = form.parentElement.querySelector(".calc-pin");
      if (pin) {
        var desc = (form.getAttribute("aria-label") || document.title) + " — free calculator by " + location.host;
        pin.href = "https://www.pinterest.com/pin/create/button/?url=" +
          encodeURIComponent(location.origin + location.pathname) +
          "&description=" + encodeURIComponent(desc);
      }
    });
    initToc();
    initSearch();
    initQuickCalc();
    initShare();
    initEmbedCopy();
    initInternalCalcClicks();
    initGuidesFilter();
    initVideoFacade();
    initCountUp();
  });

  // Count-up animation for freshly calculated results (<=300 ms), skipped for reduced motion.
  function initCountUp() {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    document.addEventListener("gc:result", function (e) {
      var box = e.detail && e.detail.box;
      if (!box) return;
      box.querySelectorAll(".row b").forEach(function (b) {
        var m = /^([\d.,]+)(.*)$/.exec(b.textContent.trim());
        if (!m) return;
        var target = parseFloat(m[1].replace(/,/g, ""));
        if (!isFinite(target) || target <= 0) return;
        var suffix = m[2], dec = (m[1].split(".")[1] || "").length;
        var start = performance.now(), dur = 280;
        function step(now) {
          var p = Math.min((now - start) / dur, 1);
          var val = (target * (1 - Math.pow(1 - p, 3)));
          b.textContent = val.toFixed(dec) + suffix;
          if (p < 1) requestAnimationFrame(step); else b.textContent = target.toFixed(dec) + suffix;
        }
        requestAnimationFrame(step);
      });
    });
  }
})();
