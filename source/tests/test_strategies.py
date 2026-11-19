
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
        """Bảng oracle First-Fit"""
        expected = {212: 1, 417: 1, 112: 1, 426: 1, 100: 0, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(first_fit(self.holes, size), exp)

    def test_best_fit_oracle(self):
        """Bảng oracle Best-Fit"""
        expected = {212: 3, 417: 1, 112: 2, 426: 1, 100: 0, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(best_fit(self.holes, size), exp)

    def test_worst_fit_oracle(self):
        """Bảng oracle Worst-Fit"""
        expected = {212: 4, 417: 4, 112: 4, 426: 4, 100: 4, 700: None}
        for size, exp in expected.items():
            with self.subTest(size=size):
                self.assertEqual(worst_fit(self.holes, size), exp)

    def test_tie_break_smallest_index(self):
        """Tie: khi có nhiều lỗ bằng nhau, chọn index NHỎ NHẤT."""
        holes = [200, 300, 200, 300]
        self.assertEqual(first_fit(holes, 150), 0)
        self.assertEqual(best_fit(holes, 150), 0)   
        self.assertEqual(worst_fit(holes, 150), 1)  

    def test_strategies_dict(self):
        """Kiểm tra từ điển STRATEGIES chứa đủ 3 chiến lược."""
        self.assertEqual(set(STRATEGIES.keys()), {"first_fit", "best_fit", "worst_fit"})
        self.assertIs(STRATEGIES["first_fit"], first_fit)
        self.assertIs(STRATEGIES["best_fit"], best_fit)
        self.assertIs(STRATEGIES["worst_fit"], worst_fit)

    def test_no_hole_big_enough(self):
        """Không lỗ nào đủ -> cả 3 chiến lược trả None."""
        holes = [10, 20, 30]
        for f in (first_fit, best_fit, worst_fit):
            self.assertIsNone(f(holes, 100))

    def test_empty_holes(self):
        """Danh sách lỗ trống rỗng -> cả 3 chiến lược trả None."""
        for f in (first_fit, best_fit, worst_fit):
            self.assertIsNone(f([], 10))

    def test_exact_match(self):
        """size đúng bằng lỗ -> vẫn chọn được. """
        holes = [100, 200]
        self.assertEqual(first_fit(holes, 100), 0)
        self.assertEqual(best_fit(holes, 100), 0)
        self.assertEqual(worst_fit(holes, 100), 1)

    def test_single_hole(self):
        """Chỉ có 1 lỗ trống: cả 3 chiến lược đều trả index 0 nếu đủ."""
        holes = [500]
        self.assertEqual(first_fit(holes, 100), 0)
        self.assertEqual(best_fit(holes, 100), 0)
        self.assertEqual(worst_fit(holes, 100), 0)


class TestMetrics(unittest.TestCase):
    

    def test_external_fragmentation_oracle(self):
        """Chỉ 2 lỗ trống trong 3 lỗ, có phân mảnh ngoài 0.25"""
        snapshot = [(0, 100, None, 0), (100, 200, "P1", 190), (300, 300, None, 0)]
        self.assertAlmostEqual(external_fragmentation(snapshot), 0.25)

    def test_external_fragmentation_zero_when_one_hole(self):
        """Chỉ có 1 lỗ trống -> không có phân mảnh ngoài -> 0."""
        snapshot = [(0, 500, None, 0), (500, 500, "P1", 500)]
        self.assertEqual(external_fragmentation(snapshot), 0.0)

    def test_external_fragmentation_zero_when_no_hole(self):
        """Không còn lỗ trống -> 0"""
        snapshot = [(0, 1000, "P1", 1000)]
        self.assertEqual(external_fragmentation(snapshot), 0.0)

    def test_internal_fragmentation_oracle(self):
        """Có 1 lỗ chứa tiến trình -> int = 10"""
        snapshot = [(0, 100, None, 0), (100, 200, "P1", 190), (300, 300, None, 0)]
        self.assertEqual(internal_fragmentation(snapshot), 10)

    def test_internal_fragmentation_no_alloc(self):
        """Toàn bộ là lỗ trống -> int = 0."""
        snapshot = [(0, 1000, None, 0)]
        self.assertEqual(internal_fragmentation(snapshot), 0)

    def test_internal_fragmentation_multiple(self):
        """Có 2 lỗ chứa tiến trình, tổng dư thừa còn lại của 2 lỗ -> int = 5"""
        snapshot = [(0, 104, "P1", 102), (104, 200, "P2", 197), (304, 696, None, 0)]
        self.assertEqual(internal_fragmentation(snapshot), 5)


if __name__ == "__main__":
    unittest.main()
