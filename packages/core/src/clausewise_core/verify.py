"""Deterministic citation verification (PLAN.md §5.2, §8.3; CLAUDE.md non-negotiables).

Every flag a model produces must be grounded: its ``clause_quote`` has to appear in the
contract, and every ``jurisdiction_rule_id`` has to exist in the corpus. Flags that fail
either check are dropped here, before the report is returned, so an injection or hallucination
cannot invent a rule or misquote the document.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field

from clausewise_core.schemas import Flag

_WS = re.compile(r"\s+")


def _normalize(text: str) -> str:
    """Collapse runs of whitespace so quote matching is robust to wrapping/indentation."""
    return _WS.sub(" ", text).strip()


def quote_in_contract(quote: str, contract_text: str) -> bool:
    """True if ``quote`` appears in ``contract_text`` ignoring whitespace differences."""
    needle = _normalize(quote)
    return bool(needle) and needle in _normalize(contract_text)


def flag_failures(flag: Flag, contract_text: str, corpus_rule_ids: set[str]) -> list[str]:
    """Return the reasons ``flag`` fails verification (empty list means it passes)."""
    reasons: list[str] = []
    if not quote_in_contract(flag.clause_quote, contract_text):
        reasons.append("clause_quote does not string-match the contract")
    for rule_id in flag.jurisdiction_rule_ids:
        if rule_id not in corpus_rule_ids:
            reasons.append(f"unknown rule_id: {rule_id}")
    return reasons


@dataclass
class VerificationResult:
    """Flags that passed verification, and the ones dropped with their reasons."""

    kept: list[Flag] = field(default_factory=list)
    dropped: list[tuple[Flag, list[str]]] = field(default_factory=list)


def verify_flags(
    flags: Iterable[Flag],
    contract_text: str,
    corpus_rule_ids: Iterable[str],
) -> VerificationResult:
    """Partition ``flags`` into kept vs. dropped by deterministic verification."""
    rule_ids = set(corpus_rule_ids)
    result = VerificationResult()
    for flag in flags:
        reasons = flag_failures(flag, contract_text, rule_ids)
        if reasons:
            result.dropped.append((flag, reasons))
        else:
            result.kept.append(flag)
    return result
