"""Test cho io_csv.py và simulator.py (Task 5)."""
import csv
import os
import tempfile
import unittest

import io_csv
import simulator


class TestReadRequests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def make_file(self, text):
        path = os.path.join(self.tmp.name, "in.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        return path

    def test_valid_file(self):
        path = self.make_file("action,pid,size\ninit,,1000\nalloc,P1,212\nfree,P1,\n")
        total, requests = io_csv.read_requests(path)
        self.assertEqual(total, 1000)
        self.assertEqual(requests, [("alloc", "P1", 212), ("free", "P1", None)])

    def test_blank_lines_and_bom_are_ok(self):
        path = self.make_file("\ufeffaction,pid,size\n\ninit,,500\n\nalloc,A,10\n")
        self.assertEqual(io_csv.read_requests(path), (500, [("alloc", "A", 10)]))

    def test_missing_file(self):
        with self.assertRaisesRegex(ValueError, "Không tìm thấy"):
            io_csv.read_requests(os.path.join(self.tmp.name, "khong_co.csv"))

    def test_empty_file(self):
        with self.assertRaisesRegex(ValueError, "rỗng"):
            io_csv.read_requests(self.make_file(""))

    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, "thiếu cột size"):
            io_csv.read_requests(self.make_file("action,pid\ninit,,1000\n"))

    def test_header_only(self):
        with self.assertRaisesRegex(ValueError, "thiếu dòng init"):
            io_csv.read_requests(self.make_file("action,pid,size\n"))

    def test_first_row_must_be_init(self):
        with self.assertRaisesRegex(ValueError, "dòng 2"):
            io_csv.read_requests(self.make_file("action,pid,size\nalloc,P1,10\n"))

    def test_bad_init_size(self):
        for bad in ("0", "-5", "abc", ""):
            with self.subTest(size=bad):
                with self.assertRaisesRegex(ValueError, "dòng 2"):
                    io_csv.read_requests(self.make_file(f"action,pid,size\ninit,,{bad}\n"))

    def test_init_twice(self):
        with self.assertRaisesRegex(ValueError, "dòng 3"):
            io_csv.read_requests(self.make_file("action,pid,size\ninit,,100\ninit,,200\n"))

    def test_unknown_action(self):
        with self.assertRaisesRegex(ValueError, "dòng 3"):
            io_csv.read_requests(self.make_file("action,pid,size\ninit,,100\nmove,P1,10\n"))

    def test_bad_alloc_size(self):
        for bad in ("abc", "-5", "10.5", "0", ""):
            with self.subTest(size=bad):
                with self.assertRaisesRegex(ValueError, "dòng 3"):
                    io_csv.read_requests(self.make_file(f"action,pid,size\ninit,,100\nalloc,P1,{bad}\n"))

    def test_empty_pid(self):
        with self.assertRaisesRegex(ValueError, "pid"):
            io_csv.read_requests(self.make_file("action,pid,size\ninit,,100\nfree,,\n"))


class TestSimulator(unittest.TestCase):

    # Ví dụ giáo trình: tạo các lỗ trống 100, 500, 200, 300, 600 rồi cấp 212, 417, 112, 426
    REQUESTS = (
        [("alloc", "P1", 100), ("alloc", "K1", 40), ("alloc", "P2", 500), ("alloc", "K2", 40),
         ("alloc", "P3", 200), ("alloc", "K3", 40), ("alloc", "P4", 300), ("alloc", "K4", 40),
         ("alloc", "P5", 600), ("alloc", "K5", 140)]
        + [("free", p, None) for p in ("P1", "P2", "P3", "P4", "P5")]
        + [("alloc", "A", 212), ("alloc", "B", 417), ("alloc", "C", 112), ("alloc", "D", 426)]
    )

    def test_trace_format(self):
        trace = simulator.run_simulation(2000, self.REQUESTS, "best_fit")
        self.assertEqual(len(trace), len(self.REQUESTS))
        self.assertEqual(trace[0]["step"], 1)
        for row in trace:
            self.assertEqual(set(row), set(io_csv.TRACE_COLUMNS))
            self.assertIn(row["success"], (0, 1))

    def test_strategies_differ(self):
        def failed(name):
            trace = simulator.run_simulation(2000, self.REQUESTS, name)
            return [r["pid"] for r in trace if not r["success"]]
        self.assertEqual(failed("best_fit"), [])
        self.assertEqual(failed("first_fit"), ["D"])
        self.assertEqual(failed("worst_fit"), ["D"])

    def test_failed_requests(self):
        requests = [("alloc", "A", 10), ("alloc", "A", 10), ("free", "X", None), ("alloc", "B", 5000)]
        trace = simulator.run_simulation(100, requests, "first_fit")
        self.assertEqual([r["success"] for r in trace], [1, 0, 0, 0])

    def test_unknown_strategy(self):
        with self.assertRaises(ValueError):
            simulator.run_simulation(100, [], "random_fit")

    def test_write_trace(self):
        trace = simulator.run_simulation(100, [("alloc", "A", 10), ("free", "A", None)], "best_fit")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sub", "trace.csv")  # thư mục sub chưa có, hàm phải tự tạo
            io_csv.write_trace(path, trace)
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.reader(f))
        self.assertEqual(rows[0], io_csv.TRACE_COLUMNS)
        self.assertEqual(len(rows), 3)


if __name__ == "__main__":
    unittest.main()
