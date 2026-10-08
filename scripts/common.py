"""Shared helpers: paths, config loading, JSON IO, slugify."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DATA = ROOT / "data"
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
SITE = ROOT / "site"
REPORTS = ROOT / "reports"


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def site_config() -> dict:
    """Site config with environment overrides.

    CI sets these from the repository context so the deployed site never contains a
    placeholder URL or a fake contact address.
    """
    import os
    cfg = load_json(CONFIG / "site.json")
    env_map = {
        "SITE_BASE_URL": "base_url",
        "SITE_CUSTOM_DOMAIN": "custom_domain",
        "SITE_CONTACT_EMAIL": "contact_email",
        "ADSENSE_CLIENT": "adsense_client",
        "ANALYTICS_ID": "analytics_id",
        "GOOGLE_SITE_VERIFICATION": "google_site_verification",
        "BING_SITE_VERIFICATION": "bing_site_verification",
    }
    for env_key, cfg_key in env_map.items():
        val = os.environ.get(env_key, "").strip()
        if val:
            cfg[cfg_key] = val
    # GitHub Pages serves only lower-case hostnames, so canonical/og URLs must use a
    # lower-case host or they point at a URL the platform does not answer on.
    base = str(cfg.get("base_url", ""))
    if "://" in base:
        scheme, rest = base.split("://", 1)
        host = rest.split("/", 1)[0].lower()
        cfg["base_url"] = scheme + "://" + host + rest[len(host):]
    return cfg


def seo_config() -> dict:
    return load_json(CONFIG / "seo.json")


def topics_config() -> dict:
    return load_json(CONFIG / "topics.json")


def articles() -> list[dict]:
    return load_json(DATA / "articles.json", default=[])


def save_articles(items: list[dict]) -> None:
    save_json(DATA / "articles.json", items)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"['\u2019]", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")


def strip_fences(text: str) -> str:
    """Remove ```lang ... ``` fences an LLM may wrap output in."""
    text = text.strip()
    m = re.match(r"^```[a-zA-Z]*\n(.*)\n```$", text, re.S)
    return m.group(1).strip() if m else text


def word_count(html_or_text: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html_or_text)
    return len(re.findall(r"\b[\w'-]+\b", text))


def human_date(value: str) -> str:
    """Format an ISO date as "Oct 8, 2026" for display.

    Returns the input unchanged when it is missing or not a real ISO date, so a bad
    value degrades to the raw string instead of raising during the build.
    """
    import datetime as _dt
    if not value:
        return ""
    try:
        return _dt.date.fromisoformat(str(value)[:10]).strftime("%b %-d, %Y")
    except ValueError:
        try:
            # %-d is POSIX-only; fall back to a portable strip for other platforms.
            return _dt.date.fromisoformat(str(value)[:10]).strftime("%b %d, %Y").replace(" 0", " ")
        except ValueError:
            return str(value)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse a leading --- YAML-ish block into a flat dict (stdlib only)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    meta: dict = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [v.strip().strip('"') for v in val[1:-1].split(",") if v.strip()]
        else:
            meta[key] = val.strip('"')
    return meta, body
