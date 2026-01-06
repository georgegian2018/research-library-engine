
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
├─ cli/
├─ data/       # SQLite database lives here (default)
├─ library/    # Your PDFs (optional; can point to any folder)
├─ imports/
├─ exports/
└─ README.md
