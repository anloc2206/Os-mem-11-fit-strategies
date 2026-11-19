UNIT = 4


class MemoryManager:
    """Quản lý cấp phát, thu hồi và gộp lỗ trống bộ nhớ."""

    def __init__(self, total_size: int, unit: int = UNIT):
        if total_size <= 0:
            raise ValueError("Tổng dung lượng bộ nhớ phải lớn hơn 0")
        self.total_size = total_size
        self.unit = unit
        self.blocks = [{"start": 0, "size": total_size, "pid": None, "requested": 0}]

    def allocate(self, pid: str, size: int, strategy) -> bool:
        if size <= 0 or not pid or any(b["pid"] == pid for b in self.blocks):
            return False

        aligned_size = ((size + self.unit - 1) // self.unit) * self.unit
        holes = [b["size"] for b in self.blocks if b["pid"] is None]
        chosen_idx = strategy(holes, aligned_size)

        if chosen_idx is None or chosen_idx < 0 or chosen_idx >= len(holes):
            return False

        # Tìm block lỗ trống tương ứng
        hole_cnt = 0
        for idx, b in enumerate(self.blocks):
            if b["pid"] is None:
                if hole_cnt == chosen_idx:
                    if b["size"] < aligned_size:
                        return False
                    rem = b["size"] - aligned_size
                    alloc_block = {"start": b["start"], "size": aligned_size, "pid": pid, "requested": size}
                    if rem > 0:
                        rem_block = {"start": b["start"] + aligned_size, "size": rem, "pid": None, "requested": 0}
                        self.blocks[idx:idx + 1] = [alloc_block, rem_block]
                    else:
                        self.blocks[idx] = alloc_block
                    return True
                hole_cnt += 1
        return False

    def free(self, pid: str) -> bool:
        if not pid:
            return False

        target_idx = next((i for i, b in enumerate(self.blocks) if b["pid"] == pid), -1)
        if target_idx == -1:
            return False

        self.blocks[target_idx]["pid"] = None
        self.blocks[target_idx]["requested"] = 0

        # Gộp các lỗ trống kề nhau
        merged = []
        for b in self.blocks:
            if merged and merged[-1]["pid"] is None and b["pid"] is None:
                merged[-1]["size"] += b["size"]
            else:
                merged.append(b.copy())
        self.blocks = merged
        return True

    def snapshot(self) -> list:
        return [(b["start"], b["size"], b["pid"], b["requested"]) for b in self.blocks]

    def check_invariants(self) -> None:
        if not self.blocks:
            raise AssertionError("Danh sách block rỗng")

        total = 0
        for i, b in enumerate(self.blocks):
            total += b["size"]
            if i == 0 and b["start"] != 0:
                raise AssertionError("Block đầu phải bắt đầu từ 0")
            if i > 0:
                prev = self.blocks[i - 1]
                if b["start"] != prev["start"] + prev["size"]:
                    raise AssertionError(f"Block {i} không liền kề block trước")
                if b["pid"] is None and prev["pid"] is None:
                    raise AssertionError("Chưa gộp 2 lỗ trống kề nhau")

        if total != self.total_size:
            raise AssertionError("Tổng size không bằng total_size")