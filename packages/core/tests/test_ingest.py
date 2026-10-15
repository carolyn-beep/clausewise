"""Tests for document ingestion (text/.txt paths; parser extras are optional)."""

from pathlib import Path

import pytest
from clausewise_core.ingest import read_text


def test_raw_text_is_returned_unchanged():
    blob = "1. Term\nThis is raw contract text, not a file path."
    assert read_text(blob) == blob


def test_reads_txt_file(tmp_path: Path):
    p = tmp_path / "contract.txt"
    p.write_text("Hello clause.", encoding="utf-8")
    assert read_text(p) == "Hello clause."


def test_long_blob_is_not_treated_as_a_path():
    blob = "x" * 5000
    assert read_text(blob) == blob


def test_unsupported_suffix_raises(tmp_path: Path):
    p = tmp_path / "thing.rtf"
    p.write_text("data", encoding="utf-8")
    with pytest.raises(ValueError):
        read_text(p)
