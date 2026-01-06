from __future__ import annotations

from typing import List, Optional
from sqlmodel import text
from app.backend.db import ENGINE


def fts_search(query: str, limit: int = 50) -> List[dict]:
    """
    Full-text search across title/abstract/doi using SQLite FTS5.
    """
    sql = text(
        """
        SELECT
          p.id, p.title, p.doi, p.year, p.venue,
          bm25(paper_fts) AS rank
        FROM paper_fts
        JOIN paper p ON p.id = paper_fts.paper_id
        WHERE paper_fts MATCH :q
        ORDER BY rank
        LIMIT :limit;
        """
    )
    with ENGINE.connect() as conn:
        rows = conn.execute(sql, {"q": query, "limit": limit}).mappings().all()
        return [dict(r) for r in rows]


def list_papers(limit: int = 100, offset: int = 0, year: Optional[int] = None) -> List[dict]:
    base = "SELECT id, title, doi, year, venue, created_at FROM paper"
    params = {"limit": limit, "offset": offset}
    if year is not None:
        base += " WHERE year = :year"
        params["year"] = year
    base += " ORDER BY created_at DESC LIMIT :limit OFFSET :offset;"
    with ENGINE.connect() as conn:
        rows = conn.execute(text(base), params).mappings().all()
        return [dict(r) for r in rows]
