from __future__ import annotations
from difflib import SequenceMatcher
from typing import Set

from app.backend.models import Paper
from app.backend.dedup.normalize import normalize_title


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(
        None,
        normalize_title(a),
        normalize_title(b),
    ).ratio()


def author_overlap(p1: Paper, p2: Paper) -> float:
    a1: Set[str] = {a.name.lower() for a in p1.authors}
    a2: Set[str] = {a.name.lower() for a in p2.authors}

    if not a1 or not a2:
        return 0.0

    return len(a1 & a2) / max(len(a1), len(a2))


def dedup_score(p1: Paper, p2: Paper) -> float:
    """
    Weighted similarity score in range [0,1].
    """
    t = title_similarity(p1.title, p2.title)
    a = author_overlap(p1, p2)
    return round((0.7 * t + 0.3 * a), 3)
