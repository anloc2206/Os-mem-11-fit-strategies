
from typing import List, Optional


def first_fit(holes: List[int], size: int) -> Optional[int]:
    """Select the first hole large enough for the process."""
    for i, h in enumerate(holes):
        if h >= size:
            return i
    return None


def best_fit(holes: List[int], size: int) -> Optional[int]:
    """Select the smallest hole that can fit the process."""
    best_idx: Optional[int] = None
    best_size: Optional[int] = None

    for i, h in enumerate(holes):
        if h >= size and (best_size is None or h < best_size):
            best_size = h
            best_idx = i

    return best_idx


def worst_fit(holes: List[int], size: int) -> Optional[int]:
    """Select the largest hole that can fit the process."""
    worst_idx: Optional[int] = None
    worst_size = -1

    for i, h in enumerate(holes):
        if h >= size and h > worst_size:
            worst_size = h
            worst_idx = i

    return worst_idx


STRATEGIES = {
    "first_fit": first_fit,
    "best_fit": best_fit,
    "worst_fit": worst_fit,
}
