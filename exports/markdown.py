from __future__ import annotations
from typing import List
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper


def export_markdown() -> str:
    """
    Export papers as Markdown list.
    """
    lines: List[str] = ["# Research Library\n"]

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for p in papers:
            line = f"- **{p.title}**"
            if p.year:
                line += f" ({p.year})"
            if p.doi:
                line += f" — DOI: `{p.doi}`"
            lines.append(line)

    return "\n".join(lines)

