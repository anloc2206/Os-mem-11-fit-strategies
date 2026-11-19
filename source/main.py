"""Chạy mô phỏng bằng dòng lệnh (không cần giao diện).

Ví dụ:
    python source/main.py --input input/sample_requests.csv --strategy best_fit --output output/sample_trace.csv
"""
import argparse
import sys

from io_csv import read_requests, write_trace
from simulator import run_simulation
from strategies import STRATEGIES


def main():
    parser = argparse.ArgumentParser(description="Mô phỏng cấp phát bộ nhớ First-Fit / Best-Fit / Worst-Fit")
    parser.add_argument("--input", required=True, help="file CSV đầu vào (xem định dạng trong README)")
    parser.add_argument("--strategy", default="best_fit", choices=list(STRATEGIES),
                        help="chiến lược cấp phát (mặc định: best_fit)")
    parser.add_argument("--output", default="output/trace.csv", help="file CSV trace đầu ra")
    args = parser.parse_args()

    try:
        total, requests = read_requests(args.input)
        trace = run_simulation(total, requests, args.strategy)
        write_trace(args.output, trace)
    except (ValueError, OSError) as e:
        print(f"Lỗi: {e}")
        sys.exit(1)

    # In tóm tắt kết quả
    alloc_ok = sum(1 for r in trace if r["action"] == "alloc" and r["success"])
    alloc_fail = sum(1 for r in trace if r["action"] == "alloc" and not r["success"])
    free_ok = sum(1 for r in trace if r["action"] == "free" and r["success"])
    free_fail = sum(1 for r in trace if r["action"] == "free" and not r["success"])
    print(f"File đầu vào : {args.input}")
    print(f"Chiến lược   : {args.strategy}")
    print(f"Tổng bộ nhớ  : {total} KB, số yêu cầu: {len(requests)}")
    print(f"Cấp phát     : {alloc_ok} thành công, {alloc_fail} thất bại")
    print(f"Thu hồi      : {free_ok} thành công, {free_fail} thất bại")
    if trace:
        last = trace[-1]
        print(f"Cuối cùng    : trống {last['free_total']} KB, lỗ lớn nhất {last['largest_hole']} KB, "
              f"phân mảnh ngoài {last['external_frag']}, phân mảnh trong {last['internal_frag']} KB")
    print(f"Đã ghi trace : {args.output}")


if __name__ == "__main__":
    main()
