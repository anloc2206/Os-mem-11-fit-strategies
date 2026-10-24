# Pseudocode và độ phức tạp — Task 2 (OS_MEM_11)

Tài liệu mô tả 3 chiến lược cấp phát vùng nhớ liên tục và 2 hàm đo phân mảnh
theo hợp đồng ở Mục 4 file phân công. Người đọc có thể tái lập logic mà không
cần đọc mã nguồn.

---

## 0. Quy ước ký hiệu

- `holes`: `list[int]` — kích thước các lỗ trống (KB), theo thứ tự địa chỉ tăng dần.
- `size`: `int` — kích thước yêu cầu, ĐÃ làm tròn lên bội của `UNIT = 4`.
- `None`: trong ngữ cảnh strategy → không có lỗ nào đủ; trong snapshot → block là lỗ trống (`pid = None`).
- Chỉ số index trong `holes` là **0-based**.
- `snapshot`: `list[tuple]`, mỗi tuple `(start, size, pid, requested)`.
- Lưu ý phân biệt:
  - **Strategy** (`first_fit`, ...) chỉ nhận `holes: list[int]` và `size: int`.
  - **Metrics** (`external_fragmentation`, ...) nhận `snapshot: list[tuple]`.

---

## 1. First-Fit
```
FIRST_FIT(holes, size):
    for i from 0 to len(holes) - 1:
        if holes[i] >= size:
            return i
    return None
```


**Ý tưởng:** duyệt `holes` theo thứ tự địa chỉ, chọn lỗ đầu tiên đủ lớn. Không quan tâm lỗ lớn bao nhiêu — miễn đủ chứa là lấy.

- **Độ phức tạp thời gian:** best case `O(1)` (lỗ đầu tiên đủ), worst case `O(n)`.
- **Độ phức tạp không gian:** `O(1)`.
- **Tie-break:** không áp dụng — luôn lấy lỗ đầu tiên thỏa.
- **Ưu điểm:** nhanh, đơn giản.
- **Nhược điểm:** có thể làm vỡ vụn lỗ lớn ở đầu, tăng phân mảnh ngoài về sau.

---

## 2. Best-Fit

```
BEST_FIT(holes, size):
    best_idx  = None
    best_size = None
    for i from 0 to len(holes) - 1:
        if holes[i] >= size and (best_size is None or holes[i] < best_size):
            best_size = holes[i]
            best_idx  = i
    return best_idx
```


**Ý tưởng:** duyệt toàn bộ `holes`, tìm lỗ **nhỏ nhất** còn đủ chứa `size`.

**Tie-break:** dùng `<` (không phải `<=`) → khi gặp lỗ cùng kích thước `best_size`, **không** cập nhật → giữ **index nhỏ nhất**.

- **Độ phức tạp thời gian:** `O(n)` — luôn duyệt hết list vì cần tìm lỗ nhỏ hơn.
- **Độ phức tạp không gian:** `O(1)`.
- **Ưu điểm:** để lại lỗ lớn nguyên vẹn → giảm phân mảnh ngoài.
- **Nhược điểm:** tạo nhiều lỗ nhỏ vụn; chậm hơn First-Fit về hằng số.

---

## 3. Worst-Fit

```
WORST_FIT(holes, size):
    worst_idx  = None
    worst_size = -1
    for i from 0 to len(holes) - 1:
        if holes[i] >= size and holes[i] > worst_size:
            worst_size = holes[i]
            worst_idx  = i
    return worst_idx
```


**Ý tưởng:** duyệt toàn bộ `holes`, tìm lỗ **lớn nhất** đủ chứa `size`.

**Tie-break:** dùng `>` (không phải `>=`) → giữ **index nhỏ nhất** khi có nhiều lỗ cùng kích thước.

