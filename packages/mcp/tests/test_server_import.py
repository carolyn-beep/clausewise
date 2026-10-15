"""Smoke tests: the server imports, tools are registered, and payloads look right."""

import asyncio
import inspect

from clausewise_mcp.server import (
    build_deadlines_payload,
    build_explain_payload,
    build_lookup_payload,
    main,
    mcp,
)


def test_server_objects_exist():
    assert mcp.name == "clausewise"
    assert callable(main)


def test_tools_are_registered():
    result = mcp.list_tools()
    tools = asyncio.run(result) if inspect.isawaitable(result) else result
    names = {getattr(tool, "name", None) for tool in tools}
    assert {"lookup_rule", "explain_clause", "check_deadlines"} <= names


def test_lookup_payload_returns_owbpa():
    payload = build_lookup_payload("federal", "release_timing")
    assert payload["query"] == {"state": "federal", "topic": "release_timing"}
    assert payload["disclaimer"]
    assert any(rule["id"] == "federal.owbpa.626f" for rule in payload["rules"])


def test_explain_payload_retrieves_relevant_rules():
    payload = build_explain_payload(
        "Employee shall not compete with the Company for two years.",
        state="CA",
        topic="noncompete",
    )
    ids = {rule["id"] for rule in payload["relevant_rules"]}
    assert "ca.noncompete.16600" in ids
    assert payload["disclaimer"]


def test_explain_payload_without_topic_still_returns_noncompete_rules():
    # Without a topic filter, BM25 on a short clause is noisier, but a non-compete-relevant
    # rule should still surface among the top results (dense retrieval improves this later).
    payload = build_explain_payload(
        "Employee shall not compete with the Company for two years.", state="CA"
    )
    ids = {rule["id"] for rule in payload["relevant_rules"]}
    noncompete_related = {
        "ca.noncompete.16600",
        "ca.noncompete.16600_1",
        "ca.choice_of_law.16600_5",
        "federal.ftc_noncompete.status",
    }
    assert ids & noncompete_related


def test_deadlines_payload_surfaces_owbpa_windows():
    payload = build_deadlines_payload(state="CA", contract_type="separation_agreement")
    rules = {rule["id"]: rule for rule in payload["deadline_rules"]}
    assert "federal.owbpa.626f" in rules
    assert rules["federal.owbpa.626f"]["thresholds"]["consider_days"] == 21
