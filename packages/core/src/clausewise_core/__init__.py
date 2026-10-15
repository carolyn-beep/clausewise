"""ClauseWise core: shared schemas, enums, the source allowlist, and the disclaimer."""

from clausewise_core.disclaimer import DISCLAIMER
from clausewise_core.enums import Confidence, ContractType, IssueType, Severity
from clausewise_core.schemas import (
    Clause,
    Facts,
    Flag,
    FlagReport,
    PendingChange,
    RuleCard,
    StatuteChunk,
)

__all__ = [
    "DISCLAIMER",
    "Confidence",
    "ContractType",
    "IssueType",
    "Severity",
    "Clause",
    "Facts",
    "Flag",
    "FlagReport",
    "PendingChange",
    "RuleCard",
    "StatuteChunk",
]
