# Research Library Engine (RLE)


![Format](https://img.shields.io/badge/Format-Markdown-blue.svg)
![Templates](https://img.shields.io/badge/Templates-Available-brightgreen)
![Status](https://img.shields.io/badge/Status-Active%20Development-blue)
![LaTeX](https://img.shields.io/badge/LaTeX-Compatible-green?style=flat-square)
![Focus](https://img.shields.io/badge/Focus-Documentation%20Hub-purple)
![Research](https://img.shields.io/badge/Focus-Engineering%20Research-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellowgreen)



Local-first **Research Library Engine** for **desktop/laptop** use.

RLE is a Calibre-inspired, research-first system focused on:
- **metadata integrity**
- **deduplication**
- **search (SQLite FTS5)**
- **exports (BibTeX / RIS / IEEE / Markdown / CSV)**

PDF files are **never modified** (“untouched PDFs”); the engine stores metadata, file paths, and hashes only.

---

## Features (MVP)
- PDF ingest (hash-based identity)
- DOI detection (basic regex)
- SQLite database with FTS5 full-text search
- FastAPI local server
- CLI tooling

---

## Core Stack (MVP)

**Backend**
- Python + FastAPI
- SQLite (FTS5 enabled)
- SQLModel / SQLAlchemy
- File-based storage (PDFs untouched)

**CLI**
- `rle init`
- `rle ingest`
- `rle search`
- `rle serve`

---

## Setup

```bash
python -m venv .venv
# Windows:
# .venv\Scripts\activate
source .venv/bin/activate

pip install -e .
```
---


## Initialize DB

```bash
rle init
```

## Ingest PDFs
Ingest a folder recursively:
```bash
rle ingest ./library
```
Or ingest a single PDF:
```bash
# or a single file
rle ingest ./library/some_paper.pdf
```

## Search
```bash
rle search "MIMO phased array"
```

## Run Local Server
```bash
rle serve
```
# Then open:
- API Docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

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
├─ data/                  # SQLite database (generated)
├─ library/               # PDFs (untouched)
├─ imports/
├─ exports/
├─ docs/
│  └─ architecture.md
│
├─ README.md
├─ LICENSE.md
├─ pyproject.toml
└─ .gitignore

```


