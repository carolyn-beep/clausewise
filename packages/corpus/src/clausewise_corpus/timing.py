"""Deadline / timing lookup over the corpus (backs the MCP ``check_deadlines`` tool).

Deterministic: it surfaces rule cards whose thresholds encode a time window (OWBPA's 21/45/7
days, California's 72-hour / 30-day final-pay rules, the §16600.1 notice deadline), optionally
narrowed to the topics relevant to a contract type. No model involved.
"""

from __future__ import annotations

from datetime import date

from clausewise_core.schemas import RuleCard

from clausewise_corpus.loader import load_rules

# A threshold key counts as a "deadline" if it mentions one of these.
_TIMING_HINTS = ("day", "hour", "deadline", "consider", "revoke", "notice", "penalty")

# Topics whose timing matters for each contract type (others fall back to all timing rules).
_TYPE_TOPICS: dict[str, set[str]] = {
    "separation_agreement": {"release_timing", "final_pay"},
    "employment_agreement": {"final_pay", "noncompete"},
    "offer_letter": {"noncompete", "stay_or_pay"},
    "contractor_agreement": {"misclassification", "final_pay"},
}


def _has_timing_threshold(card: RuleCard) -> bool:
    return any(
        any(hint in key.lower() for hint in _TIMING_HINTS) for key in card.thresholds
    )


def timing_rules(
    state: str | None = None,
    contract_type: str | None = None,
    as_of: date | None = None,
) -> list[RuleCard]:
    """Return effective rule cards carrying a deadline/timing threshold.

    Includes the federal overlay whenever ``state`` is given. If ``contract_type`` maps to
    specific topics, the result is narrowed to those topics (falling back to all timing rules
    when that narrowing would be empty).
    """
    as_of = as_of or date.today()
    states = {state, "federal"} if state else None

    cards = [
        card
        for card in load_rules()
        if (states is None or card.jurisdiction in states)
        and _has_timing_threshold(card)
        and card.is_effective_on(as_of)
    ]

    topics = _TYPE_TOPICS.get(contract_type or "")
    if topics:
        narrowed = [card for card in cards if card.topic in topics]
        if narrowed:
            cards = narrowed

    return sorted(cards, key=lambda card: card.id)
