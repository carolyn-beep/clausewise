"""Clause segmentation (PLAN.md §8.1).

Split contract text into clauses at heading / numbering boundaries using regex. A later,
optional LLM "repair" pass (key-dependent) can clean up messy documents; this module is the
deterministic baseline and is the only one needed for well-structured contracts.
"""

from __future__ import annotations

import re

from clausewise_core.schemas import Clause

# Lines that look like the start of a numbered or titled section, e.g.
#   "1. Confidentiality"      "1.2 Term"      "Section 4. Release"
#   "ARTICLE V - NON-COMPETE"  "(a) Definitions"
_HEADING_RE = re.compile(
    r"""^[ \t]*(
        (?:section|article)\s+[0-9ivxlc]+          # Section 4 / ARTICLE V
        | [0-9]+(?:\.[0-9]+)*\.?                    # 1  / 1.2  / 3.
        | \([0-9a-z]+\)                             # (a) / (12)
    )[ \t]*[.:\-–)]?[ \t]*(.*)$""",
    re.IGNORECASE | re.VERBOSE,
)


def segment_clauses(text: str) -> list[Clause]:
    """Segment ``text`` into clauses at heading/numbering boundaries.

    Returns clauses with ids ``c1``, ``c2``, … and their character spans in ``text``. If no
    headings are found, the whole document is returned as a single clause so downstream code
    always has something to work with.
    """
    lines = text.splitlines(keepends=True)
    boundaries: list[tuple[int, str | None]] = []  # (char offset, heading text)
    offset = 0
    for line in lines:
        stripped = line.strip()
        match = _HEADING_RE.match(line) if stripped else None
        if match:
            marker, title = match.group(1).strip(), match.group(2).strip()
            heading = f"{marker} {title}".strip() if title else marker
            boundaries.append((offset, heading))
        offset += len(line)

    if not boundaries:
        body = text.strip()
        if not body:
            return []
        start = text.index(body)
        return [Clause(id="c1", heading=None, text=body, start=start, end=start + len(body))]

    # Keep any preamble before the first heading (title, parties, effective date) as a clause.
    if boundaries[0][0] > 0 and text[: boundaries[0][0]].strip():
        boundaries.insert(0, (0, None))

    clauses: list[Clause] = []
    for index, (start, heading) in enumerate(boundaries):
        end = boundaries[index + 1][0] if index + 1 < len(boundaries) else len(text)
        chunk = text[start:end].rstrip()
        clauses.append(
            Clause(
                id=f"c{index + 1}",
                heading=heading,
                text=chunk,
                start=start,
                end=start + len(chunk),
            )
        )
    return clauses
