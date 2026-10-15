# ADR-003: RAG + strong prompting + structured outputs; fine-tuning is a scoped benchmark

- **Status:** Accepted (2026-10-15)

## Context

A frontier model with good retrieval beats a fine-tuned ~8B model at nuanced legal synthesis.
Fine-tuning for *classification* is measurable and teachable; fine-tuning for *generation*
would bake law into weights that cannot be updated when the law changes.

## Decision

The core method is RAG + strong prompting + structured outputs with a frontier model.
Fine-tuning is a scoped benchmark module (`classify_clauses`), optional at runtime: the
pipeline must work without it and fall back to the client LLM.

## Consequences

- Legal knowledge stays in the versioned corpus, not in model weights (see ADR-004).
- Fine-tune only for classification/extraction, where outputs are checkable.
- Revisit if the benchmark shows the local classifier clearly wins on cost/latency for local
  mode.
