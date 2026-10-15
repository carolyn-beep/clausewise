"""Controlled vocabularies for ClauseWise.

`issue_type` values are frozen here (PLAN.md §5.4). Do not invent new ones ad hoc; add a
member here first so the schema, the corpus and the evals all agree.
"""

from enum import StrEnum


class ContractType(StrEnum):
    """The kinds of worker-side documents ClauseWise analyzes (PLAN.md §8.1)."""

    nda = "nda"
    employment_agreement = "employment_agreement"
    offer_letter = "offer_letter"
    separation_agreement = "separation_agreement"
    piia = "piia"  # proprietary-information / invention-assignment agreement
    contractor_agreement = "contractor_agreement"
    sow = "sow"
    unknown = "unknown"


class IssueType(StrEnum):
    """Clause categories a flag can carry (PLAN.md §5.4)."""

    noncompete = "noncompete"
    non_solicit = "non_solicit"
    invention_assignment = "invention_assignment"
    confidentiality_whistleblower = "confidentiality_whistleblower"
    non_disparagement = "non_disparagement"
    arbitration = "arbitration"
    class_waiver = "class_waiver"
    choice_of_law = "choice_of_law"
    forum_selection = "forum_selection"
    release_timing = "release_timing"
    release_scope = "release_scope"
    final_pay = "final_pay"
    misclassification = "misclassification"
    liquidated_damages = "liquidated_damages"
    indemnification = "indemnification"
    payment_terms = "payment_terms"
    late_fees = "late_fees"
    kill_fee = "kill_fee"
    stay_or_pay = "stay_or_pay"
    unilateral_modification = "unilateral_modification"
    other = "other"


class Severity(StrEnum):
    """How much attention a flag deserves. `critical` drives the missed-critical-flag eval."""

    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Confidence(StrEnum):
    """How confident we are in a rule card, pending attorney review."""

    high = "high"
    medium = "medium"
    low = "low"
