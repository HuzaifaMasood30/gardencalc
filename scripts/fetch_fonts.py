"""Download the latin subsets of Fraunces and Inter for self-hosting.

Both families ship as variable fonts, so Google serves one file per family that
covers every requested weight. We keep only the /* latin */ blocks (the site is
English-only) and download each into static/fonts/. The @font-face rules live at
the top of static/css/style.css so the page needs no extra stylesheet request.

Run once; the .woff2 files are committed.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "fonts"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

FAMILIES = [
    ("Fraunces", "opsz,wght@9..144,600;9..144,700", "fraunces-var.woff2"),
    ("Inter", "wght@400;500;600;700", "inter-var.woff2"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for family, spec, name in FAMILIES:
        url = f"https://fonts.googleapis.com/css2?family={family}:{spec}&display=swap"
        css = subprocess.check_output(["curl", "-s", "-A", UA, url], text=True)
        blocks = re.split(r"/\*\s*([a-z0-9-]+)\s*\*/", css)
        src = None
        for i in range(1, len(blocks) - 1, 2):
            if blocks[i] == "latin":
                src = re.search(r"url\((https://[^)]+\.woff2)\)", blocks[i + 1]).group(1)
                break
        if not src:
            raise SystemExit(f"no latin subset found for {family}")
        subprocess.check_call(["curl", "-s", "-A", UA, src, "-o", str(OUT / name)])
        print("saved", OUT / name)


if __name__ == "__main__":
    main()
