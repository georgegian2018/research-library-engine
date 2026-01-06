from __future__ import annotations
import re


def normalize_title(title: str) -> str:
    """
    Normalize a paper title for comparison.
    """
    if not title:
        return ""

    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title
