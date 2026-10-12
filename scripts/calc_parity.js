/* Verifies the browser calculator (static/js/main.js) matches scripts/calculators.py.
   Run: node scripts/calc_parity.js static/js/main.js */
global.document = {
  addEventListener() {},
  querySelectorAll() { return []; },
  querySelector() { return null; }
};
const fs = require("fs");
const path = process.argv[2];
const arg4 = process.argv[4];
const system = arg4 === "metric" || arg4 === "conv" ? arg4 : "imperial";
const exportName = system === "metric" ? "CALCS_M" : "CALCS";
let src = fs.readFileSync(path, "utf8");
const close = src.lastIndexOf("})();");
src = src.slice(0, close) +
  "globalThis.__C = " + exportName + "; globalThis.__CV = convertValue;\n})();";
eval(src);

const cases = JSON.parse(process.argv[3] || "[]");
if (system === "conv") {
  // [[conv, system, value], ...] -> [converted, ...]
  console.log(JSON.stringify(cases.map(([c, sys, v]) => __CV(v, c, sys))));
} else {
  const out = {};
  for (const [kind, inputs] of cases) {
    out[kind] = Object.fromEntries(__C[kind](inputs));
  }
  console.log(JSON.stringify(out));
}
