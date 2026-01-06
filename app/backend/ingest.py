from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

import fitz  # PyMuPDF
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper
from app.backend.fts import rebuild_fts


# -------------------------------------------------------------------
# DOI detection
# -------------------------------------------------------------------

DOI_RE = re.compile(
    r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b",
    re.IGNORECASE,
)


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_pdf_text_first_pages(
    path: Path,
    max_pages: int = 2,
    max_chars: int = 20000,
) -> str:
    doc = fitz.open(str(path))
    parts = []
    pages = min(max_pages, doc.page_count)

    for i in range(pages):
        parts.append(doc.load_page(i).get_text("text"))
        if sum(len(p) for p in parts) > max_chars:
            break

    doc.close()
    return "\n".join(parts)[:max_chars]


def extract_pdf_metadata(path: Path) -> Tuple[str, str]:
    """
    Return (title, author) from PDF metadata if present.
    """
    doc = fitz.open(str(path))
    md = doc.metadata or {}
    doc.close()

    title = (md.get("title") or "").strip()
    author = (md.get("author") or "").strip()
    return title, author


def detect_doi(text: str) -> Optional[str]:
    m = DOI_RE.search(text)
    return m.group(0).strip() if m else None


# -------------------------------------------------------------------
# Ingest
# -------------------------------------------------------------------

def ingest_pdf(path: Path) -> dict:
    """
    Ingest a single PDF into the library (MVP).

    - Hash-based dedup
    - DOI-based dedup
    - Paper creation only (no file table yet)
    """
    if not path.exists():
        raise FileNotFoundError(str(path))

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Only PDF supported for MVP. Got: {path.name}")

    file_hash = sha256_file(path)

    # Extract text + metadata
    title, author = extract_pdf_metadata(path)
    text = extract_pdf_text_first_pages(path)
    doi = detect_doi(text)

    with get_session() as session:
        # DOI-level dedup
        paper: Optional[Paper] = None
        if doi:
            paper = session.exec(
                select(Paper).where(Paper.doi == doi)
            ).first()

        # Create paper if needed
        if paper is None:
            paper = Paper(
                id=str(uuid4()),
                title=title or path.stem,
                abstract="",
                year=None,
                venue="",
                doi=doi,
                arxiv_id=None,
            )
            session.add(paper)
            session.commit()
            session.refresh(paper)

    # Rebuild FTS after ingest (MVP-safe)
    rebuild_fts()

    return {
        "status": "ingested",
        "paper_id": paper.id,
        "title": paper.title,
        "doi": paper.doi,
        "file_path": str(path.resolve()),
        "sha256": file_hash,
    }
