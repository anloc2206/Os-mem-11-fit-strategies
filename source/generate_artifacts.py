"""Tự động sinh toàn bộ bộ input mẫu, trace, compare.csv, test_table.csv và biểu đồ so sánh.

Cách chạy (từ thư mục gốc repo):
    python source/generate_artifacts.py
"""
import csv
import os
import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SOURCE_DIR.parent
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

import io_csv
import metrics
import simulator
from memory import MemoryManager
from strategies import STRATEGIES, first_fit, best_fit, worst_fit

INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"


def create_sample_inputs():
    """Mục 7 & 13: Tạo đủ các file CSV mẫu trong input/."""
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = {
        "case_tie_break.csv": (
            "action,pid,size\n"
            "init,,1080\n"
            "alloc,H1,200\nalloc,K1,20\n"
            "alloc,H2,300\nalloc,K2,20\n"
            "alloc,H3,200\nalloc,K3,20\n"
            "alloc,H4,300\nalloc,K4,20\n"
            "free,H1,\nfree,H2,\nfree,H3,\nfree,H4,\n"
            "alloc,P_TIE,150\n"
        ),
        "case_exact_fit.csv": (
            "action,pid,size\n"
            "init,,200\n"
            "alloc,P1,80\n"
            "alloc,P2,120\n"
            "free,P1,\n"
            "alloc,P3,80\n"
        ),
        "case_round_up.csv": (
            "action,pid,size\n"
            "init,,100\n"
            "alloc,P1,13\n"
            "alloc,P2,5\n"
            "alloc,P3,17\n"
        ),
        "case_duplicate_pid.csv": (
            "action,pid,size\n"
            "init,,200\n"
            "alloc,P1,40\n"
            "alloc,P1,60\n"
        ),
        "case_free_nonexistent.csv": (
            "action,pid,size\n"
            "init,,200\n"
            "alloc,P1,40\n"
            "free,P999,\n"
        ),
        "case_coalesce_both_sides.csv": (
            "action,pid,size\n"
            "init,,400\n"
            "alloc,A,100\n"
            "alloc,B,100\n"
            "alloc,C,100\n"
            "free,A,\n"
            "free,C,\n"
            "free,B,\n"
        ),
        "case_oversize.csv": (
            "action,pid,size\n"
            "init,,200\n"
            "alloc,BIG,250\n"
        ),
        "case_empty.csv": "",
        "case_invalid_format.csv": (
            "action,pid,size\n"
            "init,,200\n"
            "alloc,P1,-50\n"
        ),
        # Mục 13: Workload làm First-Fit, Best-Fit, Worst-Fit khác hẳn nhau
        "case_ff_vs_wf.csv": (
            "action,pid,size\n"
            "init,,1200\n"
            "alloc,H1,300\nalloc,K1,20\n"
            "alloc,H2,120\nalloc,K2,20\n"
            "alloc,H3,500\nalloc,K3,20\n"
            "alloc,H4,200\nalloc,K4,20\n"
            "free,H1,\nfree,H2,\nfree,H3,\nfree,H4,\n"
            "alloc,A,110\n"
            "alloc,B,180\n"
            "alloc,C,450\n"
            "alloc,D,280\n"
            "alloc,E,190\n"
        ),
    }
    for filename, content in cases.items():
        with open(INPUT_DIR / filename, "w", encoding="utf-8", newline="") as f:
            f.write(content)
    print(f"[OK] Đã tạo {len(cases)} file CSV mẫu trong input/")


