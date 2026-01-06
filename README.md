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

## Usage examples

```bash
rle tag <PAPER_ID> mimo
rle tags <PAPER_ID>
rle note <PAPER_ID> notes.md
rle view-note <PAPER_ID>
```

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
## Then open:
- API Docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

---

## Repository Structure

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

## 🔗 Reference Collections

See [`/links`](./links) for:

- 🧪 **Research tools and academic repositories**
- 📚 **IEEE / ITU / ETSI standard documents**
- 🔗 **Long-term reference materials**



## 🔗 Linked Repositories

| Repository | Description |
|------------|-------------|
| [`engineering-research-wiki`](https://github.com/georgiosgiannakopoulos/engineering-research-wiki) | Technical deep-dives into RF, signal processing, and many more... |
| [`technical-wiki-hub`](https://github.com/georgiosgiannakopoulos/technical-wiki-hub) | Technical deep-dives into wiki-page-template, linux-and-tools, networking-basics and many more...|
| [`research library engine`](https://github.com/georgiosgiannakopoulos/research-library-engine) | Technical deep-dives into Research tools and academic repositories, with exporting BibTeX / RIS / IEEE / Markdown / CSV |



| Repository | Description |
|------------|-------------|
| [`engineering-research-wiki`](https://github.com/georgiosgiannakopoulos/engineering-research-wiki) | Technical deep-dives into RF, signal processing, and many more... |
| [`technical-wiki-hub`](https://github.com/georgiosgiannakopoulos/technical-wiki-hub) | Technical deep-dives into wiki-page-template, linux-and-tools, networking-basics and many more...|
| [`research library engine`](https://github.com/georgiosgiannakopoulos/research-library-engine) | Technical deep-dives into Research tools and academic repositories, with exporting BibTeX / RIS / IEEE / Markdown / CSV |

More domain-specific wikis will be listed here as they are added.
---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙌 Acknowledgments

Built and maintained by [Georgios Giannakopoulos](https://github.com/georgiosgiannakopoulos).  
Inspired by open knowledge engineering and long-term documentation practices.

