
from typing import List, Tuple, Optional

# Snapshot biß╗âu diß╗àn danh s├ích c├íc block bß╗Ö nhß╗¢ theo thß╗⌐ tß╗▒ ─æß╗ïa chß╗ë t─âng dß║ºn: (start, size, pid, requested)
Snapshot = List[Tuple[int, int, Optional[str], int]]


def external_fragmentation(snapshot: Snapshot) -> float:
    """T├¡nh to├ín tß╗╖ lß╗ç ph├ón mß║únh ngoß║íi vi dß╗▒a tr├¬n trß║íng th├íi c├íc khoß║úng trß╗æng (holes) trong bß╗Ö nhß╗¢."""
    holes = [b[1] for b in snapshot if b[2] is None]
    if len(holes) <= 1:
        return 0.0
    total_free = sum(holes)
    if total_free == 0:
        return 0.0
    return 1.0 - (max(holes) / total_free)


def internal_fragmentation(snapshot: Snapshot) -> int:
    """T├¡nh to├ín tß╗òng dung l╞░ß╗úng ph├ón mß║únh nß╗Öi vi (phß║ºn dung l╞░ß╗úng cß║Ñp ph├ít d╞░ thß╗½a so vß╗¢i y├¬u cß║ºu thß╗▒c tß║┐ cß╗ºa tiß║┐n tr├¼nh)."""
    total = 0
    for _start, size, pid, requested in snapshot:
        if pid is not None:
            total += size - requested
    return total
