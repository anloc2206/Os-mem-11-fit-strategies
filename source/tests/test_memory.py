import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import unittest

try:
    from source.memory import MemoryManager, UNIT
except ImportError:
    from memory import MemoryManager, UNIT


def dummy_first_fit(holes, req_size):
    for i, h_size in enumerate(holes):
        if h_size >= req_size:
            return i
    return None


class TestMemoryManager(unittest.TestCase):

    def test_round_to_unit(self):
        m = MemoryManager(1000)
        self.assertTrue(m.allocate("P1", 5, dummy_first_fit))
        self.assertEqual(m.snapshot()[0], (0, 8, "P1", 5))

    def test_split_hole(self):
        m = MemoryManager(100)
        self.assertTrue(m.allocate("A", 30, dummy_first_fit))
        self.assertEqual(m.snapshot(), [(0, 32, "A", 30), (32, 68, None, 0)])

    def test_exact_fit_no_remainder(self):
        m = MemoryManager(100)
        self.assertTrue(m.allocate("A", 100, dummy_first_fit))
        self.assertEqual(m.snapshot(), [(0, 100, "A", 100)])
        self.assertFalse(m.allocate("B", 4, dummy_first_fit))

    def test_coalesce_with_next_hole(self):
        m = MemoryManager(1000)
        m.allocate("A", 100, dummy_first_fit)
        m.allocate("B", 100, dummy_first_fit)
        self.assertTrue(m.free("B"))
        self.assertEqual(m.snapshot(), [(0, 100, "A", 100), (100, 900, None, 0)])

    def test_coalesce_with_prev_hole(self):
        m = MemoryManager(1000)
        m.allocate("A", 100, dummy_first_fit)
        m.allocate("B", 100, dummy_first_fit)
        m.allocate("C", 100, dummy_first_fit)
        m.free("A")
        m.free("B")
        self.assertEqual(m.snapshot(), [(0, 200, None, 0), (200, 100, "C", 100), (300, 700, None, 0)])

    def test_reuse_middle_hole(self):
        m = MemoryManager(1000)
        m.allocate("A", 100, dummy_first_fit)
        m.allocate("B", 100, dummy_first_fit)
        m.allocate("C", 100, dummy_first_fit)
        m.free("B")
        self.assertTrue(m.allocate("D", 100, dummy_first_fit))
        self.assertEqual(m.snapshot()[1], (100, 100, "D", 100))

    def test_invalid_inputs(self):
        m = MemoryManager(1000)
        self.assertFalse(m.allocate("P1", -5, dummy_first_fit))
        self.assertFalse(m.allocate("", 10, dummy_first_fit))

    def test_coalescing_both_sides(self):
        m = MemoryManager(1000)
        m.allocate("A", 100, dummy_first_fit)
        m.allocate("B", 100, dummy_first_fit)
        m.allocate("C", 100, dummy_first_fit)
        m.free("A")
        m.free("C")
        m.free("B")
        self.assertEqual(m.snapshot(), [(0, 1000, None, 0)])


if __name__ == "__main__":
    unittest.main()