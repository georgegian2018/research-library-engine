from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine


# -------------------------------------------------------------------
# Database location (local-first)
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "db.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH}"


# -------------------------------------------------------------------
# Engine
# -------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


# -------------------------------------------------------------------
# Session management
# -------------------------------------------------------------------

@contextmanager
def get_session() -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.
    """
    with Session(engine) as session:
        yield session


# -------------------------------------------------------------------
# Initialization
# -------------------------------------------------------------------

def init_db() -> None:
    """
    Create database tables.
    """
    SQLModel.metadata.create_all(engine)
