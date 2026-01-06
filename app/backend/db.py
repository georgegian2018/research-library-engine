from __future__ import annotations

import os
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine

DEFAULT_DB_PATH = Path("data") / "db.sqlite"


def get_db_path() -> Path:
    db_path = Path(os.environ.get("RLE_DB_PATH", str(DEFAULT_DB_PATH)))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_engine():
    db_path = get_db_path()
    # check_same_thread=False allows FastAPI to use SQLite safely with threadpool
    return create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})


ENGINE = get_engine()


def create_tables():
    SQLModel.metadata.create_all(ENGINE)


def get_session() -> Session:
    return Session(ENGINE)
