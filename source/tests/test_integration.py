import os
import sys
import tempfile
import unittest
from pathlib import Path

source_dir = Path(__file__).resolve().parent.parent
project_root = source_dir.parent
for p in (str(project_root), str(source_dir)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from source.memory import MemoryManager
    from source.strategies import STRATEGIES
    from source import io_csv, simulator
except ImportError:
    from memory import MemoryManager
    from strategies import STRATEGIES
    import io_csv
    import simulator


class TestMemoryIntegration(unittest.TestCase):

    def test_allocate_free_and_reallocate_all_strategies(self):
        for name, strat in STRATEGIES.items():
            with self.subTest(strategy=name):
                memory = MemoryManager(1000)
                self.assertTrue(memory.allocate("P1", 100, strat))
                self.assertTrue(memory.allocate("P2", 200, strat))
                self.assertTrue(memory.free("P1"))
                self.assertTrue(memory.allocate("P3", 100, strat))
                memory.check_invariants()

                pids = [b[2] for b in memory.snapshot() if b[2] is not None]
                self.assertIn("P2", pids)
                self.assertIn("P3", pids)
                self.assertNotIn("P1", pids)

    def test_multiple_processes_and_coalescing(self):
        for name, strat in STRATEGIES.items():
            with self.subTest(strategy=name):
                memory = MemoryManager(1000)
                self.assertTrue(memory.allocate("P1", 100, strat))
                self.assertTrue(memory.allocate("P2", 100, strat))
                self.assertTrue(memory.allocate("P3", 100, strat))
                self.assertTrue(memory.free("P1"))
                self.assertTrue(memory.free("P2"))
                memory.check_invariants()
                self.assertEqual(memory.snapshot()[0], (0, 200, None, 0))

                self.assertTrue(memory.allocate("P4", 150, strat))
                memory.check_invariants()

    def test_ff_bf_wf_tradeoff_end_to_end(self):
        """Workload cho thấy 3 chiến lược First-Fit, Best-Fit, Worst-Fit cho kết quả khác hẳn nhau."""
        requests = [
            ("alloc", "H1", 300), ("alloc", "K1", 20),
            ("alloc", "H2", 120), ("alloc", "K2", 20),
            ("alloc", "H3", 500), ("alloc", "K3", 20),
            ("alloc", "H4", 200), ("alloc", "K4", 20),
            ("free", "H1", None), ("free", "H2", None), ("free", "H3", None), ("free", "H4", None),
            ("alloc", "A", 110),
            ("alloc", "B", 180),
            ("alloc", "C", 450),
            ("alloc", "D", 280),
            ("alloc", "E", 190),
        ]
        failed = {}
        final_ext = {}
        for name in STRATEGIES:
            trace = simulator.run_simulation(1200, requests, name)
            failed[name] = [r["pid"] for r in trace if not r["success"]]
            final_ext[name] = trace[-1]["external_frag"]

        self.assertEqual(failed["first_fit"], ["D"])
        self.assertEqual(failed["best_fit"], ["E"])
        self.assertEqual(failed["worst_fit"], ["C"])
        self.assertEqual(len(set(final_ext.values())), 3)

    def test_csv_empty_and_invalid_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty_path = os.path.join(tmp, "empty.csv")
            with open(empty_path, "w", encoding="utf-8") as f:
                f.write("")
            with self.assertRaises(ValueError):
                io_csv.read_requests(empty_path)

            bad_path = os.path.join(tmp, "invalid.csv")
            with open(bad_path, "w", encoding="utf-8") as f:
                f.write("action,pid,size\ninit,,1000\nalloc,P1,-20\n")
            with self.assertRaises(ValueError):
                io_csv.read_requests(bad_path)

            bad_total_path = os.path.join(tmp, "bad_total.csv")
            with open(bad_total_path, "w", encoding="utf-8") as f:
                f.write("action,pid,size\ninit,,1001\nalloc,P1,16\n")
            total, reqs = io_csv.read_requests(bad_total_path)
            with self.assertRaises(ValueError):
                simulator.run_simulation(total, reqs, "first_fit")

    def test_invalid_memory_arguments(self):
        with self.assertRaises(ValueError):
            MemoryManager(1001)
        with self.assertRaises(ValueError):
            MemoryManager(0)
        m = MemoryManager(100)
        for bad_size in (True, False, 0, -4, 12.5, "16"):
            self.assertFalse(m.allocate("P1", bad_size, STRATEGIES["first_fit"]))


if __name__ == "__main__":
    unittest.main()