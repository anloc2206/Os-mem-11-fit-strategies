# OS_MEM_11: First-Fit, Best-Fit và Worst-Fit

Ứng dụng desktop (Python Tkinter) mô phỏng cấp phát và thu hồi vùng nhớ liên tục (Contiguous Memory Allocation), trực quan hóa bản đồ bộ nhớ (Memory Map), tính toán phân mảnh trong/ngoài và đối chiếu hiệu năng giữa 3 chiến lược **First-Fit**, **Best-Fit**, **Worst-Fit**.

- **Môn học:** Hệ điều hành
- **Giảng viên:** Mai Ngọc Châu
- **Lớp:** 012012500102
- **Nhóm:** OS_2627102_08
- **Trưởng nhóm:** Hồ An Lộc (GitHub: `anloc2206`)

---

## 1. Thành viên và Phân công

| STT | Họ tên | MSSV | GitHub | Mảng phụ trách chính |
|---|---|---|---|---|
| 1 | Hồ An Lộc | 082207006118 | `anloc2206` | Giao diện Tkinter (GUI), điều phối, quản lý repo (Leader) |
| 2 | Trần Huy Bảo | 079207005017 | `huybaotran307-thb` | Lõi bộ nhớ (`memory.py`), cấp phát/thu hồi/gộp lỗ trống |
| 3 | Vũ Minh Khôi | 075207011378 | `khoiminhvu2303-sudo` | Thuật toán 3 chiến lược (`strategies.py`), chỉ số phân mảnh (`metrics.py`), `pseudocode.md` |
| 4 | Phạm Minh Tân | 079207043105 | `Pham-Minh-Tan` | Đọc/ghi & kiểm tra lỗi CSV (`io_csv.py`), bộ mô phỏng (`simulator.py`), CLI (`main.py`) |
| 5 | Nguyễn Hưng Duy | 079207019278 | `ngduymeomeo` | Kiểm thử tích hợp, sinh workload, benchmark hiệu năng (`benchmark.py`) |

---

## 2. Đặc tả bài toán & Giả định

- **Phạm vi:** Chỉ xét cấp phát vùng nhớ liên tục (không làm paging, segmentation, bộ nhớ ảo).
- **Đơn vị cấp phát (`UNIT`):** `4 KB`. Tổng dung lượng bộ nhớ (`total_size`) phải là số nguyên dương và chia hết cho `4`.
- **Làm tròn kích thước:** Mọi yêu cầu `alloc` có `size > 0` được làm tròn lên bội nhỏ nhất của `4` (`aligned_size = ((size + 3) // 4) * 4`). Phần dư `aligned_size - size` là **phân mảnh trong** (Internal Fragmentation).
- **Gộp lỗ trống (Coalescing):** Khi thu hồi (`free`), các lỗ trống liền kề bên trái và/hoặc bên phải được gộp ngay thành một lỗ trống duy nhất.
- **Quy tắc phá hòa (Tie-breaking):** Khi có nhiều lỗ trống cùng kích thước tối ưu, chọn lỗ có **địa chỉ bắt đầu nhỏ nhất** (index nhỏ nhất).
- **Công thức phân mảnh ngoài (External Fragmentation):**
  - Nếu số lỗ trống $\le 1$ hoặc tổng vùng trống $= 0$: trả về `0.0`.
  - Ngược lại: $1 - \frac{\text{largest\_hole}}{\text{free\_total}}$.

---

## 3. Cấu trúc thư mục

```text
Os-mem-11-fit-strategies/
├── source/
│   ├── memory.py               # Lõi quản lý bộ nhớ (MemoryManager, check_invariants)
│   ├── strategies.py           # Thuật toán first_fit, best_fit, worst_fit
│   ├── metrics.py              # Tính phân mảnh trong và phân mảnh ngoài
│   ├── io_csv.py               # Đọc/kiểm tra lỗi CSV input và ghi CSV trace
│   ├── simulator.py            # Bộ mô phỏng chạy chuỗi yêu cầu
│   ├── main.py                 # Giao diện dòng lệnh (CLI)
│   ├── gui.py                  # Ứng dụng desktop Tkinter (Dark System Monitor)
│   ├── benchmark.py            # Stress test & đo hiệu năng (100 -> 100.000 yêu cầu)
│   ├── generate_artifacts.py   # Tự động sinh bộ input mẫu, trace, compare, test_table, biểu đồ
│   └── tests/                  # Bộ Unit Test & Integration Test (46 test cases)
├── input/                      # Bộ file CSV đầu vào (sample, tie-break, biên, lỗi, FF vs WF)
├── output/                     # Trace CSV, compare.csv, test_table.csv, benchmark.csv, biểu đồ PNG
├── report/
│   └── pseudocode.md           # Pseudocode, phân tích độ phức tạp và bảng test oracle tính tay
├── PROGRESS.md                 # Bảng theo dõi tiến độ 8 tuần
└── README.md
```

---

## 4. Cài đặt và Hướng dẫn chạy

