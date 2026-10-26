"""Aggregated curated article definitions.

The article prose is split across ``curated_a``, ``curated_b`` and ``curated_c`` so no
single file is unwieldy. ``_body`` lives here and is imported by those modules, which is
why the imports sit below its definition.
"""
from __future__ import annotations

TODAY = "2026-10-26"


def _body(lead: str, worked_lead: str, bullets: str, sections: list[tuple[str, str]]) -> str:
    """Assemble a body: answer-first lead, a worked example, then H2 sections."""
    parts = [lead.strip(), "", "## Worked Example", "", worked_lead.strip(), "", bullets.strip()]
    for heading, text in sections:
        parts += ["", f"## {heading}", "", text.strip()]
    return "\n".join(parts) + "\n"


from curated_a import ARTICLES as _A  # noqa: E402
from curated_b import ARTICLES as _B  # noqa: E402
from curated_c import ARTICLES as _C  # noqa: E402
from curated_d import ARTICLES as _D  # noqa: E402
from curated_e import ARTICLES as _E  # noqa: E402
from curated_f import ARTICLES as _F  # noqa: E402

ARTICLES = _A + _B + _C + _D + _E + _F
