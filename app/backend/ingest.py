from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

import fitz  # PyMuPDF
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper, File
from app.backend.fts import rebuild_fts

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def extract_pdf_text_first_pages(path: Path, max_pages: int = 2, max_chars: int = 20000) -> str:
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
    Returns (title, author) from PDF metadata when present.
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


def ingest_pdf(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(str(path))
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Only PDF supported for MVP. Got: {path.name}")

    file_hash = sha256_file(path)

    with get_session() as session:
        # 1) Exact hash dedup
        existing_file = session.exec(select(File).where(File.sha256 == file_hash)).first()
        if existing_file:
            return {
                "status": "skipped",
                "reason": "duplicate_file_hash",
                "file_id": existing_file.id,
                "paper_id": existing_file.paper_id,
                "path": existing_file.path,
            }

        # 2) Extract metadata + DOI
        title, author = extract_pdf_metadata(path)
        text = extract_pdf_text_first_pages(path)
        doi = detect_doi(text)

        # 3) DOI dedup (paper-level)
        paper: Optional[Paper] = None
        if doi:
            paper = session.exec(select(Paper).where(Paper.doi == doi)).first()

        # 4) Create paper if needed
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

        # 5) Add file as a version
        # version = count existing files for paper + 1
        existing_versions = session.exec(select(File).where(File.paper_id == paper.id)).all()
        version = len(existing_versions) + 1

        f = File(
            id=str(uuid4()),
            paper_id=paper.id,
            path=str(path.resolve()),
            sha256=file_hash,
            version=version,
        )
        session.add(f)
        session.commit()

    # Rebuild FTS after ingest (MVP-simple). Later: incremental updates.
    rebuild_fts()

    return {
        "status": "ingested",
        "paper_id": paper.id,
        "title": paper.title,
        "doi": paper.doi,
        "file_path": str(path.resolve()),
        "sha256": file_hash,
        "version": version,
    }
