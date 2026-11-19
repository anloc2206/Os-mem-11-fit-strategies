
"""Tạo workload dùng chung cho các chiến lược cấp phát bộ nhớ."""
import random


def generate(n, seed, total_size, max_size):
    """Sinh n thao tác alloc/free có thể tái lập bằng seed."""
    rng = random.Random(seed)
    operations = []
    active_pids = []
    next_pid = 1

    for _ in range(n):
        if active_pids and rng.random() < 0.30:
            index = rng.randrange(len(active_pids))
            pid = active_pids.pop(index)
            operations.append(("free", pid, 0))
        else:
            pid = f"P{next_pid}"
            next_pid += 1
            size = rng.randint(20, max(20, min(max_size, total_size)))
            operations.append(("alloc", pid, size))
            active_pids.append(pid)

    return operations
