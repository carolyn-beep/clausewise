"""Single-relevant-document retrieval metrics (PLAN.md §10.2).

Each query has exactly one gold rule card, so these reduce to the familiar hit/rank forms:
recall@k is a hit indicator, MRR uses the reciprocal of the gold's rank, and nDCG@k has an
ideal DCG of 1 (gold at rank 1).
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def recall_at_k(ranked_ids: Sequence[str], gold_id: str, k: int) -> float:
    """1.0 if the gold id is within the top ``k`` results, else 0.0."""
    return 1.0 if gold_id in ranked_ids[:k] else 0.0


def reciprocal_rank(ranked_ids: Sequence[str], gold_id: str) -> float:
    """1 / rank of the gold id (0.0 if it is absent)."""
    for position, rule_id in enumerate(ranked_ids, start=1):
        if rule_id == gold_id:
            return 1.0 / position
    return 0.0


def ndcg_at_k(ranked_ids: Sequence[str], gold_id: str, k: int) -> float:
    """nDCG@k for a single relevant document (ideal DCG is 1.0)."""
    for position, rule_id in enumerate(ranked_ids[:k], start=1):
        if rule_id == gold_id:
            return 1.0 / math.log2(position + 1)
    return 0.0
