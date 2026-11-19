
import unittest
import random

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
        memory.check_invariants()

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
        memory.check_invariants()

    def test_invalid_inputs(self):
        memory = MemoryManager(1000)

        # Kich thuoc khong hop le
        self.assertFalse(memory.allocate("P1", 0, dummy_first_fit))
        self.assertFalse(memory.allocate("P2", -100, dummy_first_fit))

        # PID khong hop le
        self.assertFalse(memory.allocate("", 100, dummy_first_fit))

        # PID bi trung
        self.assertTrue(memory.allocate("P3", 100, dummy_first_fit))
        self.assertFalse(memory.allocate("P3", 200, dummy_first_fit))

        # Thu hoi PID khong hop le hoac khong ton tai
        self.assertFalse(memory.free(""))
        self.assertFalse(memory.free("P999"))

        memory.check_invariants()

    def test_stress_5000_operations(self):
        memory = MemoryManager(10000)
        rng = random.Random(42)

        active_pids = []
        next_pid = 1

        for _ in range(5000):
            if active_pids and rng.random() < 0.30:
                index = rng.randrange(len(active_pids))
                pid = active_pids.pop(index)
                memory.free(pid)
            else:
                pid = f"P{next_pid}"
                next_pid += 1
                size = rng.randint(1, 500)

                if memory.allocate(pid, size, dummy_first_fit):
                    active_pids.append(pid)

            # Kiem tra tinh toan ven sau moi thao tac
            memory.check_invariants()

        self.assertGreaterEqual(len(memory.snapshot()), 1)


if __name__ == "__main__":
    unittest.main()
