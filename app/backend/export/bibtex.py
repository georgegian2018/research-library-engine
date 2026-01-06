from __future__ import annotations

from typing import List
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper


def _bibtex_key(paper: Paper) -> str:
    """
    Generate a stable BibTeX key.
    """
    base = paper.id or "paper"
    return base.replace(":", "_").replace("/", "_")


def export_bibtex() -> str:
    """
    Export all papers as BibTeX entries.
    """
    entries: List[str] = []

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for p in papers:
            key = _bibtex_key(p)

            authors = " and ".join(a.name for a in p.authors) if p.authors else "Unknown"

            fields = {
                "title": p.title,
                "author": authors,
                "year": str(p.year) if p.year else None,
                "journal": p.venue,
                "doi": p.doi,
            }

            body = []
            for k, v in fields.items():
                if v:
                    body.append(f"  {k} = {{{v}}}")

            entry = "@article{{{key},\n{body}\n}}".format(
                key=key,
                body=",\n".join(body),
            )

            entries.append(entry)

    return "\n\n".join(entries)

