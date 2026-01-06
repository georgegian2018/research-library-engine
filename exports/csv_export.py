from __future__ import annotations
import csv
import io
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper


def export_csv() -> str:
    """
    Export all papers as CSV.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["title", "authors", "year", "venue", "doi"])

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for p in papers:
            authors = "; ".join(a.name for a in p.authors) if p.authors else ""
            writer.writerow([
                p.title,
                authors,
                p.year or "",
                p.venue or "",
                p.doi or "",
            ])

    return output.getvalue()

