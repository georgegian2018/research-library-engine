from __future__ import annotations
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Project, Paper, PaperProject


def create_project(name: str, description: str = "") -> Project:
    with get_session() as session:
        existing = session.exec(
            select(Project).where(Project.name == name)
        ).first()
        if existing:
            raise ValueError("Project already exists")

        project = Project(name=name, description=description)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project


def list_projects():
    with get_session() as session:
        return session.exec(select(Project)).all()


def add_paper_to_project(project_id: int, paper_id: str):
    with get_session() as session:
        project = session.get(Project, project_id)
        paper = session.get(Paper, paper_id)

        if not project or not paper:
            raise ValueError("Project or Paper not found")

        link = session.exec(
            select(PaperProject)
            .where(PaperProject.project_id == project_id)
            .where(PaperProject.paper_id == paper_id)
        ).first()

        if not link:
            session.add(
                PaperProject(project_id=project_id, paper_id=paper_id)
            )
            session.commit()


def list_papers_in_project(project_id: int):
    with get_session() as session:
        project = session.get(Project, project_id)
        if not project:
            raise ValueError("Project not found")
        return project.papers
