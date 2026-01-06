from __future__ import annotations

from sqlmodel import text

from app.backend.db import engine


# -------------------------------------------------------------------
# FTS5 schema (SQLite)
# -------------------------------------------------------------------

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
"""


# -------------------------------------------------------------------
# FTS helpers
# -------------------------------------------------------------------

def ensure_fts() -> None:
    """
    Ensure the FTS virtual table exists.
    Safe to call multiple times.
    """
    with engine.connect() as conn:
        conn.execute(text(FTS_SCHEMA_SQL))
        conn.commit()


def rebuild_fts() -> None:
    """
    Rebuild FTS index from the Paper table.

    MVP strategy:
    - clear index
    - reinsert all papers
    """
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM paper_fts;"))
        conn.execute(
            text(
                """
                INSERT INTO paper_fts(paper_id, title, abstract, doi)
                SELECT
                    id,
                    title,
                    COALESCE(abstract, ''),
                    COALESCE(doi, '')
                FROM paper;
                """
            )
        )
        conn.commit()
