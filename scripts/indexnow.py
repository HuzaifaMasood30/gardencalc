"""Submit the published URLs to IndexNow.

IndexNow is a shared notification protocol: one POST tells participating search
engines (Bing, Yandex, Seznam, Naver) that URLs changed, so they can recrawl
without waiting for the next organic crawl. Google does not participate; it is
handled by Search Console.

Key verification: the endpoint fetches https://<host>/<key>.txt and expects the
file body to equal the key, so the key file is emitted at the site root by
build.py. This script is a no-op unless indexnow_key is configured.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from common import SITE, site_config

ENDPOINT = "https://api.indexnow.org/indexnow"


def urls() -> list[str]:
    sitemap = SITE / "sitemap.xml"
    if not sitemap.exists():
        return []
    import re

    return re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text(encoding="utf-8"))


def run() -> bool:
    cfg = site_config()
    key = str(cfg.get("indexnow_key", "")).strip()
    base = str(cfg.get("base_url", "")).rstrip("/")
    if not key or not base.startswith(("http://", "https://")):
        print("[indexnow] skipped (no key or no absolute base_url)")
        return False

    host = base.split("://", 1)[1].split("/", 1)[0]
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{base}/{key}.txt",
        "urlList": urls(),
    }
    if not payload["urlList"]:
        print("[indexnow] skipped (no URLs)")
        return False

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"[indexnow] submitted {len(payload['urlList'])} URLs -> HTTP {resp.status}")
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as exc:
        # 422 means the key file is not reachable yet (first deploy); not fatal.
        print(f"[indexnow] HTTP {exc.code}: {exc.read()[:200]!r}")
        return False
    except Exception as exc:  # noqa: BLE001 - never fail the pipeline on a ping
        print(f"[indexnow] error: {exc}")
        return False


if __name__ == "__main__":
    run()
