# Theo dõi tiến độ dự án OS_MEM_11

- **Môn:** Hệ điều hành
- **Nhóm:** OS_2627102_08

## Bảng checklist chi tiết theo tuần

- [x] **Tuần 1: Chọn đề tài, phân vai, đặc tả và repo**
  - [x] Tạo GitHub repository công khai (`Os-mem-11-fit-strategies`).
  - [x] Thiết lập cấu trúc thư mục (`source/`, `input/`, `output/`, `report/`).
  - [x] Viết README ban đầu và phân công nhiệm vụ nhóm.

- [x] **Tuần 2: Mô hình / Pseudocode và Test Oracle**
  - [x] Hoàn thiện tài liệu giải thuật và pseudocode cho 3 chiến lược (`First-Fit`, `Best-Fit`, `Worst-Fit`).
  - [x] Xây dựng bảng Test Oracle chuẩn cho các trường hợp kiểm thử tay (`report/pseudocode.md`).

- [x] **Tuần 3 - 4: Hiện thực lõi thuật toán và các chiến lược**
  - [x] Hoàn thành `memory.py` (Quản lý vùng nhớ, cấp phát, thu hồi, gộp lỗ, kiểm tra bất biến `check_invariants`).
  - [x] Hoàn thành `strategies.py` và `metrics.py` (3 thuật toán và hàm tính phân mảnh trong/ngoài).
  - [x] Viết và chạy thành công các Unit Test đạt trạng thái `OK`.

- [x] **Tuần 5: Giao diện GUI, CSV và Trực quan hóa**
  - [x] Hoàn thành giao diện Tkinter (`gui.py`) với Memory Map, KPI cards và bảng chi tiết block.
  - [x] Hiện thực đọc/kiểm tra lỗi file CSV (`io_csv.py`), bộ mô phỏng (`simulator.py`) và CLI (`main.py`).
  - [x] Bổ sung đủ bộ file CSV mẫu (`input/case_*.csv`) bao gồm các ca biên, lỗi và workload phân tách FF/BF/WF.

- [x] **Tuần 6: Kiểm thử đúng đắn và Hiệu năng**
  - [x] Hoàn thiện kiểm thử tích hợp dùng `STRATEGIES` thật và kiểm thử input rỗng/không hợp lệ (`test_integration.py`).
  - [x] Chạy stress test và benchmark hiệu năng trên cỡ 100 → 100.000 yêu cầu (`benchmark.py` → `output/benchmark.csv`).
  - [x] Xuất trace 3 chiến lược, `output/compare.csv` và vẽ 2 biểu đồ `chart_compare.png`, `chart_benchmark.png`.

- [x] **Tuần 7: Hoàn thiện, Review chéo và Sửa lỗi**
  - [x] Thực hiện review chéo và sửa toàn bộ lỗi phát hiện (`memory.py` kiểm tra `total_size % unit`, chặn `bool`; `gui.py` lưu `self.history` & `self.total`, bắt lỗi nhập liệu không crash).
  - [x] Hoàn thiện bảng kiểm thử đối chiếu oracle (`output/test_table.csv` — 32/32 PASS) và chạy toàn bộ 46/46 test `OK`.
  - [x] Cập nhật hoàn chỉnh `README.md` và `PROGRESS.md`.

- [ ] **Tuần 8: Báo cáo, Video demo và Nộp bài**
  - [ ] Ghép nội dung báo cáo chi tiết (8 - 12 trang) trong `report/`.
  - [ ] Quay và công khai video demo luồng chạy, dữ liệu mẫu, kết quả và kiểm thử.
  - [ ] Cập nhật link video demo vào `README.md` và báo cáo trước khi nộp.