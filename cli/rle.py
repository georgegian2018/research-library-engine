from __future__ import annotations

import typer

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

app = typer.Typer(help="Research Library Engine CLI")


# -------------------------------------------------------------------
# Export commands
# -------------------------------------------------------------------

@app.command("export-bibtex")
def cmd_export_bibtex():
    """Export all papers as BibTeX."""
    print(export_bibtex())


@app.command("export-ieee")
def cmd_export_ieee():
    """Export all papers as IEEE-style references."""
    print(export_ieee())


@app.command("export-markdown")
def cmd_export_markdown():
    """Export all papers as Markdown."""
    print(export_markdown())


@app.command("export-csv")
def cmd_export_csv():
    """Export all papers as CSV."""
    print(export_csv())


# -------------------------------------------------------------------
# Deduplication
# -------------------------------------------------------------------

@app.command("dedup-report")
def cmd_dedup_report(threshold: float = 0.85):
    """Show possible duplicate papers."""
    results = find_possible_duplicates(threshold)
    if not results:
        print("No possible duplicates found.")
        return

    for r in results:
        print(
            f"{r['score']}: "
            f"{r['paper_1_title']}  <->  {r['paper_2_title']}"
        )


# -------------------------------------------------------------------
# Projects
# -------------------------------------------------------------------

@app.command("project-create")
def cmd_project_create(name: str, description: str = ""):
    """Create a new project."""
