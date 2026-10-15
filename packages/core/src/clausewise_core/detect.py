"""Contract-type detection (PLAN.md §8.1).

A deterministic keyword heuristic that needs no model. A single Haiku call is the richer
option for ambiguous documents (key-dependent); this baseline covers the common cases and is
the fallback when no model is available.
"""

from __future__ import annotations

from clausewise_core.enums import ContractType

# Ordered most-specific first: on a tie, the earlier entry wins.
_SIGNALS: list[tuple[ContractType, tuple[str, ...]]] = [
    (
        ContractType.separation_agreement,
        ("severance", "separation agreement", "release of claims", "general release"),
    ),
    (
        ContractType.offer_letter,
        ("offer letter", "pleased to offer", "start date", "this offer"),
    ),
    (
        ContractType.piia,
        ("invention assignment", "proprietary information", "assignment of inventions", "piia"),
    ),
    (
        ContractType.nda,
        (
            "non-disclosure",
            "nondisclosure",
            "confidentiality agreement",
            "confidential information",
        ),
    ),
    (
        ContractType.sow,
        ("statement of work", "scope of work", "deliverables"),
    ),
    (
        ContractType.contractor_agreement,
        ("independent contractor", "contractor agrees", "services agreement"),
    ),
    (
        ContractType.employment_agreement,
        ("employment agreement", "employee agrees", "at-will", "duties and responsibilities"),
    ),
]


def detect_contract_type(text: str) -> ContractType:
    """Return the best-guess :class:`ContractType` for ``text`` (``unknown`` if no signal)."""
    lowered = text.lower()
    best_type = ContractType.unknown
    best_score = 0
    for contract_type, keywords in _SIGNALS:
        score = sum(1 for kw in keywords if kw in lowered)
        if score > best_score:
            best_type, best_score = contract_type, score
    return best_type
