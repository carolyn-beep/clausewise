"""Legal-fact suite: federal rules (PLAN.md §10.2, §15.1).

Deterministic assertions against ``lookup_rule``. These run on every PR and every monitoring
update; a new legal fact must ship with a new assertion here.
"""

from clausewise_corpus.loader import lookup_rule


def _owbpa():
    cards = lookup_rule("federal", "release_timing")
    assert cards, "OWBPA release-timing rule card not found in corpus"
    return cards[0]


# --- OWBPA 21 / 45 / 7 (the three required Phase 0 legal-fact tests) -------------------------


def test_owbpa_individual_consideration_period_is_21_days():
    assert _owbpa().thresholds["consider_days"] == 21


def test_owbpa_group_consideration_period_is_45_days():
    assert _owbpa().thresholds["consider_days_group"] == 45


def test_owbpa_revocation_period_is_7_days():
    assert _owbpa().thresholds["revoke_days"] == 7


# --- Other federal facts ---------------------------------------------------------------------


def test_ftc_noncompete_rule_is_not_in_effect():
    cards = lookup_rule("federal", "noncompete")
    assert cards, "FTC non-compete status card not found"
    assert "not in effect" in cards[0].plain_summary.lower()


def test_speak_out_act_is_present_and_dated():
    cards = lookup_rule("federal", "confidentiality_whistleblower")
    assert cards, "Speak Out Act card not found"
    assert cards[0].effective_from.isoformat() == "2022-12-07"


def test_owbpa_requires_written_advice_to_consult_counsel():
    assert "advise the worker in writing to consult counsel" in _owbpa().plain_summary


def test_owbpa_group_programs_disclose_titles_and_ages():
    assert "job titles and ages" in _owbpa().plain_summary


def test_ftc_enforcement_still_possible_under_section_5():
    card = lookup_rule("federal", "noncompete")[0]
    assert "Section 5" in card.plain_summary


def test_ftc_status_dated_to_cfr_removal():
    card = lookup_rule("federal", "noncompete")[0]
    assert card.effective_from.isoformat() == "2026-02-12"


def test_speak_out_covers_assault_and_harassment():
    summary = lookup_rule("federal", "confidentiality_whistleblower")[0].plain_summary.lower()
    assert "sexual assault" in summary
    assert "sexual harassment" in summary


def test_speak_out_applies_to_pre_dispute_clauses():
    summary = lookup_rule("federal", "confidentiality_whistleblower")[0].plain_summary.lower()
    assert "pre-dispute" in summary
