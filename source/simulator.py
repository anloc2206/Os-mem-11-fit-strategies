"""Chạy mô phỏng cấp phát bộ nhớ từ một danh sách yêu cầu (Task 5)."""
import os
import sys

# Cho phép import memory, strategies, metrics dù chạy từ đâu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import metrics
from memory import MemoryManager
from strategies import STRATEGIES


def run_simulation(total, requests, strategy_name):
    """Chạy lần lượt các yêu cầu và trả về list dict, mỗi dict là một dòng trace.

    Đầu vào : total (KB), requests = list (action, pid, size), strategy_name = first_fit/best_fit/worst_fit.
    Đầu ra  : list dict có các khóa theo TRACE_COLUMNS (step bắt đầu từ 1, không có dòng init).
    """
    if strategy_name not in STRATEGIES:
        raise ValueError(f"Chiến lược '{strategy_name}' không tồn tại (chọn: {', '.join(STRATEGIES)})")
    strategy = STRATEGIES[strategy_name]
    manager = MemoryManager(total)

    trace = []
    for step, (action, pid, size) in enumerate(requests, start=1):
        if action == "alloc":
            ok = manager.allocate(pid, size, strategy)
        elif action == "free":
            ok = manager.free(pid)
        else:
            raise ValueError(f"Yêu cầu thứ {step}: action '{action}' không hợp lệ")

        snap = manager.snapshot()
        holes = [b[1] for b in snap if b[2] is None]  # kích thước các lỗ trống
        trace.append({
            "step": step,
            "strategy": strategy_name,
            "action": action,
            "pid": pid,
            "size": size,
            "success": 1 if ok else 0,
            "free_total": sum(holes),
            "largest_hole": max(holes) if holes else 0,
            "external_frag": round(metrics.external_fragmentation(snap), 4),
            "internal_frag": metrics.internal_fragmentation(snap),
        })
    return trace
