# ADR-007: Legal information, never legal advice

- **Status:** Accepted (2026-10-15)

## Context

The UPL line (PLAN.md §13.1) separates protected legal *information* from licensed legal
*advice*. The FTC's DoNotPay order (§13.2) shows regulators act on deceptive *claims*.

## Decision

Outputs flag, cite, explain, suggest questions and point to lawyer referrals. They never say
sign/don't sign and never predict how a dispute would end. Disclaimers are clear and
conspicuous at the point of use. The product name and tagline never use "lawyer" or
"attorney". Marketing claims are backed by published evals.

## Consequences

- Every FlagReport carries citations, `as_of`, `corpus_version` and the disclaimer.
- Preferred phrasing: "Courts in California have treated clauses like this as void under
  §16600; a qualified professional can confirm how that applies to you."
- Get an employment attorney or law-school clinic to review at least one state before launch.
- Revisit: never.
