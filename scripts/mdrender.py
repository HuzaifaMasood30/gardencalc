"""Markdown rendering for article bodies.

Pipeline: resolve {{url:slug}} placeholders -> escape raw HTML -> render Markdown with
table and list support -> add stable ids to h2 headings and collect a table of contents.
Escaping first keeps LLM output from injecting HTML while leaving Markdown syntax intact.
"""
from __future__ import annotations

import html
import re

import markdown as md

_EXT = ["tables", "sane_lists", "fenced_code"]


def resolve_placeholders(text: str, slug_to_url: dict[str, str]) -> str:
    return re.sub(r"\{\{url:([a-z0-9-]+)\}\}", lambda m: slug_to_url.get(m.group(1), "#"), text)


def _slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def add_heading_ids(body_html: str) -> tuple[str, list[dict]]:
    """Give each <h2> an id and return a TOC of [{id, text}]."""
    toc: list[dict] = []
    used: dict[str, int] = {}

    def repl(match: re.Match) -> str:
        inner = match.group(1)
        base = _slugify(inner)
        n = used.get(base, 0)
        used[base] = n + 1
        hid = base if n == 0 else f"{base}-{n}"
        toc.append({"id": hid, "text": re.sub(r"<[^>]+>", "", inner).strip()})
        return f'<h2 id="{hid}">{inner}</h2>'

    out = re.sub(r"<h2>(.*?)</h2>", repl, body_html, flags=re.S)
    return out, toc


def render_with_toc(markdown_text: str, slug_to_url: dict[str, str] | None = None):
    """Return (html, toc). Prefer this over render() for article bodies."""
    if slug_to_url:
        markdown_text = resolve_placeholders(markdown_text, slug_to_url)
    safe = html.escape(markdown_text, quote=False)
    body = md.markdown(safe, extensions=_EXT)
    return add_heading_ids(body)


def render(markdown_text: str, slug_to_url: dict[str, str] | None = None) -> str:
    if slug_to_url:
        markdown_text = resolve_placeholders(markdown_text, slug_to_url)
    safe = html.escape(markdown_text, quote=False)
    return md.markdown(safe, extensions=_EXT)