def generate_traces_and_compare():
    """Mục 8: Sinh trace 3 chiến lược và file compare.csv từ workload case_ff_vs_wf.csv."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    workload_path = INPUT_DIR / "case_ff_vs_wf.csv"
    total, reqs = io_csv.read_requests(str(workload_path))

    compare_rows = []
    for name in STRATEGIES:
        trace = simulator.run_simulation(total, reqs, name)
        io_csv.write_trace(str(OUTPUT_DIR / f"trace_{name}.csv"), trace)

        alloc_ok = sum(1 for r in trace if r["action"] == "alloc" and r["success"] == 1)
        alloc_fail = sum(1 for r in trace if r["action"] == "alloc" and r["success"] == 0)
        last = trace[-1]
        compare_rows.append({
            "workload": workload_path.name,
            "strategy": name,
            "total_memory": total,
            "total_requests": len(reqs),
            "alloc_success": alloc_ok,
            "alloc_fail": alloc_fail,
            "free_total": last["free_total"],
            "largest_hole": last["largest_hole"],
            "external_frag": last["external_frag"],
            "internal_frag": last["internal_frag"],
        })

    compare_path = OUTPUT_DIR / "compare.csv"
    with open(compare_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(compare_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(compare_rows)
    print("[OK] Đã sinh output/trace_first_fit.csv, trace_best_fit.csv, trace_worst_fit.csv và compare.csv")


def generate_test_table():
    """Mục 9: Bảng test_table.csv lấy expected từ oracle tính tay (bảng 6.1, 6.2, 6.3 trong pseudocode.md)."""
    rows = []

    def add_row(tid, category, desc, inp, expected, actual):
        status = "PASS" if str(expected) == str(actual) else "FAIL"
        rows.append({
            "test_id": tid,
            "category": category,
            "description": desc,
            "input": inp,
            "expected": expected,
            "actual": actual,
            "status": status,
        })

    # 1. Oracle bảng 6.1 (pseudocode.md): holes = [100, 500, 200, 300, 600]
    holes_61 = [100, 500, 200, 300, 600]
    oracle_61 = [
        (212, 1, 3, 4),
        (417, 1, 1, 4),
        (112, 1, 2, 4),
        (426, 1, 1, 4),
        (100, 0, 0, 4),
        (700, None, None, None),
    ]
    idx = 1
    for sz, exp_ff, exp_bf, exp_wf in oracle_61:
        for s_name, fn, exp in (
            ("first_fit", first_fit, exp_ff),
            ("best_fit", best_fit, exp_bf),
            ("worst_fit", worst_fit, exp_wf),
        ):
            act = fn(holes_61, sz)
            cat = "Biên" if sz in (100, 700) else "Thường"
            add_row(f"TC{idx:02d}", cat, f"Oracle 6.1 {s_name} size={sz}", f"holes={holes_61}; size={sz}", exp, act)
            idx += 1

    # 2. Oracle bảng 6.2 (pseudocode.md): Tie-break holes = [200, 300, 200, 300], size = 150
    holes_62 = [200, 300, 200, 300]
    for s_name, fn, exp in (("first_fit", first_fit, 0), ("best_fit", best_fit, 0), ("worst_fit", worst_fit, 1)):
        add_row(f"TC{idx:02d}", "Tie-break", f"Oracle 6.2 {s_name}", f"holes={holes_62}; size=150", exp, fn(holes_62, 150))
        idx += 1

    # 3. Oracle bảng 6.3 (pseudocode.md): Phân mảnh ngoài và trong
    snap_63 = [(0, 100, None, 0), (100, 200, "P1", 190), (300, 300, None, 0)]
    add_row(f"TC{idx:02d}", "Thường", "Oracle 6.3 external_fragmentation", str(snap_63), 0.25, round(metrics.external_fragmentation(snap_63), 4))
    idx += 1
    add_row(f"TC{idx:02d}", "Thường", "Oracle 6.3 internal_fragmentation", str(snap_63), 10, metrics.internal_fragmentation(snap_63))
    idx += 1

    # 4. Các ca biên & dễ sai
    m = MemoryManager(100)
    m.allocate("P1", 13, first_fit)
    add_row(f"TC{idx:02d}", "Biên", "Làm tròn lên bội UNIT=4 (13->16)", "total=100; alloc(P1,13)", (0, 16, "P1", 13), m.snapshot()[0])
    idx += 1

    m = MemoryManager(100)
    m.allocate("A", 100, first_fit)
    add_row(f"TC{idx:02d}", "Biên", "Exact fit (rem=0)", "total=100; alloc(A,100)", [(0, 100, "A", 100)], m.snapshot())
    idx += 1

    m = MemoryManager(200)
    m.allocate("P1", 40, first_fit)
    add_row(f"TC{idx:02d}", "Dễ sai", "Trùng PID", "alloc(P1,40) rồi alloc(P1,60)", False, m.allocate("P1", 60, first_fit))
    idx += 1

    add_row(f"TC{idx:02d}", "Dễ sai", "Free PID không tồn tại", "free(P999)", False, m.free("P999"))
    idx += 1

    m = MemoryManager(400)
    m.allocate("A", 100, first_fit)
    m.allocate("B", 100, first_fit)
    m.allocate("C", 100, first_fit)
    m.free("A")
    m.free("C")
    m.free("B")
    add_row(f"TC{idx:02d}", "Dễ sai", "Gộp hole hai phía", "alloc A,B,C -> free A,C,B", [(0, 400, None, 0)], m.snapshot())
    idx += 1

    m = MemoryManager(200)
    add_row(f"TC{idx:02d}", "Biên", "Cấp phát lớn hơn tổng bộ nhớ", "total=200; alloc(BIG,250)", False, m.allocate("BIG", 250, first_fit))
    idx += 1

    try:
        MemoryManager(1001)
        act_err = "NoError"
    except ValueError:
        act_err = "ValueError"
    add_row(f"TC{idx:02d}", "Dễ sai", "total_size không chia hết cho UNIT", "MemoryManager(1001)", "ValueError", act_err)
    idx += 1

    add_row(f"TC{idx:02d}", "Dễ sai", "size là kiểu bool (True)", "allocate(P1, True)", False, m.allocate("P1", True, first_fit))
    idx += 1

    try:
        io_csv.read_requests(str(INPUT_DIR / "case_empty.csv"))
        act_empty = "NoError"
    except ValueError:
        act_empty = "ValueError"
    add_row(f"TC{idx:02d}", "Dễ sai", "Đọc file CSV rỗng", "input/case_empty.csv", "ValueError", act_empty)

    table_path = OUTPUT_DIR / "test_table.csv"
    with open(table_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    passed = sum(1 for r in rows if r["status"] == "PASS")
    print(f"[OK] Đã sinh output/test_table.csv ({passed}/{len(rows)} PASS)")


def plot_charts():
    """Mục 12: Vẽ biểu đồ so sánh từ compare.csv và benchmark.csv."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[!] Chưa cài matplotlib -> bỏ qua vẽ biểu đồ. Chạy 'pip install matplotlib' rồi chạy lại script này.")
        return

    # Biểu đồ 1: So sánh 3 chiến lược từ output/compare.csv
    compare_path = OUTPUT_DIR / "compare.csv"
    if compare_path.exists():
        with open(compare_path, newline="", encoding="utf-8") as f:
            data = list(csv.DictReader(f))
        strats = [r["strategy"] for r in data]
        ext_vals = [float(r["external_frag"]) for r in data]
        free_vals = [int(r["free_total"]) for r in data]
        largest_vals = [int(r["largest_hole"]) for r in data]

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        colors = ["#3B82F6", "#10B981", "#F59E0B"]

        bars1 = axes[0].bar(strats, ext_vals, color=colors)
        axes[0].set_title("Phân mảnh ngoài (External Fragmentation)")
        axes[0].set_ylabel("Tỷ lệ phân mảnh ngoài (thấp hơn = tốt hơn)")
        axes[0].set_ylim(0, max(ext_vals) * 1.25 + 0.05)
        for bar, val in zip(bars1, ext_vals):
            axes[0].text(bar.get_x() + bar.get_width() / 2, val + 0.015, f"{val:.4f}", ha="center", fontweight="bold")

        x = range(len(strats))
        w = 0.35
        b_free = axes[1].bar([i - w / 2 for i in x], free_vals, width=w, label="Tổng vùng trống (KB)", color="#60A5FA")
        b_large = axes[1].bar([i + w / 2 for i in x], largest_vals, width=w, label="Lỗ trống lớn nhất (KB)", color="#1E40AF")
        axes[1].set_title("Tổng vùng trống vs Lỗ trống lớn nhất")
        axes[1].set_xticks(list(x))
        axes[1].set_xticklabels(strats)
        axes[1].set_ylabel("Dung lượng (KB)")
        axes[1].legend()
        for bar in list(b_free) + list(b_large):
            h = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width() / 2, h + 5, str(int(h)), ha="center", fontsize=8)

        fig.suptitle("So sánh First-Fit, Best-Fit và Worst-Fit trên case_ff_vs_wf.csv", fontweight="bold")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "chart_compare.png", dpi=150)
        plt.close()
        print("[OK] Đã vẽ output/chart_compare.png")

    # Biểu đồ 2: Thời gian chạy từ output/benchmark.csv
    bench_path = OUTPUT_DIR / "benchmark.csv"
    if bench_path.exists():
        with open(bench_path, newline="", encoding="utf-8") as f:
            bdata = list(csv.DictReader(f))
        plt.figure(figsize=(8, 4.8))
        for strat, marker in (("first_fit", "o"), ("best_fit", "s"), ("worst_fit", "^")):
            sub = [r for r in bdata if r["strategy"] == strat]
            xs = [int(r["n_requests"]) for r in sub]
            ys = [float(r["avg_time_ms"]) for r in sub]
            plt.plot(xs, ys, marker=marker, linewidth=2, label=strat)
        plt.xscale("log")
        plt.yscale("log")
        plt.title("Benchmark thời gian thực thi theo số lượng yêu cầu (log-log)")
        plt.xlabel("Số lượng yêu cầu (N)")
        plt.ylabel("Thời gian trung bình (ms)")
        plt.grid(True, which="both", linestyle="--", alpha=0.4)
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "chart_benchmark.png", dpi=150)
        plt.close()
        print("[OK] Đã vẽ output/chart_benchmark.png")


if __name__ == "__main__":
    create_sample_inputs()
    generate_traces_and_compare()
    generate_test_table()
    plot_charts()