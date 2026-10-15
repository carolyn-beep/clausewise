"""Load rule cards from bundled YAML and look them up (PLAN.md §5.3, §6).

Rule cards live as YAML under ``clausewise_corpus/rules/<jurisdiction>/*.yaml`` and ship with
the package, so the lookup works offline in the local MCP mode. ``lookup_rule`` filters by
jurisdiction, topic and temporal validity; it never applies a ``pending_change`` as current.
"""

from __future__ import annotations

import hashlib
from datetime import date
from functools import lru_cache
from importlib import resources
from importlib.resources.abc import Traversable
from typing import Any

import yaml
from clausewise_core.schemas import RuleCard

# Bumped by a human when a corpus PR is merged (PLAN.md §7.2, format YYYY.MM.N).
CORPUS_VERSION = "2026.10.0"


def _iter_yaml(node: Traversable) -> list[Traversable]:
    """Recursively collect every ``*.yaml`` / ``*.yml`` file under ``node``."""
    found: list[Traversable] = []
    for child in node.iterdir():
        if child.is_dir():
            found.extend(_iter_yaml(child))
        elif child.name.endswith((".yaml", ".yml")):
            found.append(child)
    return found


@lru_cache(maxsize=1)
def load_rules() -> tuple[RuleCard, ...]:
    """Load, validate and cache every rule card in the corpus, sorted by id."""
    rules_root = resources.files("clausewise_corpus") / "rules"
    cards: list[RuleCard] = []
    for path in _iter_yaml(rules_root):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        cards.append(RuleCard.model_validate(data))
    _assert_unique_ids(cards)
    return tuple(sorted(cards, key=lambda card: card.id))


def _assert_unique_ids(cards: list[RuleCard]) -> None:
    seen: set[str] = set()
    for card in cards:
        if card.id in seen:
            raise ValueError(f"duplicate rule card id in corpus: {card.id}")
        seen.add(card.id)


def lookup_rule(state: str, topic: str, as_of: date | None = None) -> list[RuleCard]:
    """Return rule cards matching ``state`` and ``topic`` that are effective on ``as_of``.

    ``state`` is ``"federal"`` or a two-letter code (e.g. ``"CA"``). ``as_of`` defaults to
    today. Results are sorted by rule id for determinism.
    """
    as_of = as_of or date.today()
    matches = [
        card
        for card in load_rules()
        if card.jurisdiction == state and card.topic == topic and card.is_effective_on(as_of)
    ]
    return sorted(matches, key=lambda card: card.id)


def manifest() -> dict[str, Any]:
    """Return the corpus manifest (PLAN.md §5.3 ``clausewise://corpus/manifest``)."""
    cards = load_rules()
    payload = "\n".join(f"{card.id}:{card.source_sha256 or ''}" for card in cards)
    return {
        "corpus_version": CORPUS_VERSION,
        "rule_count": len(cards),
        "snapshot_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "jurisdictions": sorted({card.jurisdiction for card in cards}),
    }
