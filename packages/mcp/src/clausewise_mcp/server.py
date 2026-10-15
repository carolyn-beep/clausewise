"""The ClauseWise FastMCP server (PLAN.md §5.3).

Phase 0 exposes one read-only tool, ``lookup_rule``, backed by the versioned corpus, plus the
``clausewise://corpus/manifest`` resource. Every tool here is read-only and has no
side effects: nothing sends email, writes files, or forwards contract text anywhere.

Run it:
    uv run clausewise-mcp          # stdio (Claude Desktop / Claude Code / Cursor)
    uv run clausewise-mcp --http   # Streamable HTTP on 127.0.0.1:8000 (ChatGPT, remote)
"""

from __future__ import annotations

import sys
from datetime import date
from typing import Any

from clausewise_core.disclaimer import DISCLAIMER
from clausewise_corpus.loader import CORPUS_VERSION
from clausewise_corpus.loader import lookup_rule as _lookup_rule
from clausewise_corpus.loader import manifest as _manifest
from fastmcp import FastMCP

mcp: FastMCP = FastMCP("clausewise")


def build_lookup_payload(state: str, topic: str, as_of: str | None = None) -> dict[str, Any]:
    """Pure implementation behind the ``lookup_rule`` tool (kept callable for tests)."""
    as_of_date = date.fromisoformat(as_of) if as_of else date.today()
    cards = _lookup_rule(state, topic, as_of_date)
    return {
        "corpus_version": CORPUS_VERSION,
        "as_of": as_of_date.isoformat(),
        "query": {"state": state, "topic": topic},
        "rules": [card.model_dump(mode="json") for card in cards],
        "disclaimer": DISCLAIMER,
    }


@mcp.tool
def lookup_rule(state: str, topic: str, as_of: str | None = None) -> dict[str, Any]:
    """Look up the employment-law rule card(s) for a state and topic.

    Read-only. Returns the matching rule cards with citations, effective dates and a
    plain-language summary, plus the corpus version, the "as of" date and the ClauseWise
    disclaimer. This is legal information, not legal advice.

    Args:
        state: ``"federal"`` or a two-letter state code (e.g. ``"CA"``, ``"MA"``).
        topic: A clause topic such as ``"release_timing"``, ``"noncompete"`` or
            ``"confidentiality_whistleblower"``.
        as_of: Optional ``YYYY-MM-DD`` date; rules not yet effective on that date are omitted.
            Defaults to today.
    """
    return build_lookup_payload(state, topic, as_of)


@mcp.resource("clausewise://corpus/manifest")
def corpus_manifest() -> dict[str, Any]:
    """Corpus version, rule count, snapshot hash and the jurisdictions covered."""
    return _manifest()


def main() -> None:
    """Console-script entry point. Pass ``--http`` for Streamable HTTP, else stdio."""
    if "--http" in sys.argv[1:]:
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
