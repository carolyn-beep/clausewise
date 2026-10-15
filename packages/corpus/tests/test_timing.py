"""Tests for the deadline/timing lookup."""

from datetime import date

from clausewise_corpus.timing import timing_rules


def test_federal_owbpa_is_a_timing_rule():
    ids = {c.id for c in timing_rules()}
    assert "federal.owbpa.626f" in ids


def test_ab692_is_not_a_timing_rule():
    # AB 692 encodes an effective-date and a dollar floor, not a deadline window.
    ids = {c.id for c in timing_rules("CA", as_of=date(2026, 6, 1))}
    assert "ca.stay_or_pay.ab692" not in ids


def test_state_query_includes_federal_overlay():
    ids = {c.id for c in timing_rules("CA")}
    assert "federal.owbpa.626f" in ids  # federal overlay
    assert "ca.final_pay.201" in ids  # CA final-pay timing


def test_contract_type_narrows_topics():
    ids = {c.id for c in timing_rules("CA", contract_type="separation_agreement")}
    # separation -> release_timing + final_pay; the §16600.1 notice (noncompete) drops out.
    assert "federal.owbpa.626f" in ids
    assert "ca.final_pay.201" in ids
    assert "ca.noncompete.16600_1" not in ids
