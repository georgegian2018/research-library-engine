from app.backend.export.bibtex import export_bibtex

@app.command()
def export_bibtex_cmd():
    """Export all papers as BibTeX."""
    print(export_bibtex())




from app.backend.tags_notes import (
    add_tag_to_paper,
    list_tags_for_paper,
    set_note_for_paper,
    get_note_for_paper,
)

@app.command()
def tag(paper_id: str, tag: str):
    """Add a tag to a paper."""
    add_tag_to_paper(paper_id, tag)
    print(f"[green]Added tag '{tag}' to paper {paper_id}[/green]")


@app.command()
def tags(paper_id: str):
    """List tags for a paper."""
    tags = list_tags_for_paper(paper_id)
    for t in tags:
        print(f"- {t}")


@app.command()
def note(paper_id: str, file: str):
    """Set a Markdown note for a paper from a file."""
    md = Path(file).read_text(encoding="utf-8")
    set_note_for_paper(paper_id, md)
    print("[green]Note saved.[/green]")


@app.command()
def view_note(paper_id: str):
    """View a paper's note."""
    print(get_note_for_paper(paper_id))

from pathlib import Path


from __future__ import annotations

from pathlib import Path
import typer
from rich import print

from app.backend.db import create_tables
from app.backend.fts import ensure_fts, rebuild_fts
from app.backend.ingest import ingest_pdf
from app.backend.search import fts_search

app = typer.Typer(help="Research Library Engine CLI")


@app.command()
def init():
    """
    Initialize the local database and FTS index.
    """
    create_tables()
    ensure_fts()
    rebuild_fts()
    print("[green]Initialized DB + FTS5.[/green]")


@app.command()
def ingest(path: str):
    """
    Ingest a PDF file or all PDFs within a folder (recursive).
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise typer.BadParameter(f"Path not found: {p}")

    create_tables()
    ensure_fts()

    results = []
    if p.is_file():
        results.append(ingest_pdf(p))
    else:
        pdfs = sorted([x for x in p.rglob("*.pdf") if x.is_file()])
        print(f"[cyan]Found {len(pdfs)} PDF(s). Ingesting...[/cyan]")
        for pdf in pdfs:
            try:
                results.append(ingest_pdf(pdf))
            except Exception as e:
                results.append({"status": "error", "path": str(pdf), "error": str(e)})

    # Summary
    ing = sum(1 for r in results if r.get("status") == "ingested")
    skp = sum(1 for r in results if r.get("status") == "skipped")
    err = sum(1 for r in results if r.get("status") == "error")
    print(f"[green]Ingested:[/green] {ing}  [yellow]Skipped:[/yellow] {skp}  [red]Errors:[/red] {err}")

    # Print last few results
    for r in results[-10:]:
        print(r)


@app.command()
def search(q: str, limit: int = 20):
    """
    Full-text search (FTS5) over titles/abstract/doi.
    """
    create_tables()
    ensure_fts()
    rebuild_fts()

    hits = fts_search(q, limit=limit)
    print(f"[cyan]Hits:[/cyan] {len(hits)}")
    for h in hits:
        print(f"- {h.get('title')}  ({h.get('year')})  DOI={h.get('doi')}  rank={h.get('rank')}")


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """
    Run the local FastAPI server.
    """
    import uvicorn
    uvicorn.run("app.backend.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
