
from typing import List, Tuple, Optional

# Snapshot biểu diễn danh sách các block bộ nhớ theo thứ tự địa chỉ tăng dần: (start, size, pid, requested)
Snapshot = List[Tuple[int, int, Optional[str], int]]


def external_fragmentation(snapshot: Snapshot) -> float:
    """Tính toán tỷ lệ phân mảnh ngoại vi dựa trên trạng thái các khoảng trống (holes) trong bộ nhớ."""
    holes = [b[1] for b in snapshot if b[2] is None]
    if len(holes) <= 1:
        return 0.0
    total_free = sum(holes)
    if total_free == 0:
        return 0.0
    return 1.0 - (max(holes) / total_free)


def internal_fragmentation(snapshot: Snapshot) -> int:
    """Tính toán tổng dung lượng phân mảnh nội vi (phần dung lượng cấp phát dư thừa so với yêu cầu thực tế của tiến trình)."""
    total = 0
    for _start, size, pid, requested in snapshot:
        if pid is not None:
            total += size - requested
    return total