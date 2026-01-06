from __future__ import annotations
from datetime import datetime
from sqlmodel import select
from app.backend.db import get_session
from app.backend.models import Paper, Tag, PaperTag, Note


def add_tag_to_paper(paper_id: str, tag_name: str):
    tag_name = tag_name.strip().lower()
    with get_session() as session:
        paper = session.get(Paper, paper_id)
        if not paper:
            raise ValueError("Paper not found")

        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)

        link = session.exec(
            select(PaperTag)
            .where(PaperTag.paper_id == paper_id)
            .where(PaperTag.tag_id == tag.id)
        ).first()

        if not link:
            session.add(PaperTag(paper_id=paper_id, tag_id=tag.id))
            session.commit()


def list_tags_for_paper(paper_id: str):
    with get_session() as session:
        paper = session.get(Paper, paper_id)
        if not paper:
            raise ValueError("Paper not found")
        return [t.name for t in paper.tags]


def set_note_for_paper(paper_id: str, markdown: str):
    with get_session() as session:
        note = session.exec(
            select(Note).where(Note.paper_id == paper_id)
        ).first()

        if not note:
            note = Note(paper_id=paper_id, content_md=markdown)
            session.add(note)
        else:
            note.content_md = markdown
            note.updated_at = datetime.utcnow()

        session.commit()


def get_note_for_paper(paper_id: str) -> str:
    with get_session() as session:
        note = session.exec(
            select(Note).where(Note.paper_id == paper_id)
        ).first()
        return note.content_md if note else ""
