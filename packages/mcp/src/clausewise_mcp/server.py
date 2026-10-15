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
from clausewise_core.retrieval import Retriever
from clausewise_corpus.loader import CORPUS_VERSION, load_rules
from clausewise_corpus.loader import lookup_rule as _lookup_rule
from clausewise_corpus.loader import manifest as _manifest
from clausewise_corpus.timing import timing_rules
from fastmcp import FastMCP

mcp: FastMCP = FastMCP("clausewise")


def _rule_summary(card: Any) -> dict[str, Any]:
    """The subset of a rule card worth returning to a client or its LLM."""
    return {
        "id": card.id,
        "jurisdiction": card.jurisdiction,
        "topic": card.topic,
        "citation": card.citation,
        "source_url": card.source_url,
        "effective_from": card.effective_from.isoformat(),
        "last_verified": card.last_verified.isoformat(),
        "confidence": card.confidence.value,
        "plain_summary": card.plain_summary,
        "thresholds": card.thresholds,
        "pending_changes": [pc.model_dump() for pc in card.pending_changes],
    }


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


def build_explain_payload(
    clause_text: str,
    state: str | None = None,
    topic: str | None = None,
    as_of: str | None = None,
) -> dict[str, Any]:
    """Pure implementation behind the ``explain_clause`` tool (kept callable for tests)."""
    as_of_date = date.fromisoformat(as_of) if as_of else date.today()
    jurisdictions = [state, "federal"] if state else None
    cards = Retriever(load_rules()).search(
        clause_text, jurisdictions=jurisdictions, topic=topic, as_of=as_of_date, k=3
    )
    return {
        "corpus_version": CORPUS_VERSION,
        "as_of": as_of_date.isoformat(),
        "relevant_rules": [_rule_summary(card) for card in cards],
        "note": (
            "Legal information, not legal advice. These are the rules most relevant to the "
            "clause; read each rule's plain_summary and primary source."
        ),
        "disclaimer": DISCLAIMER,
    }


@mcp.tool
def explain_clause(
    clause_text: str,
    state: str | None = None,
    topic: str | None = None,
    as_of: str | None = None,
) -> dict[str, Any]:
    """Return the employment-law rules most relevant to a single clause.

    Read-only. Retrieves the best-matching rule cards (federal overlay plus ``state`` if
    given) so the clause can be explained in plain language against a cited, dated source.
    This is legal information, not legal advice.

    Args:
        clause_text: The text of one clause to explain.
        state: Optional two-letter state code (e.g. ``"CA"``) to include that state's rules.
        topic: Optional clause topic to restrict the search (e.g. ``"noncompete"``).
        as_of: Optional ``YYYY-MM-DD``; rules not yet effective then are omitted.
    """
    return build_explain_payload(clause_text, state, topic, as_of)


def build_deadlines_payload(
    state: str | None = None,
    contract_type: str | None = None,
    as_of: str | None = None,
) -> dict[str, Any]:
    """Pure implementation behind the ``check_deadlines`` tool (kept callable for tests)."""
    as_of_date = date.fromisoformat(as_of) if as_of else date.today()
    cards = timing_rules(state, contract_type, as_of_date)
    return {
        "corpus_version": CORPUS_VERSION,
        "as_of": as_of_date.isoformat(),
        "query": {"state": state, "contract_type": contract_type},
        "deadline_rules": [_rule_summary(card) for card in cards],
        "disclaimer": DISCLAIMER,
    }


@mcp.tool
def check_deadlines(
    state: str | None = None,
    contract_type: str | None = None,
    as_of: str | None = None,
) -> dict[str, Any]:
    """Return the time-window rules that may apply (OWBPA 21/45/7, CA final-pay 72h/30d, …).

    Read-only. Surfaces rule cards whose thresholds encode a deadline, for the federal overlay
    plus ``state`` if given, optionally narrowed to a ``contract_type``. Legal information,
    not legal advice; always verify dates against the cited source.

    Args:
        state: Optional two-letter state code (e.g. ``"CA"``).
        contract_type: Optional type (e.g. ``"separation_agreement"``) to focus the result.
        as_of: Optional ``YYYY-MM-DD``; rules not yet effective then are omitted.
    """
    return build_deadlines_payload(state, contract_type, as_of)


def main() -> None:
    """Console-script entry point. Pass ``--http`` for Streamable HTTP, else stdio."""
    if "--http" in sys.argv[1:]:
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
