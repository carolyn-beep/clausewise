"""Round-trip and validation tests for the core schemas (Phase 0 definition of done)."""

from datetime import date

import pytest
from clausewise_core import DISCLAIMER
from clausewise_core.enums import Confidence, ContractType, IssueType, Severity
from clausewise_core.schemas import Facts, Flag, FlagReport, PendingChange, RuleCard
from pydantic import ValidationError


def _owbpa_card() -> RuleCard:
    return RuleCard(
        id="federal.owbpa.626f",
        jurisdiction="federal",
        topic="release_timing",
        citation="29 U.S.C. §626(f) (OWBPA)",
        source_url="https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title29-section626",
        effective_from=date(1990, 10, 16),
        last_verified=date(2026, 10, 15),
        verified_by="self-review",
        confidence=Confidence.high,
        plain_summary="OWBPA sets the 21/45/7-day windows for a valid age-claim waiver.",
        thresholds={"consider_days": 21, "consider_days_group": 45, "revoke_days": 7},
    )


def test_rulecard_round_trips_through_json():
    card = _owbpa_card()
    restored = RuleCard.model_validate_json(card.model_dump_json())
    assert restored == card


def test_rulecard_rejects_off_allowlist_source_url():
    with pytest.raises(ValidationError):
        RuleCard(
            id="x.y.z",
            jurisdiction="federal",
            topic="noncompete",
            citation="Example",
            source_url="https://example.com/not-official",
            effective_from=date(2020, 1, 1),
            last_verified=date(2026, 10, 15),
            verified_by="self-review",
            plain_summary="should not validate",
        )


def test_rulecard_temporal_validity():
    card = _owbpa_card()
    assert card.is_effective_on(date(2026, 10, 15))
    assert not card.is_effective_on(date(1989, 1, 1))


def test_pending_change_is_not_treated_as_current():
    card = _owbpa_card()
    card = card.model_copy(
        update={
            "pending_changes": [
                PendingChange(bill="H.R. 0000", status="introduced", would_change="nothing yet")
            ]
        }
    )
    # A pending change never affects whether the rule is currently effective.
    assert card.is_effective_on(date(2026, 10, 15))


def test_flagreport_round_trips_through_json():
    report = FlagReport(
        corpus_version="2026.10.0",
        as_of=date(2026, 10, 15),
        contract_type=ContractType.separation_agreement,
        jurisdictions=["federal"],
        facts=Facts(work_state="MA", governing_law_state="DE", annual_pay=92000),
        flags=[
            Flag(
                clause_id="c7",
                clause_quote="You have 14 days to sign this release.",
                issue_type=IssueType.release_timing,
                severity=Severity.high,
                jurisdiction_rule_ids=["federal.owbpa.626f"],
                explanation_plain="A valid age-claim waiver usually needs at least 21 days.",
                questions_to_ask=["Am I being asked to waive age-discrimination claims?"],
                when_to_get_a_lawyer="If you are 40+ and the window is under 21 days.",
            )
        ],
        disclaimer=DISCLAIMER,
    )
    restored = FlagReport.model_validate_json(report.model_dump_json())
    assert restored == report


def test_flagreport_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        FlagReport.model_validate(
            {
                "corpus_version": "2026.10.0",
                "as_of": "2026-10-15",
                "contract_type": "nda",
                "disclaimer": DISCLAIMER,
                "surprise": "extra field should be forbidden",
            }
        )
