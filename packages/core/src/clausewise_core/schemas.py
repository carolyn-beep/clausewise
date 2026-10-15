"""Pydantic models for ClauseWise (PLAN.md §5.4 FlagReport, §5.5 rule card).

These schemas are the contract between the corpus, the MCP server and the evals. The source
allowlist is enforced on ``RuleCard.source_url`` so a card with an off-allowlist source
cannot even be constructed.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from clausewise_core.allowlist import is_allowlisted
from clausewise_core.enums import Confidence, ContractType, IssueType, Severity


class PendingChange(BaseModel):
    """A not-yet-effective change to the law, surfaced but never applied as current."""

    model_config = ConfigDict(extra="forbid")

    bill: str
    status: str
    would_change: str


class StatuteChunk(BaseModel):
    """A verbatim slice of statute text, split at the subsection level with a context header."""

    model_config = ConfigDict(extra="forbid")

    ref: str
    context: str
    text: str


class RuleCard(BaseModel):
    """One (jurisdiction, topic) rule, versioned and tied to a dated primary source."""

    model_config = ConfigDict(extra="forbid")

    id: str
    jurisdiction: str
    topic: str
    citation: str
    source_url: str
    source_sha256: str | None = None
    effective_from: date
    effective_to: date | None = None
    last_verified: date
    verified_by: str
    confidence: Confidence = Confidence.medium
    statute_chunks: list[StatuteChunk] = Field(default_factory=list)
    plain_summary: str
    thresholds: dict[str, Any] = Field(default_factory=dict)
    pending_changes: list[PendingChange] = Field(default_factory=list)
    related_rules: list[str] = Field(default_factory=list)
    related_cases: list[str] = Field(default_factory=list)

    @field_validator("source_url")
    @classmethod
    def _source_url_must_be_allowlisted(cls, value: str) -> str:
        if not is_allowlisted(value):
            raise ValueError(
                f"source_url host is not on the primary-source allowlist: {value!r}"
            )
        return value

    def is_effective_on(self, as_of: date) -> bool:
        """True if this rule is in force on ``as_of`` (temporal validity, PLAN.md §6)."""
        if as_of < self.effective_from:
            return False
        if self.effective_to is not None and as_of > self.effective_to:
            return False
        return True


class Facts(BaseModel):
    """Facts extracted from the contract or supplied via MCP elicitation (PLAN.md §5.2)."""

    model_config = ConfigDict(extra="forbid")

    work_state: str | None = None
    governing_law_state: str | None = None
    annual_pay: float | None = None
    contract_date: date | None = None


class Flag(BaseModel):
    """One clause worth attention, with its plain-language explanation and citations."""

    model_config = ConfigDict(extra="forbid")

    clause_id: str
    clause_quote: str
    issue_type: IssueType
    severity: Severity
    jurisdiction_rule_ids: list[str] = Field(default_factory=list)
    explanation_plain: str
    questions_to_ask: list[str] = Field(default_factory=list)
    when_to_get_a_lawyer: str
    pending_changes: list[PendingChange] = Field(default_factory=list)


class FlagReport(BaseModel):
    """The structured report ``analyze_contract`` returns (PLAN.md §5.4)."""

    model_config = ConfigDict(extra="forbid")

    corpus_version: str
    as_of: date
    contract_type: ContractType
    jurisdictions: list[str] = Field(default_factory=list)
    facts: Facts = Field(default_factory=Facts)
    flags: list[Flag] = Field(default_factory=list)
    injection_warnings: list[str] = Field(default_factory=list)
    disclaimer: str
