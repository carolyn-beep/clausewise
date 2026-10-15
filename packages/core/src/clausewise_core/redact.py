"""Redaction pre-pass (PLAN.md §8.1, ADR-008).

Replace sensitive spans (amounts, dates, emails, phone numbers, SSNs, and any caller-supplied
party names) with stable placeholders before the text is sent to a model, keeping a map so the
original values can be restored in the final report. This is a deterministic, regex-based pass:
party-name redaction relies on names the caller provides (e.g. from fact extraction or
elicitation); NER/LLM-based name detection is a later, optional enhancement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("AMOUNT", re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")),
    ("PHONE", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")),
    (
        "DATE",
        re.compile(
            r"\b(?:\d{4}-\d{2}-\d{2}"
            r"|\d{1,2}/\d{1,2}/\d{2,4}"
            r"|(?:January|February|March|April|May|June|July|August|September|October|"
            r"November|December)\s+\d{1,2},\s+\d{4})\b"
        ),
    ),
]


@dataclass
class RedactionResult:
    """The redacted text plus a placeholder→original mapping for restoration."""

    text: str
    mapping: dict[str, str] = field(default_factory=dict)


def redact(text: str, party_names: list[str] | None = None) -> RedactionResult:
    """Redact amounts/dates/emails/phones/SSNs (and any ``party_names``) to placeholders.

    Equal originals always map to the same placeholder, so the structure of the document is
    preserved. Use :func:`restore` to put the originals back into the final report text.
    """
    mapping: dict[str, str] = {}
    original_to_placeholder: dict[tuple[str, str], str] = {}
    counters: dict[str, int] = {}

    def placeholder_for(kind: str, original: str) -> str:
        key = (kind, original)
        if key not in original_to_placeholder:
            counters[kind] = counters.get(kind, 0) + 1
            token = f"[{kind}_{counters[kind]}]"
            original_to_placeholder[key] = token
            mapping[token] = original
        return original_to_placeholder[key]

    # Party names first (they may contain words the other patterns ignore), longest first so a
    # full name is redacted before any substring of it.
    for name in sorted(party_names or [], key=len, reverse=True):
        if not name.strip():
            continue
        text = text.replace(name, placeholder_for("PARTY", name))

    for kind, pattern in _PATTERNS:
        text = pattern.sub(lambda m, k=kind: placeholder_for(k, m.group(0)), text)

    return RedactionResult(text=text, mapping=mapping)


def restore(text: str, mapping: dict[str, str]) -> str:
    """Reverse :func:`redact`: replace each placeholder in ``text`` with its original value."""
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text
