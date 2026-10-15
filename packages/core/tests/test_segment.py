"""Tests for clause segmentation."""

from clausewise_core.segment import segment_clauses


def test_segments_numbered_sections_plus_preamble(severance_text: str):
    clauses = segment_clauses(severance_text)
    # Preamble + five numbered sections.
    assert len(clauses) == 6
    assert clauses[0].heading is None  # preamble (title + parties)
    headings = [c.heading for c in clauses if c.heading]
    assert any("Severance Payment" in h for h in headings)
    assert any("Governing Law" in h for h in headings)


def test_clause_spans_point_back_at_source(severance_text: str):
    for clause in segment_clauses(severance_text):
        assert severance_text[clause.start : clause.end] == clause.text


def test_clause_ids_are_sequential(severance_text: str):
    ids = [c.id for c in segment_clauses(severance_text)]
    assert ids == [f"c{i + 1}" for i in range(len(ids))]


def test_unstructured_text_is_one_clause():
    clauses = segment_clauses("Just a single paragraph with no headings at all.")
    assert len(clauses) == 1
    assert clauses[0].id == "c1"


def test_empty_text_yields_no_clauses():
    assert segment_clauses("   \n  ") == []
