
# Research Library Engine (RLE)

Local-first **Research Library Engine** for **desktop/laptop** use.

RLE is a Calibre-inspired, research-first system focused on:
- **metadata integrity**
- **deduplication**
- **search (FTS5)**
- **exports (BibTeX / RIS / IEEE / Markdown / CSV)**

PDF files are **never modified** (“untouched PDFs”); the engine stores metadata + file paths + hashes.



# Research Library Engine (RLE)

Local-first research library engine for desktop/laptop use.

## Features (MVP)
- PDF ingest (hash-based identity)
- DOI detection (basic regex)
- SQLite database + FTS5 full-text search
- FastAPI local server
- CLI tooling

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -e .
```
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

## Initialize DB
```bash
rle init
```

## Ingest PDFs
```bash
rle ingest ./library
# or a single file
rle ingest ./library/some_paper.pdf
```

## Search
```bash
rle search "MIMO phased array"
```

## Run server
```bash
rle serve
# then open http://127.0.0.1:8000/docs

```

```yaml
---

## 6) Run it (commands)

From the repo root:


python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -e .

rle init
rle ingest ./library
rle search "antenna"
rle serve
```



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

```

## Repository Layout

```text
research-library-engine/
├─ app/
│  ├─ backend/
│  │  ├─ main.py
│  │  ├─ db.py
│  │  ├─ models.py
│  │  ├─ fts.py
│  │  ├─ ingest.py
│  │  └─ search.py
│  └─ frontend/           # (future – web UI)
│
├─ cli/
│  └─ rle.py
│
├─ data/                  # SQLite database (generated)
├─ library/               # PDFs (untouched)
├─ imports/
├─ exports/
├─ docs/
│  └─ architecture.md
│
├─ README.md
├─ LICENSE.md
└─ pyproject.toml
```
