# ruff: noqa: E501 - one RetrievalQuery per line keeps this data file readable.
"""Question → gold-rule-card pairs for retrieval evaluation (PLAN.md §10.2).

Natural, worker-phrased questions, each labelled with the jurisdiction(s) known at query time
(as in real use, where the worker's state is known) and the single rule card that should be
retrieved. Grows toward ~150 pairs per state over the project; this is the federal + CA set.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

_2026 = date(2026, 6, 1)  # a date on which AB 692 (stay-or-pay) is already effective


@dataclass(frozen=True)
class RetrievalQuery:
    question: str
    jurisdictions: tuple[str, ...]
    gold_rule_id: str
    as_of: date | None = None


QUERIES: list[RetrievalQuery] = [
    # --- Federal: OWBPA release timing -----------------------------------------------------
    RetrievalQuery("How many days do I get to consider a severance agreement?", ("federal",), "federal.owbpa.626f"),
    RetrievalQuery("Can my employer give me only 7 days to sign a release of age claims?", ("federal",), "federal.owbpa.626f"),
    RetrievalQuery("What are the OWBPA waiting periods for a waiver of age discrimination?", ("federal",), "federal.owbpa.626f"),
    RetrievalQuery("I'm over 40 in a group layoff — what ages and titles must be disclosed?", ("federal",), "federal.owbpa.626f"),
    # --- Federal: FTC non-compete status ---------------------------------------------------
    RetrievalQuery("Is the FTC noncompete ban in effect?", ("federal",), "federal.ftc_noncompete.status"),
    RetrievalQuery("Did the nationwide non-compete rule get removed?", ("federal",), "federal.ftc_noncompete.status"),
    RetrievalQuery("Are noncompetes banned by federal law right now?", ("federal",), "federal.ftc_noncompete.status"),
    RetrievalQuery("What happened to the FTC rule on non-competes?", ("federal",), "federal.ftc_noncompete.status"),
    # --- Federal: Speak Out Act ------------------------------------------------------------
    RetrievalQuery("Can an NDA stop me from talking about sexual harassment?", ("federal",), "federal.speak_out.9usc401"),
    RetrievalQuery("Is a pre-dispute non-disparagement clause about harassment enforceable?", ("federal",), "federal.speak_out.9usc401"),
    RetrievalQuery("Does the Speak Out Act cover sexual assault nondisclosure clauses?", ("federal",), "federal.speak_out.9usc401"),
    RetrievalQuery("My onboarding NDA bars me from discussing harassment claims — is that valid?", ("federal",), "federal.speak_out.9usc401"),
    # --- CA: §16600 noncompetes void -------------------------------------------------------
    RetrievalQuery("Are noncompete clauses void in California?", ("CA",), "ca.noncompete.16600"),
    RetrievalQuery("Is my California noncompete enforceable under section 16600?", ("CA",), "ca.noncompete.16600"),
    RetrievalQuery("Can a California employer stop me working in my profession or trade?", ("CA",), "ca.noncompete.16600"),
    RetrievalQuery("Does California law make employee noncompetes unenforceable?", ("CA",), "ca.noncompete.16600"),
    # --- CA: §16600.1 void-notice ----------------------------------------------------------
    RetrievalQuery("Does my California employer have to notify me my noncompete is void?", ("CA",), "ca.noncompete.16600_1"),
    RetrievalQuery("What was the February 2024 deadline for noncompete notices in California?", ("CA",), "ca.noncompete.16600_1"),
    RetrievalQuery("Am I owed written notice that my non-compete is void?", ("CA",), "ca.noncompete.16600_1"),
    # --- CA: §16600.5 out-of-state noncompete ----------------------------------------------
    RetrievalQuery("I signed a noncompete out of state but work in California — is it enforceable?", ("CA",), "ca.choice_of_law.16600_5"),
    RetrievalQuery("Can a noncompete be enforced against me in California regardless of where I signed?", ("CA",), "ca.choice_of_law.16600_5"),
    RetrievalQuery("Can I sue my employer for including a void noncompete in California?", ("CA",), "ca.choice_of_law.16600_5"),
    # --- CA: §925 choice of law / forum ----------------------------------------------------
    RetrievalQuery("Can my employer force me to litigate in another state if I work in California?", ("CA",), "ca.choice_of_law.925"),
    RetrievalQuery("My contract picks Delaware law but I work in CA — does that bind me?", ("CA",), "ca.choice_of_law.925"),
    RetrievalQuery("When can a California employee be held to out-of-state law — only with their own lawyer?", ("CA",), "ca.choice_of_law.925"),
    # --- CA: AB 692 stay-or-pay ------------------------------------------------------------
    RetrievalQuery("Do I have to repay my signing bonus if I quit early in California?", ("CA",), "ca.stay_or_pay.ab692", _2026),
    RetrievalQuery("Is a training repayment agreement enforceable in California now?", ("CA",), "ca.stay_or_pay.ab692", _2026),
    RetrievalQuery("What does the California stay-or-pay ban (AB 692) do?", ("CA",), "ca.stay_or_pay.ab692", _2026),
    # --- CA: §2870 invention assignment ----------------------------------------------------
    RetrievalQuery("Does my California employer own inventions I make on my own time?", ("CA",), "ca.invention_assignment.2870"),
    RetrievalQuery("Can an invention assignment clause take my personal side project in California?", ("CA",), "ca.invention_assignment.2870"),
    RetrievalQuery("What inventions are carved out under California Labor Code 2870?", ("CA",), "ca.invention_assignment.2870"),
    # --- CA: §§201-203 final pay -----------------------------------------------------------
    RetrievalQuery("When do I get my final wages after being fired in California?", ("CA",), "ca.final_pay.201"),
    RetrievalQuery("How long does my employer have to pay me if I quit in California?", ("CA",), "ca.final_pay.201"),
    RetrievalQuery("What are waiting time penalties for late final pay in California?", ("CA",), "ca.final_pay.201"),
    # --- CA: §2775 misclassification -------------------------------------------------------
    RetrievalQuery("Am I misclassified as an independent contractor in California?", ("CA",), "ca.misclassification.2775"),
    RetrievalQuery("What is the ABC test for employee versus contractor in California?", ("CA",), "ca.misclassification.2775"),
    RetrievalQuery("Does California presume I am an employee under AB 5?", ("CA",), "ca.misclassification.2775"),
]
