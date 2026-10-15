"""Shared fixtures for core tests."""

from pathlib import Path

import pytest

_FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def severance_text() -> str:
    return (_FIXTURES / "sample_severance.txt").read_text(encoding="utf-8")
