"""Document ingestion (PLAN.md §8.1).

Turn a contract into plain text for segmentation. Plain text, ``.txt`` and ``.md`` work with
no extra dependencies. ``.docx`` and ``.pdf`` need the optional ``parse`` extra
(``uv sync --extra parse``); layout-aware Docling parsing is a later enhancement. Raw text
passed directly is returned unchanged, so the pipeline is testable without any parser.
"""

from __future__ import annotations

from pathlib import Path

_TEXT_SUFFIXES = {".txt", ".md", ""}


def read_text(source: str | Path) -> str:
    """Return the plain text of ``source``.

    ``source`` may be a path to a ``.txt``/``.md``/``.docx``/``.pdf`` file, or raw contract
    text. A value that is not an existing file path is treated as raw text and returned as-is.
    """
    path = _as_existing_path(source)
    if path is None:
        return str(source)

    suffix = path.suffix.lower()
    if suffix in _TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        return _read_docx(path)
    if suffix == ".pdf":
        return _read_pdf(path)
    raise ValueError(f"unsupported document type: {suffix!r} ({path})")


def _as_existing_path(source: str | Path) -> Path | None:
    if isinstance(source, Path):
        return source if source.exists() else None
    # A long blob of contract text is not a path; guard against "file name too long".
    if "\n" in source or len(source) > 1024:
        return None
    try:
        path = Path(source)
    except (ValueError, OSError):
        return None
    return path if path.exists() else None


def _read_docx(path: Path) -> str:
    try:
        import docx  # python-docx
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised only without the extra
        raise ModuleNotFoundError(
            "Reading .docx needs the 'parse' extra: uv sync --extra parse"
        ) from exc
    document = docx.Document(str(path))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def _read_pdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised only without the extra
        raise ModuleNotFoundError(
            "Reading .pdf needs the 'parse' extra: uv sync --extra parse"
        ) from exc
    with fitz.open(str(path)) as doc:
        return "\n".join(page.get_text() for page in doc)
