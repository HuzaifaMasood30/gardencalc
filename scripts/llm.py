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

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
# Tried in order; the first that answers is used. Model names are retired and
# rate-limited over time, so a single hard-coded name breaks the pipeline.
MODEL_CHAIN = [MODEL, "gemini-3.6-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]
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
    seen: set[str] = set()
    for model in MODEL_CHAIN:
        if model in seen:
            continue
        seen.add(model)
        text = _call(model, key, body, retries)
        if text:
            if model != MODEL:
                print(f"[llm] used fallback model {model}")
            return text
    return None


def _call(model: str, key: str, body: dict, retries: int) -> str | None:
    url = ENDPOINT.format(model=model, key=key)
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
            if e.code in (429, 500, 502, 503, 504):
                wait = 2 ** attempt * 5
                print(f"[llm] {model} HTTP {e.code}, retrying in {wait}s")
                time.sleep(wait)
                continue
            print(f"[llm] {model} HTTP {e.code}: {e.read()[:200]!r}")
            return None
        except Exception as e:  # network, parse
            print(f"[llm] {model} error: {e}")
            time.sleep(2 ** attempt)
    return None
