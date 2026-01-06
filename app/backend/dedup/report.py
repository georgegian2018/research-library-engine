from __future__ import annotations
from typing import List, Dict
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper
from app.backend.dedup.similarity import dedup_score


def find_possible_duplicates(threshold: float = 0.85) -> List[Dict]:
    """
    Return pairs of papers with similarity score >= threshold.
    """
    results: List[Dict] = []

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                p1 = papers[i]
                p2 = papers[j]

                # Skip if DOI already matches (already known duplicate)
                if p1.doi and p2.doi and p1.doi == p2.doi:
                    continue

                score = dedup_score(p1, p2)
                if score >= threshold:
                    results.append({
                        "paper_1_id": p1.id,
                        "paper_1_title": p1.title,
                        "paper_2_id": p2.id,
                        "paper_2_title": p2.title,
                        "score": score,
                    })

    return results
