
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import unittest

try:
    from source.strategies import first_fit, best_fit, worst_fit, STRATEGIES
    from source.metrics import external_fragmentation, internal_fragmentation
except ImportError:
    from strategies import first_fit, best_fit, worst_fit, STRATEGIES
    from metrics import external_fragmentation, internal_fragmentation


class TestStrategies(unittest.TestCase):
    

    def setUp(self):
        
        self.holes = [100, 500, 200, 300, 600]

    def test_first_fit_oracle(self):
        
        expected = {212: 1, 417: 1, 112: 1, 426: 1, 100: 0, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(first_fit(self.holes, size), exp)

    def test_best_fit_oracle(self):
        
        expected = {212: 3, 417: 1, 112: 2, 426: 1, 100: 0, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(best_fit(self.holes, size), exp)

    def test_worst_fit_oracle(self):
        
        expected = {212: 4, 417: 4, 112: 4, 426: 4, 100: 4, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(worst_fit(self.holes, size), exp)

    def test_tie_break_smallest_index(self):
        
        holes = [200, 300, 200, 300]
        self.assertEqual(first_fit(holes, 150), 0)
        self.assertEqual(best_fit(holes, 150), 0)   # 2 lỗ 200 (idx 0, 2) -> chọn 0
        self.assertEqual(worst_fit(holes, 150), 1)  # 2 lỗ 300 (idx 1, 3) -> chọn 1

    def test_strategies_dict(self):
        
        self.assertEqual(set(STRATEGIES.keys()), {"first_fit", "best_fit", "worst_fit"})
        self.assertIs(STRATEGIES["first_fit"], first_fit)
        self.assertIs(STRATEGIES["best_fit"], best_fit)
        self.assertIs(STRATEGIES["worst_fit"], worst_fit)

    def test_no_hole_big_enough(self):
        
        holes = [10, 20, 30]
        for f in (first_fit, best_fit, worst_fit):
            self.assertIsNone(f(holes, 100))

    def test_empty_holes(self):
        
        for f in (first_fit, best_fit, worst_fit):
            self.assertIsNone(f([], 10))

    def test_exact_match(self):
        
        holes = [100, 200]
        self.assertEqual(first_fit(holes, 100), 0)
        self.assertEqual(best_fit(holes, 100), 0)
        self.assertEqual(worst_fit(holes, 100), 1)

    def test_single_hole(self):
        
        holes = [500]
        self.assertEqual(first_fit(holes, 100), 0)
        self.assertEqual(best_fit(holes, 100), 0)
        self.assertEqual(worst_fit(holes, 100), 0)


class TestMetrics(unittest.TestCase):
    

    def test_external_fragmentation_oracle(self):
        
        snapshot = [(0, 100, None, 0), (100, 200, "P1", 190), (300, 300, None, 0)]
        self.assertAlmostEqual(external_fragmentation(snapshot), 0.25)

    def test_external_fragmentation_zero_when_one_hole(self):
        
        snapshot = [(0, 500, None, 0), (500, 500, "P1", 500)]
        self.assertEqual(external_fragmentation(snapshot), 0.0)

    def test_external_fragmentation_zero_when_no_hole(self):
        
        snapshot = [(0, 1000, "P1", 1000)]
        self.assertEqual(external_fragmentation(snapshot), 0.0)

    def test_internal_fragmentation_oracle(self):
        
        snapshot = [(0, 100, None, 0), (100, 200, "P1", 190), (300, 300, None, 0)]
        self.assertEqual(internal_fragmentation(snapshot), 10)

    def test_internal_fragmentation_no_alloc(self):
        
        snapshot = [(0, 1000, None, 0)]
        self.assertEqual(internal_fragmentation(snapshot), 0)

    def test_internal_fragmentation_multiple(self):
        
        snapshot = [
            (0, 104, "P1", 102),      # 104 - 102 = 2
            (104, 200, "P2", 197),    # 200 - 197 = 3
            (304, 696, None, 0),      # lỗ trống, bỏ qua
        ]
        self.assertEqual(internal_fragmentation(snapshot), 5)


if __name__ == "__main__":
    unittest.main()
