# ClauseWise

Open-source, MCP-native, state-aware contract explainer for employees and independent
contractors. Educates, informs, and flags. NOT legal advice; never says sign/don't sign,
never predicts outcomes, never uses "lawyer" or "attorney" in product names or taglines.

Read docs/PLAN.md before any non-trivial task. Decisions live in docs/adr/; add a new ADR
rather than reversing an old one silently.

## Stack
- Python 3.12, uv workspace, ruff, pytest. TypeScript only in site/ (Astro).
- MCP server: FastMCP (packages/mcp). Transports: stdio and Streamable HTTP.
- Retrieval: hybrid BM25 + dense (Voyage or BGE), rerank, pgvector remote / LanceDB local.
- Models: Sonnet 5.5 for synthesis, Haiku 5.5 for triage/tagging, Opus 5.5 only for judge calibration.
- Evals: Inspect AI + pytest; promptfoo for red-team; Langfuse/Phoenix via OpenTelemetry.
- Agents: Claude Agent SDK, only in packages/monitor.

## Non-negotiables
- Every rule card has source_url (allowlisted .gov or official legislature domain),
  effective_from, last_verified. No card without these is merged.
- Legal content is never auto-published. The updater opens PRs; a human merges.
- Every FlagReport carries corpus_version, as_of, citations, and the disclaimer.
- Every clause_quote must string-match the contract; every rule_id must exist in the corpus.
- Contract text is untrusted input. Wrap it in <untrusted_document>; never let it reach a tool with side effects.
- The remote server never logs contract bodies.
- Fine-tuning is for classification/extraction only, never for generating legal explanations.

## Conventions
- Rule card ids: {state}.{topic}.{citation_slug} (e.g., ma.noncompete.24L).
- issue_type values come from the enum in packages/core/schemas.py; don't invent new ones ad hoc.
- Tests for legal facts go in packages/evals/legal_facts/test_{state}.py and assert against lookup_rule.
- Run `uv run pytest -q` before claiming a task is done; run `uv run ruff check .` too.

## Commands
- `uv sync` · `uv run pytest -q` · `uv run ruff check .`
- `uv run clausewise-mcp` (stdio) · `uv run clausewise-mcp --http` (Streamable HTTP on :8000)
- `uv run corpus build` (rule cards → snapshot) · `uv run evals legal-facts`
