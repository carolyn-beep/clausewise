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

**Phase 0 (foundations).** Workspace, CI, schemas, a "hello" `lookup_rule` tool backed by
three verified federal rule cards (OWBPA, FTC non-compete status, Speak Out Act), and the
first legal-fact tests. Phase 1 (California corpus + RAG) is next; see `docs/PLAN.md` §15.

## Licenses

- Code: **Apache-2.0** (see [`LICENSE`](LICENSE)).
- Corpus plain-language summaries: **CC BY 4.0**.
- Statute text: public domain.
