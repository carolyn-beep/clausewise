"""Lexical retrieval over the rule-card corpus (PLAN.md §8.2).

A BM25 baseline with the metadata pre-filter the plan specifies: candidates are first narrowed
by jurisdiction, (optional) topic and temporal validity, then ranked by BM25. Dense vectors,
reranking and reciprocal-rank fusion are the key-dependent Phase 1 follow-up; BM25 already
handles statute numbers and terms of art ("§16600", "garden leave") that need exact match.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from datetime import date

from rank_bm25 import BM25Okapi

from clausewise_core.schemas import RuleCard

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase word/number tokenizer (keeps statute numbers like ``16600``)."""
    return _TOKEN_RE.findall(text.lower())


def _card_document(card: RuleCard) -> str:
    parts = [card.topic, card.citation, card.plain_summary]
    parts.extend(chunk.text for chunk in card.statute_chunks)
    return " ".join(parts)


class Retriever:
    """BM25 retrieval over rule cards with a jurisdiction/topic/temporal pre-filter."""

    def __init__(self, cards: Iterable[RuleCard]) -> None:
        self.cards: list[RuleCard] = list(cards)

    def search(
        self,
        query: str,
        jurisdictions: Sequence[str] | None = None,
        topic: str | None = None,
        as_of: date | None = None,
        k: int = 5,
    ) -> list[RuleCard]:
        """Return up to ``k`` rule cards best matching ``query`` within the filtered set."""
        candidates = self._prefilter(jurisdictions, topic, as_of)
        if not candidates:
            return []
        tokens = tokenize(query)
        if not tokens:
            return candidates[:k]
        bm25 = BM25Okapi([tokenize(_card_document(c)) for c in candidates])
        scores = bm25.get_scores(tokens)
        ranked = sorted(
            zip(candidates, scores, strict=True), key=lambda pair: pair[1], reverse=True
        )
        return [card for card, _ in ranked[:k]]

    def _prefilter(
        self,
        jurisdictions: Sequence[str] | None,
        topic: str | None,
        as_of: date | None,
    ) -> list[RuleCard]:
        allowed = set(jurisdictions) if jurisdictions is not None else None
        out: list[RuleCard] = []
        for card in self.cards:
            if allowed is not None and card.jurisdiction not in allowed:
                continue
            if topic is not None and card.topic != topic:
                continue
            if as_of is not None and not card.is_effective_on(as_of):
                continue
            out.append(card)
        return out
