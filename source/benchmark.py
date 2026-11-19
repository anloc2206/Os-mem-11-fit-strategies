"""Benchmark so sánh hiệu năng First-Fit, Best-Fit và Worst-Fit.

Chạy từ thư mục gốc dự án:
    python -m source.benchmark

Kết quả được ghi vào output/benchmark.csv.
"""
from __future__ import annotations

import csv
import os
import random
import time
from statistics import mean

try:
    from source.memory import MemoryManager
    from source.strategies import STRATEGIES
except ModuleNotFoundError:
    # Hỗ trợ chạy trực tiếp khi thư mục source là working directory.
    from memory import MemoryManager
    from strategies import STRATEGIES


TOTAL_MEMORY = 10_000
NUMBER_OF_OPERATIONS = 2_000
REPEATS = 5
RANDOM_SEED = 42


def create_workload(number_of_operations: int, seed: int = RANDOM_SEED):
    """Tạo workload cố định để cả ba chiến lược được kiểm tra công bằng."""
    rng = random.Random(seed)
    operations = []
    active_pids = []
    next_pid = 1

    for _ in range(number_of_operations):
        # Thu hồi ngẫu nhiên khi đang có tiến trình; nếu không thì cấp phát.
        if active_pids and rng.random() < 0.30:
            index = rng.randrange(len(active_pids))
            pid = active_pids.pop(index)
            operations.append(("free", pid, 0))
        else:
            pid = f"P{next_pid}"
            next_pid += 1
            size = rng.randint(20, 500)
            operations.append(("alloc", pid, size))
            active_pids.append(pid)

    return operations


def fragmentation(snapshot):
    """Trả về (phân mảnh ngoài, phân mảnh trong) từ memory snapshot."""
    holes = [block[1] for block in snapshot if block[2] is None]
    free_total = sum(holes)
    external = 0.0 if len(holes) <= 1 or free_total == 0 else 1 - max(holes) / free_total
    internal = sum(size - requested for _start, size, pid, requested in snapshot if pid is not None)
    return external, internal


def run_once(strategy_name, workload):
    manager = MemoryManager(TOTAL_MEMORY)
    strategy = STRATEGIES[strategy_name]
    successes = 0
    allocation_count = 0

    start_time = time.perf_counter()
    for action, pid, size in workload:
        if action == "alloc":
            allocation_count += 1
            if manager.allocate(pid, size, strategy):
                successes += 1
        elif action == "free":
            manager.free(pid)
    elapsed = time.perf_counter() - start_time

    snapshot = manager.snapshot()
    external, internal = fragmentation(snapshot)
    return {
        "strategy": strategy_name,
        "elapsed_seconds": elapsed,
        "allocation_success": successes,
        "allocation_total": allocation_count,
        "success_rate_percent": (successes / allocation_count * 100) if allocation_count else 0.0,
        "external_fragmentation": external,
        "internal_fragmentation_kb": internal,
    }


def run_benchmark(repeats=REPEATS, number_of_operations=NUMBER_OF_OPERATIONS):
    workload = create_workload(number_of_operations)
    results = []

    for strategy_name in STRATEGIES:
        runs = [run_once(strategy_name, workload) for _ in range(repeats)]
        results.append({
            "strategy": strategy_name,
            "average_time_seconds": mean(row["elapsed_seconds"] for row in runs),
            "average_success_rate_percent": mean(row["success_rate_percent"] for row in runs),
            "average_external_fragmentation": mean(row["external_fragmentation"] for row in runs),
            "average_internal_fragmentation_kb": mean(row["internal_fragmentation_kb"] for row in runs),
            "repeats": repeats,
            "operations": number_of_operations,
        })

    return results


def save_csv(results, output_path=None):
    if output_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(project_root, "output", "benchmark.csv")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fieldnames = list(results[0].keys()) if results else []
    with open(output_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(results)
    return output_path


def main():
    results = run_benchmark()
    output_path = save_csv(results)

    print("KET QUA BENCHMARK")
    print("-" * 92)
    print(f"{'Chien luoc':<14}{'Thoi gian (s)':>16}{'Ty le cap phat (%)':>22}{'Phan manh ngoai':>20}")
    for row in results:
        print(
            f"{row['strategy']:<14}"
            f"{row['average_time_seconds']:>16.6f}"
            f"{row['average_success_rate_percent']:>22.2f}"
            f"{row['average_external_fragmentation']:>20.4f}"
        )
    print(f"\nDa luu ket qua tai: {output_path}")


if __name__ == "__main__":
    main()
