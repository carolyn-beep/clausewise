# ADR-001: Python for everything except the marketing site

- **Status:** Accepted (2026-10-15)

## Context

ClauseWise is RAG-, fine-tuning-, evals- and document-parsing-heavy, all of which are
Python-native. The MCP Python SDK is Tier 1 (v2.0.0 GA July 28, 2026) and the server calls
RAG/classifier code in-process. The budget is 10–15 hours/week.

## Decision

Use Python for ~95% of the codebase. TypeScript only in `site/` (Astro) for the marketing
page. Manage everything as one `uv` workspace plus a `site/` folder.

## Consequences

- One language for nearly all code is the biggest productivity win at this time budget.
- Interview framing: "Python for ML and data, TypeScript where the web demands it."
- Revisit only if a web app with heavy UI is added.
