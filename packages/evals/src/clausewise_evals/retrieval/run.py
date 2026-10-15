"""Run the retrieval eval and print a metrics table (PLAN.md §10.2, §10.3).

Usage:
    uv run clausewise-retrieval-eval
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from statistics import mean

from clausewise_core.retrieval import Retriever
from clausewise_corpus.loader import load_rules

from clausewise_evals.retrieval import metrics
from clausewise_evals.retrieval.dataset import QUERIES, RetrievalQuery

_RANK_DEPTH = 10  # retrieve this many to score MRR / nDCG@10


@dataclass
class RetrievalReport:
    n: int
    recall_at_1: float
    recall_at_3: float
    recall_at_5: float
    mrr: float
    ndcg_at_10: float
    misses: list[tuple[str, str]] = field(default_factory=list)  # (question, gold) not in top-5


def evaluate(queries: Sequence[RetrievalQuery] = QUERIES) -> RetrievalReport:
    """Score the BM25 retriever over ``queries`` against the current corpus."""
    retriever = Retriever(load_rules())
    r1, r3, r5, rr, ndcg = [], [], [], [], []
    misses: list[tuple[str, str]] = []

    for query in queries:
        cards = retriever.search(
            query.question,
            jurisdictions=list(query.jurisdictions),
            as_of=query.as_of,
            k=_RANK_DEPTH,
        )
        ranked = [card.id for card in cards]
        gold = query.gold_rule_id
        r1.append(metrics.recall_at_k(ranked, gold, 1))
        r3.append(metrics.recall_at_k(ranked, gold, 3))
        r5.append(metrics.recall_at_k(ranked, gold, 5))
        rr.append(metrics.reciprocal_rank(ranked, gold))
        ndcg.append(metrics.ndcg_at_k(ranked, gold, 10))
        if not metrics.recall_at_k(ranked, gold, 5):
            misses.append((query.question, gold))

    return RetrievalReport(
        n=len(queries),
        recall_at_1=mean(r1),
        recall_at_3=mean(r3),
        recall_at_5=mean(r5),
        mrr=mean(rr),
        ndcg_at_10=mean(ndcg),
        misses=misses,
    )


def format_report(report: RetrievalReport) -> str:
    lines = [
        "Retrieval eval (BM25 baseline)",
        f"  queries      {report.n}",
        f"  recall@1     {report.recall_at_1:.3f}",
        f"  recall@3     {report.recall_at_3:.3f}",
        f"  recall@5     {report.recall_at_5:.3f}",
        f"  MRR          {report.mrr:.3f}",
        f"  nDCG@10      {report.ndcg_at_10:.3f}",
    ]
    if report.misses:
        lines.append(f"  misses (not in top-5): {len(report.misses)}")
        for question, gold in report.misses:
            lines.append(f"    - {gold}: {question}")
    return "\n".join(lines)


def main() -> None:
    print(format_report(evaluate()))


if __name__ == "__main__":
    main()
