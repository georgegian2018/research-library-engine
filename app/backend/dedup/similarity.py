from __future__ import annotations

from difflib import SequenceMatcher
from typing import Set

from app.backend.models import Paper
from app.backend.dedup.normalize import normalize_title


# -------------------------------------------------------------------
# Title similarity
# -------------------------------------------------------------------

def title_similarity(title_a: str, title_b: str) -> float:
    """
    Compute normalized title similarity in range [0, 1].
    """
    if not title_a or not title_b:
        return 0.0

    a = normalize_title(title_a)
    b = normalize_title(title_b)

    return SequenceMatcher(None, a, b).ratio()


# -------------------------------------------------------------------
# Author overlap
# -------------------------------------------------------------------

def author_overlap(p1: Paper, p2: Paper) -> float:
    """
    Compute author overlap score in range [0, 1].
    """
    authors_1: Set[str] = {a.name.lower() for a in p1.authors}
    authors_2: Set[str] = {a.name.lower() for a in p2.authors}

    if not authors_1 or not authors_2:
        return 0.0

    intersection = authors_1 & authors_2
    return len(intersection) / max(len(authors_1), len(authors_2))


# -------------------------------------------------------------------
# Combined score
# -------------------------------------------------------------------

def dedup_score(p1: Paper, p2: Paper) -> float:
    """
    Weighted deduplication score in range [0, 1].

    Title similarity: 70%
    Author overlap:   30%
    """
    t_score = title_similarity(p1.title, p2.title)
    a_score = author_overlap(p1, p2)

    return round((0.7 * t_score + 0.3 * a_score), 3)
