import unittest

from source.memory import MemoryManager


def dummy_first_fit(holes, req_size):
    for i, h_size in enumerate(holes):
        if h_size >= req_size:
            return i
    return None


class TestMemoryIntegration(unittest.TestCase):

    def test_allocate_free_and_reallocate(self):
        memory = MemoryManager(1000)

        self.assertTrue(memory.allocate("P1", 100, dummy_first_fit))
        self.assertTrue(memory.allocate("P2", 200, dummy_first_fit))

        self.assertTrue(memory.free("P1"))
        self.assertTrue(memory.allocate("P3", 100, dummy_first_fit))

        snapshot = memory.snapshot()

        self.assertEqual(snapshot[0][2], "P3")
        self.assertEqual(snapshot[1][2], "P2")

    def test_multiple_processes_and_coalescing(self):
        memory = MemoryManager(1000)

        self.assertTrue(memory.allocate("P1", 100, dummy_first_fit))
        self.assertTrue(memory.allocate("P2", 100, dummy_first_fit))
        self.assertTrue(memory.allocate("P3", 100, dummy_first_fit))

        self.assertTrue(memory.free("P1"))
        self.assertTrue(memory.free("P2"))

        snapshot = memory.snapshot()

        self.assertEqual(snapshot[0], (0, 200, None, 0))

        self.assertTrue(memory.allocate("P4", 150, dummy_first_fit))

        snapshot = memory.snapshot()
        self.assertEqual(snapshot[0][2], "P4")


if __name__ == "__main__":
    unittest.main()