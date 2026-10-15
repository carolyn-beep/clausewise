"""Tests for BM25 retrieval with the metadata pre-filter."""

from datetime import date

from clausewise_core.retrieval import Retriever, tokenize
from clausewise_core.schemas import RuleCard


def _card(rule_id, jurisdiction, topic, summary, effective_from=date(2000, 1, 1)) -> RuleCard:
    return RuleCard(
        id=rule_id,
        jurisdiction=jurisdiction,
        topic=topic,
        citation=rule_id,
        source_url="https://leginfo.legislature.ca.gov/x",
        effective_from=effective_from,
        last_verified=date(2026, 10, 15),
        verified_by="test",
        plain_summary=summary,
    )


CARDS = [
    _card(
        "ca.noncompete.16600", "CA", "noncompete",
        "California noncompete clauses are void under section 16600.",
    ),
    _card(
        "ca.final_pay.201", "CA", "final_pay",
        "Final wages are due immediately on discharge in California.",
    ),
    _card(
        "federal.owbpa.626f", "federal", "release_timing",
        "OWBPA sets 21/45/7-day release windows.",
    ),
    _card(
        "ca.stay_or_pay.ab692", "CA", "stay_or_pay",
        "Stay-or-pay repayment clauses banned.", date(2026, 1, 1),
    ),
]


def test_tokenize_keeps_statute_numbers():
    assert "16600" in tokenize("Section §16600 is relevant")


def test_search_ranks_most_relevant_first():
    top = Retriever(CARDS).search("noncompete void 16600", jurisdictions=["CA", "federal"], k=1)
    assert top[0].id == "ca.noncompete.16600"


def test_topic_prefilter_limits_candidates():
    results = Retriever(CARDS).search("wages", topic="final_pay")
    assert [c.id for c in results] == ["ca.final_pay.201"]


def test_jurisdiction_prefilter_excludes_others():
    results = Retriever(CARDS).search("release windows", jurisdictions=["CA"])
    assert all(c.jurisdiction == "CA" for c in results)
    assert "federal.owbpa.626f" not in {c.id for c in results}


def test_temporal_prefilter_drops_not_yet_effective():
    before = Retriever(CARDS).search("stay or pay", as_of=date(2025, 12, 31))
    after = Retriever(CARDS).search("stay or pay", as_of=date(2026, 6, 1))
    assert "ca.stay_or_pay.ab692" not in {c.id for c in before}
    assert "ca.stay_or_pay.ab692" in {c.id for c in after}
