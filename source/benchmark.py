
"""Benchmark First-Fit, Best-Fit và Worst-Fit."""
import csv
import os
import time

try:
    from source.memory import MemoryManager
    from source.strategies import STRATEGIES
    from source.metrics import external_fragmentation, internal_fragmentation
    from source.workload import generate
except ModuleNotFoundError:
    from memory import MemoryManager
    from strategies import STRATEGIES
    from metrics import external_fragmentation, internal_fragmentation
    from workload import generate


TOTAL_SIZE = 10_000
MAX_SIZE = 500
SEED = 42
N_VALUES = [1_000, 10_000, 20_000]
REPEATS = 3


def run_once(n, seed, strategy_name):
    workload = generate(n, seed, TOTAL_SIZE, MAX_SIZE)
    manager = MemoryManager(TOTAL_SIZE)
    strategy = STRATEGIES[strategy_name]

    successes = 0
    allocations = 0

    start = time.perf_counter()

    for action, pid, size in workload:
        if action == "alloc":
            allocations += 1
            if manager.allocate(pid, size, strategy):
                successes += 1
        elif action == "free":
            manager.free(pid)

    elapsed = time.perf_counter() - start
    snapshot = manager.snapshot()

    return {
        "seconds": elapsed,
        "success_rate": successes / allocations if allocations else 0.0,
        "final_external_frag": external_fragmentation(snapshot),
        "final_internal_frag": internal_fragmentation(snapshot),
    }


def run_benchmark():
    results = []

    for n in N_VALUES:
        for seed in range(SEED, SEED + REPEATS):
            for strategy_name in STRATEGIES:
                run = run_once(n, seed, strategy_name)

                results.append({
                    "n": n,
                    "seed": seed,
                    "total_size": TOTAL_SIZE,
                    "max_size": MAX_SIZE,
                    "strategy": strategy_name,
                    "seconds": round(run["seconds"], 6),
                    "success_rate": round(run["success_rate"], 6),
                    "final_external_frag": round(run["final_external_frag"], 6),
                    "final_internal_frag": run["final_internal_frag"],
                })

    return results


def save_csv(results):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "output", "benchmark.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    columns = [
        "n", "seed", "total_size", "max_size", "strategy",
        "seconds", "success_rate", "final_external_frag",
        "final_internal_frag"
    ]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    return output_path


def main():
    results = run_benchmark()
    output_path = save_csv(results)

    print("BENCHMARK COMPLETED")
    print(f"So dong ket qua: {len(results)}")
    print(f"Da luu: {output_path}")


if __name__ == "__main__":
    main()
