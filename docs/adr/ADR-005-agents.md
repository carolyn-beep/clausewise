# ADR-005: Single structured pass for analysis; multi-agent only for offline monitoring

- **Status:** Accepted (2026-10-15)

## Context

The user-facing analysis has known steps (parse → classify → retrieve → synthesize → verify).
Anthropic's "Building effective agents" guidance prefers workflows over agents when the steps
are known.

## Decision

The user-facing analysis is a single structured-output pass with deterministic verification.
Multi-agent orchestration (Claude Agent SDK) is used only for the offline monitoring/updater
pipeline, plus an optional, measured "deep review" mode for multi-document packets.

## Consequences

- Cheaper, faster, easier to evaluate and to explain in an interview.
- Agents live only in `packages/monitor`.
- Revisit "deep review" only if it beats single-pass on the golden set.
