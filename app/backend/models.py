from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlmodel import SQLModel, Field


# -------------------------------------------------------------------
# Core entities
# -------------------------------------------------------------------

class Paper(SQLModel, table=True):
    """
    Canonical paper record.
    """

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    title: str
    abstract: str = ""
    year: Optional[int] = None
    venue: str = ""
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    authors: List["Author"] = Relationship(
        back_populates="papers",
        link_model="PaperAuthor",
    )

    tags: List["Tag"] = Relationship(
        back_populates="papers",
        link_model="PaperTag",
    )

    projects: List["Project"] = Relationship(
        back_populates="papers",
        link_model="PaperProject",
    )

    notes: List["Note"] = Relationship(back_populates="paper")


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    orcid: Optional[str] = Field(default=None, index=True)

    papers: List[Paper] = Relationship(
        back_populates="authors",
        link_model="PaperAuthor",
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    papers: List[Paper] = Relationship(
        back_populates="tags",
        link_model="PaperTag",
    )


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    papers: List[Paper] = Relationship(
        back_populates="projects",
        link_model="PaperProject",
    )


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper_id: str = Field(foreign_key="paper.id", index=True)
    content_md: str = Field(default="")
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    paper: Optional[Paper] = Relationship(back_populates="notes")


# -------------------------------------------------------------------
# Link tables (many-to-many)
# -------------------------------------------------------------------

class PaperAuthor(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    author_id: int = Field(foreign_key="author.id", primary_key=True)


class PaperTag(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class PaperProject(SQLModel, table=True):
    paper_id: str = Field(foreign_key="paper.id", primary_key=True)
    project_id: int = Field(foreign_key="project.id", primary_key=True)
