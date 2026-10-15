# ADR-006: Free and open source; no paid tier planned

- **Status:** Accepted (2026-10-15)

## Context

This is a portfolio and mission project. Charging also raises consumer-protection and UPL
exposure (paid users bring refund/warranty expectations, and a fee for applying law to a
specific contract looks more like practicing law).

## Decision

Free and open source: Apache-2.0 for code, CC BY 4.0 for plain-language summaries. No paid
tier planned. The remote server keeps auth hooks, usage metering and per-user rate limits as
abuse and cost controls, not as a product tier.

## Consequences

- Lower legal exposure; optionality for a paid tier preserved without a rewrite.
- Revisit only if the project outgrows the budget; options recorded in PLAN.md §13.4.
