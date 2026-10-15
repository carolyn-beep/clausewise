"""Tests for the primary-source domain allowlist."""

from clausewise_core.allowlist import is_allowlisted


def test_gov_hosts_are_allowed():
    assert is_allowlisted("https://uscode.house.gov/view.xhtml?req=x")
    assert is_allowlisted("https://leginfo.legislature.ca.gov/faces/codes.xhtml")
    assert is_allowlisted("https://www.ftc.gov/legal-library/browse/rules/noncompete-rule")
    assert is_allowlisted("https://malegislature.gov/Laws/GeneralLaws")
    assert is_allowlisted("https://federalregister.gov/documents/2026")


def test_trusted_non_gov_open_data_is_allowed():
    assert is_allowlisted("https://www.courtlistener.com/opinion/1234/")
    assert is_allowlisted("https://api.legiscan.com/?op=getBill&id=1")


def test_non_official_hosts_are_blocked():
    assert not is_allowlisted("https://example.com/statute")
    assert not is_allowlisted("https://fakergov.com")  # ends with .com, not .gov
    assert not is_allowlisted("https://gov.evil.com/x")
    assert not is_allowlisted("not a url at all")
    assert not is_allowlisted("")