### Yêu cầu môi trường
- **Hệ điều hành:** Windows 10/11 (khuyến nghị), Linux hoặc macOS.
- **Python:** Python 3.10 trở lên (có sẵn `tkinter` và `unittest`).
- **Thư viện vẽ biểu đồ (tùy chọn, dùng cho `generate_artifacts.py`):**
  ```bash
  pip install matplotlib
  ```

### Các lệnh chạy chính (chạy từ thư mục gốc repository)

1. **Chạy ứng dụng giao diện (GUI):**
   ```bash
   python source/gui.py
   ```
2. **Chạy mô phỏng bằng dòng lệnh (CLI):**
   ```bash
   python source/main.py --input input/case_ff_vs_wf.csv --strategy best_fit --output output/trace_best_fit.csv
   ```
3. **Chạy toàn bộ bộ kiểm thử (46 Unit & Integration Tests):**
   ```bash
   python -m unittest discover -s source/tests -v
   ```
4. **Chạy Stress Test & Benchmark hiệu năng (`output/benchmark.csv`):**
   ```bash
   python source/benchmark.py
   ```
5. **Tái lập toàn bộ input mẫu, trace, bảng đối chiếu, `test_table.csv` và biểu đồ PNG:**
   ```bash
   python source/generate_artifacts.py
   ```

---

## 5. Định dạng dữ liệu CSV

### Input CSV (`input/*.csv`)
Gồm 3 cột `action,pid,size`. Dòng dữ liệu đầu tiên bắt buộc là `init` (không cần `pid`, `size` chia hết cho `4`):

```csv
action,pid,size
init,,1000
alloc,P1,212
alloc,P2,417
free,P1,
alloc,P3,112
```

### Output Trace CSV (`output/trace_*.csv`)
Mỗi dòng tương ứng với 1 bước thực thi sau `init`, gồm 10 cột cố định:

```text
step,strategy,action,pid,size,success,free_total,largest_hole,external_frag,internal_frag
```

---

## 6. Kết quả kiểm thử & Tái lập

- **Bộ test tự động:** 46/46 test cases (`test_memory.py`, `test_strategies.py`, `test_task5.py`, `test_integration.py`) đạt trạng thái `OK`.
- **Bảng đối chiếu Oracle (`output/test_table.csv`):** 32/32 ca kiểm thử (thường, biên, tie-break, gộp lỗ 2 phía, dữ liệu sai/rỗng) đối chiếu từ bảng 6.1–6.3 trong `report/pseudocode.md` đạt `PASS`.
- **So sánh 3 chiến lược (`output/compare.csv` & `output/chart_compare.png`):** Chạy trên workload `input/case_ff_vs_wf.csv` thể hiện rõ sự khác biệt về phân mảnh ngoài và tỷ lệ cấp phát thành công giữa First-Fit, Best-Fit và Worst-Fit.
- **Benchmark (`output/benchmark.csv` & `output/chart_benchmark.png`):** Đo bằng `time.perf_counter()` với `seed=42`, `repeats=3` trên các cỡ `100`, `1.000`, `10.000`, `100.000` yêu cầu.

---

## 7. Kế hoạch 8 tuần

| Tuần | Nội dung | Trạng thái |
|---|---|---|
| 1 | Chọn đề tài, phân vai, đặc tả và repo | Đã thực hiện |
| 2 | Mô hình/pseudocode và test oracle | Đã thực hiện |
| 3–4 | Hiện thực lõi thuật toán | Đã thực hiện |
| 5 | GUI, CSV, trực quan hóa | Đã thực hiện |
| 6 | Kiểm thử đúng đắn và hiệu năng | Đã thực hiện |
| 7 | Hoàn thiện, review chéo và sửa lỗi | Đã thực hiện |
| 8 | Báo cáo, video, demo và bảo vệ ngắn | Đang tiến hành |

Chi tiết từng đầu việc xem tại [PROGRESS.md](PROGRESS.md).

---

## 8. Nguồn tham khảo & Khai báo sử dụng AI

### Nguồn tham khảo
1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley. (Chapter 9: Main Memory — Section 9.2 Contiguous Memory Allocation).
2. Tanenbaum, A. S., & Bos, H. (2015). *Modern Operating Systems* (4th ed.). Pearson. (Chapter 3: Memory Management).
3. Slide bài giảng môn Hệ điều hành — *Chapter 03: Memory Management* (Trường Đại học Giao thông Vận tải TP.HCM).
4. Python Software Foundation. *Python 3 Documentation — `tkinter`, `csv`, `unittest`, `time` modules*. https://docs.python.org/3/
5. Hunter, J. D. et al. *Matplotlib: Visualization with Python*. https://matplotlib.org/

### Khai báo sử dụng AI
Nhóm có sử dụng công cụ AI (Gemini) để hỗ trợ rà soát lỗi biên (edge cases), cải thiện bố cục giao diện Tkinter và gợi ý cấu trúc script sinh dữ liệu/biểu đồ kiểm thử. Toàn bộ mã nguồn, kết quả chạy `unittest` (46/46 PASS), `test_table.csv` và số liệu benchmark đều đã được các thành viên trong nhóm tự chạy lại, đối chiếu với oracle tính tay và kiểm chứng trước khi nộp.