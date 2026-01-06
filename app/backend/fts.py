from __future__ import annotations

from sqlmodel import text
from app.backend.db import ENGINE


FTS_SCHEMA_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS paper_fts
USING fts5(
  paper_id UNINDEXED,
  title,
  abstract,
  doi,
  content='',
  tokenize='unicode61'
);

-- Keep FTS in sync with the Paper table (manual sync via code for MVP).
"""


def ensure_fts():
    with ENGINE.connect() as conn:
        conn.execute(text(FTS_SCHEMA_SQL))
        conn.commit()


def rebuild_fts():
    """
    Rebuild FTS from Paper table. MVP approach: simple and reliable.
    """
    with ENGINE.connect() as conn:
        conn.execute(text("DELETE FROM paper_fts;"))
        conn.execute(
            text(
                """
                INSERT INTO paper_fts(paper_id, title, abstract, doi)
                SELECT id, title, abstract, COALESCE(doi, '') FROM paper;
                """
            )
        )
        conn.commit()
