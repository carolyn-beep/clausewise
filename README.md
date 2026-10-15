# ClauseWise

Open-source, MCP-native, **state-aware contract explainer** for employees and independent
contractors. It reads the paper the stronger party handed you, flags the clauses that
deserve attention, explains what each one does in plain language, and cites the relevant
state or federal rule with a primary-source link and an "as of" date.

> **ClauseWise provides legal information and education, not legal advice.** It does not tell
> you whether to sign, does not predict how a dispute would end, and is not a substitute for
> a qualified attorney licensed in your state.

See [`docs/PLAN.md`](docs/PLAN.md) for the full project plan and
[`docs/adr/`](docs/adr/) for the architecture decisions.

## What it is

- **Jurisdictions:** a federal overlay plus six priority states — California, New York,
  Texas, Washington, Illinois, Massachusetts.
- **Documents:** NDAs, offer letters and employment agreements, separation/severance
  agreements, invention-assignment agreements (PIIAs), independent-contractor agreements,
  SOWs and payment terms.
- **Surface:** one MCP server, shipped two ways — a local `stdio` package (your LLM does the
  reasoning, the contract never leaves your machine except to the model you already use) and
  a remote Streamable HTTP endpoint (required for ChatGPT).

## What it is not

Not a lawyer, not legal advice, not a prediction of how a dispute would end, and not a
recommendation to sign or not sign. The product name and tagline never use the words
"lawyer" or "attorney".

## Repository layout

```
packages/core      parsing, clause segmentation, schemas, retrieval, citation verification
packages/corpus    versioned rule cards (YAML) + loader/lookup + snapshot build
packages/mcp       FastMCP server (stdio + Streamable HTTP)
packages/evals     Inspect AI tasks, legal-fact suite, golden sets, red-team
packages/monitor   deterministic collectors + human-gated updater agent
packages/ft        fine-tuning benchmark (QLoRA clause classifier)
site/              Astro landing page
```

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 (uv will fetch it).

```bash
uv sync --all-packages          # create the venv and install every workspace package
uv run ruff check .             # lint
uv run pytest -q                # unit + legal-fact tests
uv run clausewise-mcp           # run the MCP server over stdio
uv run clausewise-mcp --http    # run it over Streamable HTTP on :8000
```

### Register the local server with an MCP client

**Claude Code** — already wired up via [`.mcp.json`](.mcp.json) at the repo root; approve the
server when prompted, then ask it to call `lookup_rule`.

**Claude Desktop** — add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clausewise": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/carolyndriscoll/clausewise", "clausewise-mcp"]
    }
  }
}
```

## Status

**Phase 1 in progress (California corpus + RAG).** Built so far:

- **Corpus:** 3 federal + 8 California rule cards (summary-level; verbatim statute text and
  exact effective dates are tracked for primary-source verification).
- **MCP tools (read-only):** `lookup_rule`, `explain_clause`, `check_deadlines`, plus guided
  prompts (`review_severance`/`review_offer`/`review_nda`/`review_contractor_agreement`) and
  the `clausewise://corpus/manifest` resource.
- **Analysis primitives:** clause segmentation, contract-type detection, a reversible
  redaction pre-pass, deterministic citation verification, and BM25 retrieval.
- **Evals:** 53 legal-fact assertions; a retrieval eval harness (BM25 recall@5 **0.973** on
  37 worker questions).

Still ahead in Phase 1 (needs API keys): dense/hybrid retrieval + rerank, the single-pass
Claude analysis (`analyze_contract` → `FlagReport`), and the golden-contract flag evals. See
`docs/PLAN.md` §15.

```bash
uv run clausewise-retrieval-eval   # print the retrieval metrics table
```

## Licenses

- Code: **Apache-2.0** (see [`LICENSE`](LICENSE)).
- Corpus plain-language summaries: **CC BY 4.0**.
- Statute text: public domain.
