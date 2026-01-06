from __future__ import annotations

from typing import List, Dict
from sqlmodel import select

from app.backend.db import get_session
from app.backend.models import Paper
from app.backend.dedup.similarity import dedup_score


def find_possible_duplicates(threshold: float = 0.85) -> List[Dict]:
    """
    Find possible duplicate papers based on similarity score.

    This function is READ-ONLY.
    It does NOT merge or delete anything.
    """
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("Threshold must be between 0 and 1")

    results: List[Dict] = []

    with get_session() as session:
        papers = session.exec(select(Paper)).all()

        count = len(papers)
        for i in range(count):
            for j in range(i + 1, count):
                p1 = papers[i]
                p2 = papers[j]

                # Skip exact DOI matches (already-known duplicates)
                if p1.doi and p2.doi and p1.doi == p2.doi:
                    continue

                score = dedup_score(p1, p2)
                if score >= threshold:
                    results.append(
                        {
                            "paper_1_id": p1.id,
                            "paper_1_title": p1.title,
                            "paper_2_id": p2.id,
                            "paper_2_title": p2.title,
                            "score": score,
                        }
                    )

    return results
