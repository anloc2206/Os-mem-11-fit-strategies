# Theo dõi tiến độ dự án OS_MEM_11

Môn: Hệ điều hành 
Nhóm: OS_2627102_08

## Bảng checklist chi tiết theo tuần

- [x] **Tuần 1: Chọn đề tài, phân vai, đặc tả và repo**
  - [x] Tạo GitHub repository công khai (`Os-mem-11-fit-strategies`).
  - [x] Thiết lập cấu trúc thư mục (`source/`, `input/`, `output/`, `report/`).
  - [x] Viết README ban đầu và phân công nhiệm vụ nhóm.

- [x] **Tuần 2: Mô hình / Pseudocode và Test Oracle**
  - [x] Hoàn thiện tài liệu giải thuật và pseudocode cho 3 chiến lược (`First-Fit`, `Best-Fit`, `Worst-Fit`)[cite: 1].
  - [x] Xây dựng bảng Test Oracle chuẩn cho các trường hợp kiểm thử tay[cite: 1].

- [x] **Tuần 3 - 4: Hiện thực lõi thuật toán và các chiến lược**
  - [x] Hoàn thành `memory.py` (Quản lý vùng nhớ, cấp phát, thu hồi, gộp lỗ, kiểm tra bất biến `check_invariants`)[cite: 1].
  - [x] Hoàn thành `strategies.py` và `metrics.py` (3 thuật toán và hàm tính phân mảnh trong/ngoài)[cite: 1].
  - [x] Viết và chạy thành công các Unit Test đạt trạng thái `OK`[cite: 7].

- [ ] **Tuần 5: Giao diện GUI, CSV và Trực quan hóa**
  - [x] Hoàn thành giao diện Tkinter (`gui.py`)[cite: 3].
  - [x] Hiện thực đọc/kiểm tra lỗi file CSV (`io_csv.py`) và bộ mô phỏng (`simulator.py`)[cite: 1].

- [ ] **Tuần 6: Kiểm thử đúng đắn và Hiệu năng**
  - [x] Viết kiểm thử tích hợp và kiểm thử biên (`test_integration.py`)[cite: 1].
  - [ ] Chạy benchmark đánh giá hiệu năng (`benchmark.py`)[cite: 1].

- [ ] **Tuần 7: Hoàn thiện, Review chéo và Sửa lỗi**
  - [ ] Thực hiện review chéo giữa các thành viên[cite: 1].
  - [ ] Hoàn thiện bảng kiểm thử (`test_table.csv`)[cite: 1].

- [ ] **Tuần 8: Báo cáo, Video demo và Nộp bài**
  - [ ] Ghép nội dung báo cáo chi tiết (8 - 12 trang)[cite: 1].
  - [ ] Quay và công khai video demo luồng chạy, dữ liệu mẫu[cite: 1].
