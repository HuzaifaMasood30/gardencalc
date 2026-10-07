"""LLM client. Gemini free tier via REST (no SDK needed).

If GEMINI_API_KEY is absent or the API fails, falls back to a deterministic
template writer so the pipeline always produces something testable offline.
The fallback still emits real calculator data, so articles remain useful.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from common import strip_fences

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
            "{model}:generateContent?key={key}")


def available() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


def generate(prompt: str, system: str = "", max_tokens: int = 4096,
             temperature: float = 0.6, retries: int = 3) -> str | None:
    """Return model text, or None if unavailable/failed."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    url = ENDPOINT.format(model=MODEL, key=key)
    data = json.dumps(body).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                payload = json.loads(r.read().decode())
            parts = payload["candidates"][0]["content"]["parts"]
            return strip_fences("".join(p.get("text", "") for p in parts))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):
                wait = 2 ** attempt * 5
                print(f"[llm] HTTP {e.code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            print(f"[llm] HTTP {e.code}: {e.read()[:200]!r}")
            return None
        except Exception as e:  # network, parse
            print(f"[llm] error: {e}")
            time.sleep(2 ** attempt)
    return None
