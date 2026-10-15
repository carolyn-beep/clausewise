"""Smoke tests: the server imports, the tool is registered, and it returns a sane payload."""

import asyncio
import inspect

from clausewise_mcp.server import build_lookup_payload, main, mcp


def test_server_objects_exist():
    assert mcp.name == "clausewise"
    assert callable(main)


def test_tool_is_registered():
    result = mcp.list_tools()
    tools = asyncio.run(result) if inspect.isawaitable(result) else result
    names = {getattr(tool, "name", None) for tool in tools}
    assert "lookup_rule" in names


def test_lookup_payload_returns_owbpa():
    payload = build_lookup_payload("federal", "release_timing")
    assert payload["query"] == {"state": "federal", "topic": "release_timing"}
    assert payload["disclaimer"]
    assert payload["corpus_version"]
    assert any(rule["id"] == "federal.owbpa.626f" for rule in payload["rules"])
