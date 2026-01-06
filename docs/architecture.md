# Research Library Engine – Architecture

This document describes the high-level architecture of the Research Library Engine (RLE).

## Core Principles
- Local-first
- PDFs are never modified
- Metadata-driven
- Reproducible research workflows

## Components
- Backend: FastAPI + SQLite (FTS5)
- CLI: Typer-based command interface
- Frontend: Planned (table-driven Web UI)

## Data Storage
- SQLite database stored in `data/`
- PDFs referenced by path from `library/`
