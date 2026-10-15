"""Tests that the corpus loads, validates, and looks up correctly."""

from datetime import date

from clausewise_corpus.loader import CORPUS_VERSION, load_rules, lookup_rule, manifest


def test_all_cards_load_and_validate():
    cards = load_rules()
    assert len(cards) >= 3  # three federal cards in Phase 0
    ids = {card.id for card in cards}
    assert {
        "federal.owbpa.626f",
        "federal.ftc_noncompete.status",
        "federal.speak_out.9usc401",
    } <= ids


def test_every_card_has_required_provenance():
    # Non-negotiable (CLAUDE.md): source_url, effective_from, last_verified on every card.
    for card in load_rules():
        assert card.source_url
        assert card.effective_from is not None
        assert card.last_verified is not None


def test_lookup_rule_filters_by_jurisdiction_and_topic():
    cards = lookup_rule("federal", "release_timing")
    assert [c.id for c in cards] == ["federal.owbpa.626f"]
    assert lookup_rule("federal", "nonexistent_topic") == []
    assert lookup_rule("ZZ", "release_timing") == []


def test_lookup_rule_respects_as_of_before_effective_date():
    # OWBPA is effective from 1990; a 1985 contract should not match it.
    assert lookup_rule("federal", "release_timing", as_of=date(1985, 1, 1)) == []
    assert lookup_rule("federal", "release_timing", as_of=date(2026, 10, 15))


def test_manifest_shape():
    m = manifest()
    assert m["corpus_version"] == CORPUS_VERSION
    assert m["rule_count"] >= 3
    assert "federal" in m["jurisdictions"]
    assert len(m["snapshot_sha256"]) == 64