- **Độ phức tạp thời gian:** `O(n)`.
- **Độ phức tạp không gian:** `O(1)`.
- **Ưu điểm:** phần dư sau cấp phát vẫn lớn → có thể tái dùng cho yêu cầu lớn sau.
- **Nhược điểm:** liên tục phá hủy lỗ lớn → sớm hết lỗ cho process lớn kế tiếp.

---

## 4. Bảng so sánh nhanh

| Tiêu chí | First-Fit | Best-Fit | Worst-Fit |
|----------|-----------|----------|-----------|
| Thời gian | Best O(1), Worst O(n) | O(n) | O(n) |
| Bộ nhớ phụ | O(1) | O(1) | O(1) |
| Tie-break | Không áp dụng | Index nhỏ nhất | Index nhỏ nhất |
| Phân mảnh ngoài | Trung bình | Thấp | Cao |
| Tốc độ thực tế | Nhanh nhất | Chậm hơn | Chậm hơn |
| Rủi ro chính | Vỡ vụn lỗ đầu | Nhiều lỗ nhỏ | Phá lỗ lớn |

---

## 5. Công thức đo phân mảnh

```
EXTERNAL_FRAGMENTATION(snapshot):
    holes ← [b[1] for b in snapshot if b[2] is None]
    if len(holes) <= 1:
        return 0
    total ← sum(holes)
    if total == 0:           
        return 0
    return 1 - (max(holes) / total)

INTERNAL_FRAGMENTATION(snapshot):
    total ← 0
    for b in snapshot:
        (start, size, pid, requested) ← b      
        if pid is not None:
            total ← total + (size - requested)
    return total
```


Ghi chú: `b = (start, size, pid, requested)`, dùng chỉ số tuple.

**Độ phức tạp:** `O(n)` với `n = len(snapshot)` cho cả hai hàm.

---

## 6. Ví dụ chạy tay

### 6.1. Bảng oracle — `holes = [100, 500, 200, 300, 600]`

Cột chiến lược ghi **chỉ số** lỗ được chọn (0-based); số trong ngoặc là **kích thước lỗ đó** (KB).

| size | First-Fit | Best-Fit | Worst-Fit |
|------|-----------|----------|-----------|
| 212 | 1 (500) | 3 (300) | 4 (600) |
| 417 | 1 (500) | 1 (500) | 4 (600) |
| 112 | 1 (500) | 2 (200) | 4 (600) |
| 426 | 1 (500) | 1 (500) | 4 (600) |
| 100 | 0 (100) | 0 (100) | 4 (600) |
| 700 | None | None | None |

### 6.2. Tie-break — `holes = [200, 300, 200, 300], size = 150`

- First-Fit → **0** (lỗ 200 đầu tiên)
- Best-Fit → **0** (2 lỗ 200 bằng nhau → lấy index nhỏ nhất)
- Worst-Fit → **1** (2 lỗ 300 bằng nhau → lấy index nhỏ nhất)

**Ví dụ Best-Fit** `holes=[200, 300, 200, 300], size=150`:
  i=0: holes[0]=200 >= 150, best_size=None  → cập nhật: best_size=200, best_idx=0
  i=1: holes[1]=300 >= 150, 300 < 200? Không → bỏ qua
  i=2: holes[2]=200 >= 150, 200 < 200? Không → bỏ qua 
  i=3: holes[3]=300 >= 150, 300 < 200? Không → bỏ qua
  → return 0

### 6.3. Phân mảnh — `snapshot = [(0,100,None,0), (100,200,"P1",190), (300,300,None,0)]`

- Lỗ trống: 100 KB (start=0) + 300 KB (start=300) → `holes = [100, 300]`, `max = 300`, `sum = 400`
- External = `1 − 300/400` = **0.25**
- Block đã cấp: P1 có size=200, requested=190 → Internal = `200 − 190` = **10 KB**

---

## 7. Nguồn tham khảo

- Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
  Chương 9 — Main Memory, mục 9.2 *Contiguous Memory Allocation* (First-Fit, Best-Fit, Worst-Fit).