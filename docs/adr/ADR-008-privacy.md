# ADR-008: Privacy ladder — default local MCP + the user's cloud LLM

- **Status:** Accepted (2026-10-15)

## Context

Contracts often contain confidentiality clauses; uploading a signed NDA or severance
agreement to a third party could itself be a prohibited disclosure (PLAN.md §13.3).

## Decision

Default recommendation is local MCP + the user's own cloud LLM. Fully local (local MCP +
Ollama) is offered for maximum privacy. The remote server keeps contract text in memory only
and logs no bodies. A redaction pre-pass (party names, amounts, dates) is available at every
level, as is sending only extracted clauses.

## Consequences

- Local mode removes ClauseWise as a third party entirely; the contract still reaches the
  user's chosen LLM provider.
- Privacy policy/ToS must state: no storage of contract text on the remote server, no training
  on user data, which providers see the text, and the logging scope.
- Revisit if a hosted upload surface is ever added.
