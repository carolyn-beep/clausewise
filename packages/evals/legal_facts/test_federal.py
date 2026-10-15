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
