
# Research Library Engine (RLE)

Local-first **Research Library Engine** for **desktop/laptop** use.

RLE is a Calibre-inspired, research-first system focused on:
- **metadata integrity**
- **deduplication**
- **search (FTS5)**
- **exports (BibTeX / RIS / IEEE / Markdown / CSV)**

PDF files are **never modified** (“untouched PDFs”); the engine stores metadata + file paths + hashes.

---

## Core Stack (MVP)
**Backend**
- Python + FastAPI
- SQLite (FTS5 enabled)
- SQLModel / SQLAlchemy
- File-based storage (PDFs untouched)

**CLI**
- `rle init`, `rle ingest`, `rle search`, `rle serve`

---

## Repository Layout

```text
research-library-engine/
├─ app/
│  ├─ backend/
│  │  ├─ __init__.py
│  │  ├─ main.py          # FastAPI app
│  │  ├─ db.py            # SQLite engine + sessions
│  │  ├─ models.py        # SQLModel ORM
│  │  ├─ fts.py           # FTS5 setup & rebuild
│  │  ├─ ingest.py        # PDF ingest + hashing + DOI detection
│  │  └─ search.py        # Search services
│  └─ frontend/           # (future – web UI)
│
├─ cli/
│  ├─ __init__.py
│  └─ rle.py              # CLI entry point
│
├─ data/
│  ├─ db.sqlite           # SQLite DB (generated)
│  └─ .gitkeep
│
├─ library/
│  └─ .gitkeep            # Your PDFs live here (optional)
│
├─ imports/
│  └─ .gitkeep
│
├─ exports/
│  └─ .gitkeep
│
├─ docs/
│  └─ architecture.md     # (optional, future)
│
├─ README.md
├─ LICENSE.md
├─ pyproject.toml
└─ .gitignore

