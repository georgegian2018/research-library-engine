from __future__ import annotations
from typing import List
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper, Author


def _bibtex_key(paper: Paper) -> str:
    """
    Generate a stable BibTeX key.
    Example: Smith2024MIMO
    """
    author = "unknown"
    if paper.authors:
        author = paper.authors[0].name.split()[-1]

    year = paper.year or "xxxx"
    title_word = paper.title.split()[0] if paper.title else "paper"

    return f"{author}{year}{title_word}"


def export_bibtex() -> str:
    """
    Export all papers as a BibTeX string.
    """
    entries: List[str] = []

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for p in papers:
            key = _bibtex_key(p)
            authors = " and ".join(a.name for a in p.authors) if p.authors else ""

            entry = [
                f"@article{{{key},",
                f"  title={{ {p.title} }},",
                f"  author={{ {authors} }},",
            ]

            if p.venue:
                entry.append(f"  journal={{ {p.venue} }},")
            if p.year:
                entry.append(f"  year={{ {p.year} }},")
            if p.doi:
                entry.append(f"  doi={{ {p.doi} }},")
            entry.append("}")

            entries.append("\n".join(entry))

    return "\n\n".join(entries)

