from __future__ import annotations

import re


def normalize_title(title: str) -> str:
    """
    Normalize a paper title for similarity comparisons.

    - lowercases
    - removes punctuation/symbols
    - collapses whitespace
    """
    if not title:
        return ""

    t = title.lower()
    t = re.sub(r"[^\w\s]", " ", t)     # replace punctuation with spaces
    t = re.sub(r"\s+", " ", t).strip() # collapse whitespace
    return t
