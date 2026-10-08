"""Submit the published URLs to IndexNow.

IndexNow is a shared notification protocol: it tells participating search
engines (Bing, Yandex, Seznam, Naver) that URLs changed, so they can recrawl
without waiting for the next organic crawl. Google does not participate; it is
handled by Search Console.

Key verification: api.indexnow.org fetches https://<host>/<key>.txt and expects
the file body to equal the key. On GitHub *project* pages the host root
(https://<user>.github.io/<key>.txt) is not ours to serve, so that endpoint
always answers 403 UserForbiddedToAccessSite. Bing's own endpoint
(https://www.bing.com/indexnow) verifies the key against the submitted URL's
directory instead and works for project pages, so that is the primary path.
Bing feeds DuckDuckGo and Copilot/ChatGPT-style search, so it is the one that
matters. This script is a no-op unless indexnow_key is configured.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from common import SITE, site_config

ENDPOINT = "https://api.indexnow.org/indexnow"
BING_ENDPOINT = "https://www.bing.com/indexnow"


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

    ok = _via_bing(base, key, payload["urlList"])
    if not ok:
        # Fall back to the shared endpoint for hosts that can serve the key at root.
        ok = _post(ENDPOINT, payload)
    return ok


def _via_bing(base: str, key: str, url_list: list[str]) -> bool:
    """Bing's endpoint accepts GET with one url per request.

    It verifies the key against the URL's own directory, which works for GitHub
    project pages where the key file cannot sit at the host root.
    """
    ok = 0
    for url in url_list:
        query = urllib.parse.urlencode({"url": url, "key": key})
        try:
            with urllib.request.urlopen(f"{BING_ENDPOINT}?{query}", timeout=30) as resp:
                if 200 <= resp.status < 300:
                    ok += 1
        except Exception:  # noqa: BLE001 - never fail the pipeline on a ping
            pass
        # Bing's GET endpoint throttles bursts, so pace the submissions. Whatever
        # is missed one run is re-notified on the next.
        time.sleep(0.7)
    print(f"[indexnow] bing accepted {ok}/{len(url_list)} URLs")
    return ok > 0


def _post(endpoint: str, payload: dict) -> bool:
    req = urllib.request.Request(
        endpoint,
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
