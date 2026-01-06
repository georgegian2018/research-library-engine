from __future__ import annotations

from typing import List
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper


def export_ieee() -> str:
    """
    Export all papers as IEEE-style reference strings.
    """
    lines: List[str] = []

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for idx, p in enumerate(papers, start=1):
            authors = ", ".join(a.name for a in p.authors) if p.authors else "Unknown"

            parts = [
                f"[{idx}] {authors}",
                f"\"{p.title},\"",
            ]

            if p.venue:
                parts.append(p.venue)
            if p.year:
                parts.append(str(p.year))
            if p.doi:
                parts.append(f"doi:{p.doi}")

            line = " ".join(parts) + "."
            lines.append(line)

    return "\n".join(lines)

