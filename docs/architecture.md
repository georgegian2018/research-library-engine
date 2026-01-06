# Research Library Engine (RLE) — Architecture

## 1. Purpose

The Research Library Engine (RLE) is a **local-first, researcher-controlled system**
for managing academic papers, metadata, notes, projects, and exports.

The design prioritizes:

- Transparency
- Data ownership
- Deterministic behavior
- Separation of code and data
- Auditability over automation

RLE is not a reference manager clone.  
It is a **research infrastructure layer**.

---

## 2. Core Design Principles

### 2.1 Local-first
- All data lives locally
- No cloud dependency
- No vendor lock-in

### 2.2 PDFs are immutable
- PDF files are never modified
- Metadata and annotations live in the database
- File paths are referenced, not embedded

### 2.3 Explicit over implicit
- No background magic
- No hidden merges
- No automatic destructive operations

### 2.4 Code ≠ Data
- Python code lives under `app/`
- Research data lives at the repository root

---

## 3. High-Level Architecture

```text
┌──────────────────────────────┐
│ Frontend UI │
│ (HTML + CSS + JS, tables) │
└──────────────┬───────────────┘
│ HTTP (JSON)
┌──────────────▼───────────────┐
│ FastAPI API │
│ app/backend/main.py │
└──────────────┬───────────────┘
│
┌──────────────▼───────────────┐
│ Backend Services │
│ ingest / search / dedup / │
│ export / projects / tags │
└──────────────┬───────────────┘
│
┌──────────────▼───────────────┐
│ SQLite Database │
│ data/db.sqlite + FTS5 │
└──────────────────────────────┘

```

---

## 4. Repository Structure

```text
research-library-engine/
├─ app/
│ ├─ backend/ # Python backend (FastAPI)
│ │ ├─ db.py # DB engine & session
│ │ ├─ models.py # Canonical data model
│ │ ├─ main.py # API entry point
│ │ ├─ ingest.py # PDF ingestion
│ │ ├─ search.py # Metadata & FTS search
│ │ ├─ fts.py # SQLite FTS5 support
│ │ ├─ tags_notes.py # Tags & Markdown notes
│ │ ├─ projects.py # Project linking
│ │ ├─ dedup/ # Deduplication logic
│ │ └─ export/ # Export generators
│ └─ frontend/ # Static table-based UI
│
├─ cli/ # CLI interface (Typer)
│
├─ data/ # SQLite database
├─ library/ # PDFs (untouched)
├─ imports/ # Incoming files
├─ exports/ # Generated outputs (BibTeX, CSV, MD)
├─ docs/ # Documentation
│ └─ architecture.md

```

---

## 5. Data Model (Conceptual)

### 5.1 Paper (core entity)

- `id` (UUID)
- `title`
- `abstract`
- `year`
- `venue`
- `doi`
- `arxiv_id`
- `created_at`

### 5.2 Relationships

- Paper ↔ Author (many-to-many)
- Paper ↔ Tag (many-to-many)
- Paper ↔ Project (many-to-many)
- Paper ↔ Note (one-to-many)

All relationships are **explicit link tables**.

---

## 6. Ingestion Flow (MVP)

1. PDF placed in `library/`
2. `ingest_pdf()` is called
3. SHA-256 hash is computed
4. Metadata extracted (PDF metadata + text)
5. DOI detected (if present)
6. Paper created or reused (DOI dedup)
7. FTS index rebuilt

No file data is modified.

---

## 7. Search Architecture

### 7.1 Metadata search
- SQLModel queries on Paper fields

### 7.2 Full-text search (FTS5)
- SQLite virtual table `paper_fts`
- Manual rebuild (MVP-safe)
- BM25 ranking

FTS is **opt-in**, explicit, and transparent.

---

## 8. Deduplication Strategy

Deduplication is **non-destructive**.

Signals used:
- Title similarity (normalized)
- Author overlap
- DOI equality (exact)

Output:
- Ranked list of *possible* duplicates
- No automatic merging

Human judgment remains in control.

---

## 9. Export Architecture

Export code lives in:



app/backend/export/


Supported formats:
- BibTeX
- IEEE-style text
- Markdown
- CSV

Generated files are written to:


exports/


Exports are **pure functions**:
- No file I/O
- Return text only

---

## 10. CLI Architecture

The CLI mirrors backend functionality:

- Exports
- Dedup reports
- Project management
- Tags & notes

CLI is:
- deterministic
- scriptable
- safe by default

---

## 11. Frontend Philosophy

- Table-driven UI
- No “library shelves”
- No visual metaphors
- Optimized for scanning, filtering, auditing

Frontend is intentionally simple:
- HTML + CSS + JS
- Served by FastAPI at `/ui`

---

## 12. Non-Goals (Explicit)

RLE intentionally does NOT:
- Sync to cloud services
- Modify PDFs
- Auto-merge records
- Hide logic behind AI decisions

---

## 13. Future Extensions

- Incremental FTS updates
- File version tracking
- Citation graphs
- Batch folder ingest
- Plugin-based exporters

All extensions must respect:
- local-first
- explicit control
- data ownership

---

## 14. Summary

The Research Library Engine is a **stable, auditable foundation**
for serious research workflows.

It is designed to grow **without architectural debt**.



