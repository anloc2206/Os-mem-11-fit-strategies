"""Stress test và benchmark hiệu năng 3 chiến lược First-Fit, Best-Fit, Worst-Fit.

Cách chạy:
    python source/benchmark.py
Kết quả xuất ra:
    output/benchmark.csv
"""
import csv
import os
import platform
import random
import statistics
import sys
import time
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SOURCE_DIR.parent
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from memory import MemoryManager
import metrics
from strategies import STRATEGIES

SIZES = [100, 1000, 10000, 100000]
REPEATS = 3
SEED = 42
TOTAL_MEM = 100000


def generate_workload(n_requests: int, total_size: int = TOTAL_MEM, seed: int = SEED):
    """Sinh chuỗi yêu cầu alloc/free giả ngẫu nhiên có thể tái lập bằng seed cố định."""
    rng = random.Random(seed)
    reqs = []
    active = []
    pid_counter = 1
    for _ in range(n_requests):
        if len(active) >= 60 or (len(active) > 20 and rng.random() < 0.48):
            pid = active.pop(rng.randrange(len(active)))
            reqs.append(("free", pid, None))
        else:
            pid = f"P{pid_counter}"
            pid_counter += 1
            size = rng.randint(16, 1024)
            reqs.append(("alloc", pid, size))
            active.append(pid)
    return total_size, reqs


def run_once(total: int, requests, strategy_fn):
    m = MemoryManager(total)
    ok_count = 0
    t0 = time.perf_counter()
    for act, pid, sz in requests:
        if act == "alloc":
            if m.allocate(pid, sz, strategy_fn):
                ok_count += 1
        else:
            if m.free(pid):
                ok_count += 1
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    m.check_invariants()
    snap = m.snapshot()
    ext_f = round(metrics.external_fragmentation(snap), 4)
    int_f = metrics.internal_fragmentation(snap)
    return elapsed_ms, ok_count, ext_f, int_f


def run_benchmark(output_path=None):
    if output_path is None:
        output_path = PROJECT_ROOT / "output" / "benchmark.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    env_info = f"{platform.system()} {platform.release()} | Python {platform.python_version()} | {platform.processor() or platform.machine()}"
    print(f"Môi trường đo : {env_info}")
    print(f"Phương pháp   : time.perf_counter(), seed={SEED}, repeats={REPEATS}, total_mem={TOTAL_MEM} KB\n")

    rows = []
    for n in SIZES:
        total, reqs = generate_workload(n)
        for strat_name, strat_fn in STRATEGIES.items():
            times = []
            last_stats = None
            for _ in range(REPEATS):
                ms, ok_cnt, ext_f, int_f = run_once(total, reqs, strat_fn)
                times.append(ms)
                last_stats = (ok_cnt, ext_f, int_f)

            avg_ms = round(statistics.mean(times), 3)
            min_ms = round(min(times), 3)
            max_ms = round(max(times), 3)
            ok_cnt, ext_f, int_f = last_stats
            rows.append({
                "n_requests": n,
                "strategy": strat_name,
                "repeats": REPEATS,
                "seed": SEED,
                "avg_time_ms": avg_ms,
                "min_time_ms": min_ms,
                "max_time_ms": max_ms,
                "success_count": ok_cnt,
                "external_frag": ext_f,
                "internal_frag": int_f,
                "environment": env_info,
            })
            print(f"N={n:>6} | {strat_name:<9} | avg={avg_ms:>8.3f} ms (min={min_ms:.3f}, max={max_ms:.3f}) | ext={ext_f:.4f}")

    fieldnames = [
        "n_requests", "strategy", "repeats", "seed",
        "avg_time_ms", "min_time_ms", "max_time_ms",
        "success_count", "external_frag", "internal_frag", "environment",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nĐã lưu kết quả benchmark tại: {output_path}")
    return rows


if __name__ == "__main__":
    run_benchmark()