/* Verifies the browser calculator (static/js/main.js) matches scripts/calculators.py.
   Run: node scripts/calc_parity.js static/js/main.js */
global.document = {
  addEventListener() {},
  querySelectorAll() { return []; },
  querySelector() { return null; }
};
const fs = require("fs");
const path = process.argv[2];
let src = fs.readFileSync(path, "utf8");
const close = src.lastIndexOf("})();");
src = src.slice(0, close) + "globalThis.__C = CALCS;\n})();";
eval(src);

const cases = JSON.parse(process.argv[3] || "[]");
const out = {};
for (const [kind, inputs] of cases) {
  out[kind] = Object.fromEntries(__C[kind](inputs));
}
console.log(JSON.stringify(out));
