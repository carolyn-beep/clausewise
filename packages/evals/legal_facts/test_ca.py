"""Legal-fact suite: California rules (PLAN.md §10.2, §15.1 Phase 1).

Deterministic assertions against ``lookup_rule``. Summary-level facts from plan research;
verbatim statute text and exact effective dates are tracked for primary-source verification.
"""

from datetime import date

from clausewise_corpus.loader import lookup_rule


def _one(state: str, topic: str, rule_id: str, as_of: date | None = None):
    cards = lookup_rule(state, topic, as_of)
    match = [c for c in cards if c.id == rule_id]
    assert match, f"{rule_id} not found for ({state}, {topic})"
    return match[0]


# --- Non-compete: §16600 void + §16600.1 notice --------------------------------------------


def test_ca_noncompetes_are_void():
    card = _one("CA", "noncompete", "ca.noncompete.16600")
    assert "void" in card.plain_summary.lower()


def test_ca_noncompete_topic_returns_both_void_rule_and_notice_rule():
    ids = {c.id for c in lookup_rule("CA", "noncompete")}
    assert {"ca.noncompete.16600", "ca.noncompete.16600_1"} <= ids


def test_ca_noncompete_void_notice_deadline():
    card = _one("CA", "noncompete", "ca.noncompete.16600_1")
    assert card.thresholds["notice_deadline"] == "2024-02-14"


# --- Choice of law: §16600.5 and §925 ------------------------------------------------------


def test_ca_choice_of_law_returns_both_cards():
    ids = {c.id for c in lookup_rule("CA", "choice_of_law")}
    assert {"ca.choice_of_law.16600_5", "ca.choice_of_law.925"} <= ids


def test_ca_16600_5_applies_regardless_of_where_signed():
    card = _one("CA", "choice_of_law", "ca.choice_of_law.16600_5")
    assert "regardless of where" in card.plain_summary.lower()


def test_ca_925_exception_is_individual_counsel():
    card = _one("CA", "choice_of_law", "ca.choice_of_law.925")
    assert "individually represented" in card.plain_summary.lower()
    assert card.effective_from == date(2017, 1, 1)


# --- Stay-or-pay: AB 692, on/after 2026-01-01 (temporal gating) -----------------------------


def test_ca_stay_or_pay_not_effective_before_2026():
    assert lookup_rule("CA", "stay_or_pay", as_of=date(2025, 12, 31)) == []


def test_ca_stay_or_pay_effective_from_2026_01_01():
    card = _one("CA", "stay_or_pay", "ca.stay_or_pay.ab692", as_of=date(2026, 1, 1))
    assert card.thresholds["applies_to_contracts_on_or_after"] == "2026-01-01"
    assert card.thresholds["private_right_floor_usd"] == 5000


# --- Invention assignment: §2870 own-time carve-out ----------------------------------------


def test_ca_invention_assignment_own_time_carveout():
    card = _one("CA", "invention_assignment", "ca.invention_assignment.2870")
    assert "own time" in card.plain_summary.lower()
    assert "written notice" in card.plain_summary.lower()


# --- Final pay: §§201-203 -------------------------------------------------------------------


def test_ca_final_pay_timing_and_penalty():
    card = _one("CA", "final_pay", "ca.final_pay.201")
    assert card.thresholds["quit_without_notice_hours"] == 72
    assert card.thresholds["waiting_time_penalty_max_days"] == 30


# --- Misclassification: §2775 ABC test -----------------------------------------------------


def test_ca_misclassification_uses_abc_test():
    card = _one("CA", "misclassification", "ca.misclassification.2775")
    assert card.thresholds["abc_prongs"] == 3
    assert "abc" in card.plain_summary.lower()


# --- Corpus hygiene for CA ------------------------------------------------------------------


def test_every_ca_card_has_allowlisted_official_source():
    ca_cards = [c for c in lookup_rule_all() if c.jurisdiction == "CA"]
    assert len(ca_cards) >= 8
    for card in ca_cards:
        assert "ca.gov" in card.source_url
        assert card.effective_from is not None
        assert card.last_verified == date(2026, 10, 15)


def lookup_rule_all():
    # Helper: pull every card regardless of topic by loading the corpus directly.
    from clausewise_corpus.loader import load_rules

    return load_rules()


# --- Additional grounded CA facts ----------------------------------------------------------


def test_ca_16600_has_narrow_exceptions():
    card = _one("CA", "noncompete", "ca.noncompete.16600")
    assert "narrow statutory exceptions" in card.plain_summary


def test_ca_16600_strengthened_by_sb699_in_2024():
    summary = _one("CA", "noncompete", "ca.noncompete.16600").plain_summary
    assert "SB 699" in summary
    assert "January 1, 2024" in summary


def test_ca_void_notice_covers_former_employees():
    assert "former employees" in _one("CA", "noncompete", "ca.noncompete.16600_1").plain_summary


def test_ca_16600_5_creates_private_right_of_action():
    assert "private right of action" in _one(
        "CA", "choice_of_law", "ca.choice_of_law.16600_5"
    ).plain_summary


def test_ca_16600_5_covers_contracts_signed_out_of_state():
    assert "worked outside California" in _one(
        "CA", "choice_of_law", "ca.choice_of_law.16600_5"
    ).plain_summary


def test_ca_925_allows_recovery_of_attorney_fees():
    assert "attorney's fees" in _one("CA", "choice_of_law", "ca.choice_of_law.925").plain_summary


def test_ca_ab692_has_tuition_exception():
    card = _one("CA", "stay_or_pay", "ca.stay_or_pay.ab692", as_of=date(2026, 6, 1))
    assert "tuition" in card.plain_summary


def test_ca_ab692_creates_private_right_of_action():
    card = _one("CA", "stay_or_pay", "ca.stay_or_pay.ab692", as_of=date(2026, 6, 1))
    assert "private right of action" in card.plain_summary


def test_ca_2870_carveout_relates_to_business_or_results_from_work():
    summary = _one("CA", "invention_assignment", "ca.invention_assignment.2870").plain_summary
    assert "relates to the employer's business" in summary
    assert "results from work" in summary


def test_ca_2870_requires_written_notice():
    assert "written notice" in _one(
        "CA", "invention_assignment", "ca.invention_assignment.2870"
    ).plain_summary


def test_ca_final_pay_due_immediately_on_discharge():
    summary = _one("CA", "final_pay", "ca.final_pay.201").plain_summary
    assert "immediately at the time of termination" in summary


def test_ca_misclassification_citation_mentions_ab5():
    assert "AB 5" in _one("CA", "misclassification", "ca.misclassification.2775").citation


def test_ca_misclassification_presumes_employee_status():
    summary = _one("CA", "misclassification", "ca.misclassification.2775").plain_summary
    assert "presumes a worker is an employee" in summary


def test_every_ca_card_has_a_substantive_plain_summary():
    for card in [c for c in lookup_rule_all() if c.jurisdiction == "CA"]:
        assert len(card.plain_summary.strip()) > 80
        assert card.confidence in {"high", "medium"}

