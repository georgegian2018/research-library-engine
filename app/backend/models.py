from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class PaperTag(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    papers: List["Paper"] = Relationship(back_populates="tags", link_model=PaperTag)


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper_id: str = Field(foreign_key="paper.id", index=True)
    content_md: str = Field(default="")
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)



from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class PaperAuthor(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    author_id: str = Field(foreign_key="author.id", primary_key=True)
    author_order: int = Field(default=0, index=True)


class Paper(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str = Field(default="", index=True)
    abstract: str = Field(default="")
    year: Optional[int] = Field(default=None, index=True)
    venue: str = Field(default="")
    doi: Optional[str] = Field(default=None, index=True)
    arxiv_id: Optional[str] = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    authors: List["Author"] = Relationship(back_populates="papers", link_model=PaperAuthor)
    files: List["File"] = Relationship(back_populates="paper")

    __table_args__ = (
        UniqueConstraint("doi", name="uq_paper_doi"),
    )


class Author(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    orcid: Optional[str] = Field(default=None, index=True)

    papers: List[Paper] = Relationship(back_populates="authors", link_model=PaperAuthor)


class File(SQLModel, table=True):
    id: str = Field(primary_key=True)
    paper_id: str = Field(foreign_key="paper.id", index=True)
    path: str = Field(index=True)
    sha256: str = Field(index=True)
    version: int = Field(default=1, index=True)
    added_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    paper: Paper = Relationship(back_populates="files")

    __table_args__ = (
        UniqueConstraint("sha256", name="uq_file_sha256"),
    )
