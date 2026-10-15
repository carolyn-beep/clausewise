# ADR-002: One MCP server, shipped local (stdio) and remote (Streamable HTTP)

- **Status:** Accepted (2026-10-15)

## Context

Users bring their own LLM and pay for their own inference. ChatGPT connects only to remote
HTTPS MCP servers; privacy-minded users want a local install. A contract-upload web app would
add hosting, privacy and UPL-perception obligations.

## Decision

Ship one MCP server two ways: a local `stdio` package (`uvx clausewise-mcp` / `.mcpb` bundle)
and a remote Streamable HTTP endpoint. No contract-upload web app in v1. The landing page gets
a rate-limited demo that runs only on pre-loaded sample contracts.

## Consequences

- No inference cost to us in MCP mode; the user's LLM does the reasoning.
- Remote server needs rate limiting and, for per-user state, OAuth 2.1.
- Revisit a real upload web app only after evals are solid and if users ask.
