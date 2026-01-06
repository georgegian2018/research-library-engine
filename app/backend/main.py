from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import select

from app.backend.db import init_db, get_session
from app.backend.models import (
    Paper,
    Tag,
    Note,
    Project,
)
from app.backend.export import (
    export_bibtex,
    export_ieee,
    export_markdown,
    export_csv,
)
from app.backend.dedup import find_possible_duplicates
from app.backend.projects import (
    create_project,
    list_projects,
    add_paper_to_project,
    list_papers_in_project,
)
from app.backend.tags_notes import (
    add_tag_to_paper,
    list_tags_for_paper,
    set_note_for_paper,
    get_note_for_paper,
)


# -------------------------------------------------------------------
# App
# -------------------------------------------------------------------

app = FastAPI(title="Research Library Engine")


# -------------------------------------------------------------------
# Startup
# -------------------------------------------------------------------

@app.on_event("startup")
def on_startup() -> None:
    init_db()


# -------------------------------------------------------------------
# Health
# -------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------------------------------------------
# Papers
# -------------------------------------------------------------------

@app.get("/papers")
def list_papers(limit: int = 100, offset: int = 0) -> List[Paper]:
    with get_session() as session:
        return session.exec(
            select(Paper).offset(offset).limit(limit)
        ).all()


# -------------------------------------------------------------------
# Search (simple metadata search placeholder)
# -------------------------------------------------------------------

@app.get("/search")
def search_papers(q: str, limit: int = 50):
    with get_session() as session:
        stmt = select(Paper).where(Paper.title.contains(q))
        return session.exec(stmt.limit(limit)).all()


# -------------------------------------------------------------------
# Tags
# -------------------------------------------------------------------

@app.post("/papers/{paper_id}/tags")
def api_add_tag(paper_id: str, tag: str):
    add_tag_to_paper(paper_id, tag)
    return {"status": "ok"}


@app.get("/papers/{paper_id}/tags")
def api_list_tags(paper_id: str):
    return list_tags_for_paper(paper_id)


# -------------------------------------------------------------------
# Notes
# -------------------------------------------------------------------

@app.post("/papers/{paper_id}/note")
def api_set_note(paper_id: str, content_md: str):
    set_note_for_paper(paper_id, content_md)
    return {"status": "ok"}


@app.get("/papers/{paper_id}/note")
def api_get_note(paper_id: str):
    return {"content_md": get_note_for_paper(paper_id)}


# -------------------------------------------------------------------
# Projects
# -------------------------------------------------------------------

@app.post("/projects")
def api_create_project(name: str, description: str = ""):
    try:
        return create_project(name, description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/projects")
def api_list_projects():
    return list_projects()


@app.post("/projects/{project_id}/papers/{paper_id}")
def api_add_paper_to_project(project_id: int, paper_id: str):
    add_paper_to_project(project_id, paper_id)
    return {"status": "ok"}


@app.get("/projects/{project_id}/papers")
def api_list_papers_in_project(project_id: int):
    return list_papers_in_project(project_id)


# -------------------------------------------------------------------
# Deduplication
# -------------------------------------------------------------------

@app.get("/dedup/report")
def api_dedup_report(threshold: float = 0.85):
    return find_possible_duplicates(threshold)


# -------------------------------------------------------------------
# Exports
# -------------------------------------------------------------------

@app.get("/export/bibtex")
def api_export_bibtex():
    return {"bibtex": export_bibtex()}


@app.get("/export/ieee")
def api_export_ieee():
    return {"ieee": export_ieee()}


@app.get("/export/markdown")
def api_export_markdown():
    return {"markdown": export_markdown()}


@app.get("/export/csv")
def api_export_csv():
    return {"csv": export_csv()}


# -------------------------------------------------------------------
# Frontend UI
# -------------------------------------------------------------------

frontend_dir = Path(__file__).resolve().parents[2] / "app" / "frontend"
if frontend_dir.exists():
    app.mount(
        "/ui",
        StaticFiles(directory=str(frontend_dir), html=True),
        name="ui",
    )
