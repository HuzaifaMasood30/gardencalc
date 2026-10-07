"""Markdown rendering for article bodies.

Pipeline: resolve {{url:slug}} placeholders -> escape raw HTML -> render Markdown with
table and list support. Escaping first keeps LLM output from injecting HTML while
leaving Markdown syntax untouched.
"""
from __future__ import annotations

import html
import re

import markdown as md

_EXT = ["tables", "sane_lists", "fenced_code"]


def resolve_placeholders(text: str, slug_to_url: dict[str, str]) -> str:
    return re.sub(r"\{\{url:([a-z0-9-]+)\}\}", lambda m: slug_to_url.get(m.group(1), "#"), text)


def render(markdown_text: str, slug_to_url: dict[str, str] | None = None) -> str:
    if slug_to_url:
        markdown_text = resolve_placeholders(markdown_text, slug_to_url)
    safe = html.escape(markdown_text, quote=False)
    return md.markdown(safe, extensions=_EXT)
