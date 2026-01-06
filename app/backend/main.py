from app.backend.export.bibtex import export_bibtex



from app.backend.tags_notes import (
    add_tag_to_paper,
    list_tags_for_paper,
    set_note_for_paper,
    get_note_for_paper,
)


from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File as UploadFileType, Query
from fastapi.middleware.cors import CORSMiddleware

from app.backend.db import create_tables
from app.backend.fts import ensure_fts, rebuild_fts
from app.backend.ingest import ingest_pdf
from app.backend.search import fts_search, list_papers


app = FastAPI(title="Research Library Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local-first MVP; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    create_tables()
    ensure_fts()
    rebuild_fts()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/papers")
def papers(limit: int = 100, offset: int = 0, year: Optional[int] = None):
    return list_papers(limit=limit, offset=offset, year=year)


@app.get("/search")
def search(q: str = Query(min_length=1), limit: int = 50):
    return fts_search(query=q, limit=limit)


@app.post("/ingest")
async def ingest_upload(file: UploadFile = UploadFileType(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"status": "error", "reason": "only_pdf_supported_mvp"}

    temp_dir = Path("imports") / "uploads"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / file.filename

    content = await file.read()
    temp_path.write_bytes(content)

    result = ingest_pdf(temp_path)
    return result




@app.post("/papers/{paper_id}/tags")
def api_add_tag(paper_id: str, tag: str):
    add_tag_to_paper(paper_id, tag)
    return {"status": "ok", "paper_id": paper_id, "tag": tag}


@app.get("/papers/{paper_id}/tags")
def api_list_tags(paper_id: str):
    return list_tags_for_paper(paper_id)


@app.post("/papers/{paper_id}/note")
def api_set_note(paper_id: str, content_md: str):
    set_note_for_paper(paper_id, content_md)
    return {"status": "ok"}


@app.get("/papers/{paper_id}/note")
def api_get_note(paper_id: str):
    return {"content_md": get_note_for_paper(paper_id)}



@app.get("/export/bibtex")
def api_export_bibtex():
    return {"bibtex": export_bibtex()}

