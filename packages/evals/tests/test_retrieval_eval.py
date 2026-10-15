"""Retrieval eval gate (PLAN.md §15 Phase 1 DoD: recall@5 ≥ 0.9)."""

from clausewise_corpus.loader import load_rules
from clausewise_evals.retrieval.dataset import QUERIES
from clausewise_evals.retrieval.run import evaluate


def test_dataset_is_sizeable():
    assert len(QUERIES) >= 30


def test_every_gold_id_exists_in_corpus():
    corpus_ids = {card.id for card in load_rules()}
    unknown = sorted({q.gold_rule_id for q in QUERIES} - corpus_ids)
    assert not unknown, f"dataset references rule ids not in corpus: {unknown}"


def test_recall_at_5_meets_dod_threshold():
    report = evaluate()
    assert report.recall_at_5 >= 0.9, f"recall@5={report.recall_at_5:.3f}; misses={report.misses}"
