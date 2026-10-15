# ADR-004: The corpus is versioned rule cards; updates are human-merged PRs, never auto-published

- **Status:** Accepted (2026-10-15)

## Context

Employment law in scope is changing fast (WA 2027 ban, NY pending bill, CA 2026 stay-or-pay
ban, FTC rule removed). Auto-publishing legal content is how a tool becomes dangerous.

## Decision

The corpus is versioned "rule cards" with primary-source URLs, effective dates and
`last_verified`. A scheduled monitoring agent opens pull requests; a human reviews and merges
only after the legal-fact suite passes. Merges tag a corpus version `YYYY.MM.N` and sign the
snapshot.

## Consequences

- Legal content is **never** auto-published.
- Every rule card carries `source_url` (allowlisted), `effective_from`, `last_verified`.
- Temporal validity and pending changes are explicit in the data, not left to the model.
