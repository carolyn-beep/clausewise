"""Tests for contract-type detection."""

from clausewise_core.detect import detect_contract_type
from clausewise_core.enums import ContractType


def test_detects_separation_agreement(severance_text: str):
    assert detect_contract_type(severance_text) == ContractType.separation_agreement


def test_detects_nda():
    text = (
        "MUTUAL NON-DISCLOSURE AGREEMENT. The parties will exchange Confidential Information "
        "and agree to maintain confidentiality."
    )
    assert detect_contract_type(text) == ContractType.nda


def test_detects_independent_contractor():
    text = (
        "INDEPENDENT CONTRACTOR AGREEMENT. Contractor agrees to perform the services described "
        "in this services agreement."
    )
    assert detect_contract_type(text) == ContractType.contractor_agreement


def test_unknown_when_no_signal():
    assert detect_contract_type("The quick brown fox jumps over the lazy dog.") == (
        ContractType.unknown
    )
