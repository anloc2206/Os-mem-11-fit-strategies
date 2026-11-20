
"""Tạo bảng kiểm thử cho hệ thống quản lý bộ nhớ."""
import csv
import os

from source.memory import MemoryManager
from source.strategies import STRATEGIES


def run_tests():
    cases = []

    for strategy_name, strategy in STRATEGIES.items():
        # Các ca cấp phát cơ bản
        for size in [1, 4, 10, 100, 500]:
            memory = MemoryManager(1000)
            result = memory.allocate("P1", size, strategy)
            memory.check_invariants()

            cases.append({
                "test_id": len(cases) + 1,
                "strategy": strategy_name,
                "test_case": f"Allocate size {size}",
                "input": size,
                "expected": True,
                "actual": result,
                "status": "PASS" if result else "FAIL",
            })

        # Cấp phát vượt quá bộ nhớ
        memory = MemoryManager(1000)
        result = memory.allocate("P1", 1200, strategy)
        memory.check_invariants()

        cases.append({
            "test_id": len(cases) + 1,
            "strategy": strategy_name,
            "test_case": "Allocate exceeding memory",
            "input": 1200,
            "expected": False,
            "actual": result,
            "status": "PASS" if not result else "FAIL",
        })

        # Thu hồi tiến trình
        memory = MemoryManager(1000)
        memory.allocate("P1", 100, strategy)
        result = memory.free("P1")
        memory.check_invariants()

        cases.append({
            "test_id": len(cases) + 1,
            "strategy": strategy_name,
            "test_case": "Free existing process",
            "input": "P1",
            "expected": True,
            "actual": result,
            "status": "PASS" if result else "FAIL",
        })

        # Thu hồi PID không tồn tại
        result = memory.free("P999")
        memory.check_invariants()

        cases.append({
            "test_id": len(cases) + 1,
            "strategy": strategy_name,
            "test_case": "Free missing process",
            "input": "P999",
            "expected": False,
            "actual": result,
            "status": "PASS" if not result else "FAIL",
        })

    return cases


def main():
    cases = run_tests()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output = os.path.join(root, "report", "test_table.csv")
    os.makedirs(os.path.dirname(output), exist_ok=True)

    with open(output, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=cases[0].keys())
        writer.writeheader()
        writer.writerows(cases)

    passed = sum(case["status"] == "PASS" for case in cases)

    print(f"Total test cases: {len(cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(cases) - passed}")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
