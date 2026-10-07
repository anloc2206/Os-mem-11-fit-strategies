import unittest
from memory import MemoryManager


def dummy_first_fit(holes, size):
    for idx, h in enumerate(holes):
        if h >= size:
            return idx
    return None


class TestMemoryManager(unittest.TestCase):

    def test_required_flow(self):
        m = MemoryManager(1000)
        self.assertTrue(m.allocate("P1", 102, dummy_first_fit))
        self.assertEqual(m.snapshot()[0], (0, 104, "P1", 102))

        self.assertTrue(m.allocate("P2", 200, dummy_first_fit))
        self.assertTrue(m.allocate("P3", 100, dummy_first_fit))

        self.assertTrue(m.free("P1"))
        self.assertTrue(m.free("P3"))
        self.assertTrue(m.free("P2"))
        self.assertEqual(m.snapshot(), [(0, 1000, None, 0)])

        self.assertFalse(m.free("X"))
        self.assertFalse(m.allocate("A", 0, dummy_first_fit))
        self.assertFalse(m.allocate("A", 5000, dummy_first_fit))

        self.assertTrue(m.allocate("A", 100, dummy_first_fit))
        self.assertFalse(m.allocate("A", 50, dummy_first_fit))
        m.check_invariants()

    def test_coalescing_both_sides(self):
        m = MemoryManager(1000)
        m.allocate("P1", 100, dummy_first_fit)
        m.allocate("P2", 100, dummy_first_fit)
        m.allocate("P3", 100, dummy_first_fit)

        m.free("P1")
        m.free("P3")
        m.free("P2")
        self.assertEqual(m.snapshot(), [(0, 1000, None, 0)])
        m.check_invariants()

    def test_check_invariants_detector(self):
        m = MemoryManager(1000)
        m.allocate("P1", 100, dummy_first_fit)
        m.blocks.append({"start": 1000, "size": 100, "pid": None, "requested": 0})
        with self.assertRaises(AssertionError):
            m.check_invariants()


if __name__ == "__main__":
    unittest.main()