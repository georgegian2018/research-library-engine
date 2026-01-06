from __future__ import annotations

from typing import List
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper


def export_markdown() -> str:
    """
    Export all papers as a Markdown document.
    """
    lines: List[str] = []
    lines.append("# Research Library\n")

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for p in papers:
            title = p.title or "(untitled)"
            line = f"- **{title}**"

            meta_parts: List[str] = []
            if p.year:
                meta_parts.append(str(p.year))
            if p.venue:
                meta_parts.append(p.venue)
            if p.doi:
                meta_parts.append(f"DOI: `{p.doi}`")

            if meta_parts:
                line += " — " + " • ".join(meta_parts)

            lines.append(line)

    return "\n".join(lines) + "\n"

