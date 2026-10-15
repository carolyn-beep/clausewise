"""Tests for deterministic citation verification."""

from clausewise_core.enums import IssueType, Severity
from clausewise_core.schemas import Flag
from clausewise_core.verify import quote_in_contract, verify_flags

CONTRACT = "The Employee has 21 days to consider this Agreement and 7 days to revoke it."
RULE_IDS = {"federal.owbpa.626f", "ca.noncompete.16600"}


def _flag(quote: str, rule_ids: list[str]) -> Flag:
    return Flag(
        clause_id="c1",
        clause_quote=quote,
        issue_type=IssueType.release_timing,
        severity=Severity.high,
        jurisdiction_rule_ids=rule_ids,
        explanation_plain="…",
        when_to_get_a_lawyer="…",
    )


def test_quote_match_ignores_whitespace():
    assert quote_in_contract("21 days   to consider", "...21 days\nto consider...")
    assert not quote_in_contract("90 days to consider", CONTRACT)


def test_keeps_grounded_flag():
    result = verify_flags(
        [_flag("21 days to consider", ["federal.owbpa.626f"])], CONTRACT, RULE_IDS
    )
    assert len(result.kept) == 1
    assert not result.dropped


def test_drops_flag_with_unquotable_text():
    result = verify_flags(
        [_flag("a quote not in the document", ["federal.owbpa.626f"])], CONTRACT, RULE_IDS
    )
    assert not result.kept
    assert result.dropped[0][1] == ["clause_quote does not string-match the contract"]


def test_drops_flag_with_unknown_rule_id():
    result = verify_flags(
        [_flag("21 days to consider", ["federal.fake.rule"])], CONTRACT, RULE_IDS
    )
    assert not result.kept
    assert "unknown rule_id: federal.fake.rule" in result.dropped[0][1]
