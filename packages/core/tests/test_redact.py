"""Tests for the redaction pre-pass."""

from clausewise_core.redact import redact, restore


def test_redacts_amounts_dates_emails_and_names(severance_text: str):
    result = redact(severance_text, party_names=["Acme Robotics, Inc.", "Jordan Rivera"])
    assert "$42,500.00" not in result.text
    assert "January 15, 2026" not in result.text
    assert "hr@acmerobotics.example" not in result.text
    assert "Acme Robotics, Inc." not in result.text
    assert "Jordan Rivera" not in result.text
    # Placeholders appear instead.
    assert "[AMOUNT_1]" in result.text
    assert "[EMAIL_1]" in result.text
    assert "[PARTY_1]" in result.text


def test_redaction_round_trips(severance_text: str):
    result = redact(severance_text, party_names=["Acme Robotics, Inc.", "Jordan Rivera"])
    assert restore(result.text, result.mapping) == severance_text


def test_equal_values_share_a_placeholder():
    text = "Pay $100 now and $100 later to Acme and Acme."
    result = redact(text, party_names=["Acme"])
    # One amount placeholder reused, one party placeholder reused.
    assert result.text.count("[AMOUNT_1]") == 2
    assert result.text.count("[PARTY_1]") == 2
    assert "[AMOUNT_2]" not in result.text


def test_no_party_names_still_redacts_patterns():
    result = redact("Invoice total: $1,250.50 due 01/15/2026.")
    assert "$1,250.50" not in result.text
    assert "01/15/2026" not in result.text
