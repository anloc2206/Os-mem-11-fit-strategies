
from typing import List, Tuple, Optional


Snapshot = List[Tuple[int, int, Optional[str], int]]


def external_fragmentation(snapshot: Snapshot) -> float:
    
    holes = [b[1] for b in snapshot if b[2] is None]
    if len(holes) <= 1:
        return 0.0
    total_free = sum(holes)
    if total_free == 0:
        return 0.0
    return 1.0 - (max(holes) / total_free)


def internal_fragmentation(snapshot: Snapshot) -> int:
    
    total = 0
    for _start, size, pid, requested in snapshot:
        if pid is not None:
            total += size - requested
    return total