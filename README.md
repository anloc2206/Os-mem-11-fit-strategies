# OS_MEM_11: First-Fit, Best-Fit và Worst-Fit

Mô phỏng cấp phát và thu hồi vùng nhớ liên tục, hiển thị memory map,
phân mảnh trong/ngoài và so sánh 3 chiến lược.

- **Môn học:** Hệ điều hành
- **Giảng viên:** Mai Ngọc Châu
- **Lớp:** 012012500102
- **Nhóm:** OS_2627102_08
- **Trưởng nhóm:** Hồ An Lộc (GitHub: anloc2206)

## 1. Thành viên

| STT | Họ tên | MSSV | GitHub |
|---|---|---|---|
| 1 | Hồ An Lộc (trưởng nhóm) | tkgithub: anloc2206 |
| 2 | Trần Huy Bảo | Đang cập nhật |
| 3 | Vũ Minh Khôi  | Đang cập nhật |
| 4 | Phạm Minh Tân |  Đang cập nhật |
| 5 | Nguyễn Hưng Duy | Đang cập nhật |

## 2. Phân công công việc

Dự án được chia thành 5 mảng việc. Nhóm sẽ chốt người phụ trách từng mảng
dựa trên thế mạnh của từng thành viên sau buổi họp nhóm đầu tiên, và cập
nhật lại bảng này trong README ngay sau đó. Mỗi mảng có một người chịu
trách nhiệm chính và một người kiểm tra chéo.

| Mảng việc | Nội dung chính | Người phụ trách |
|---|---|---|
| A. Lõi bộ nhớ | Cấu trúc block, cấp phát, tách block, thu hồi và gộp lỗ trống | Sẽ chốt sau họp nhóm |
| B. Chiến lược và phân mảnh | First-Fit, Best-Fit, Worst-Fit, tính phân mảnh trong/ngoài | Sẽ chốt sau họp nhóm |
| C. Giao diện | Vẽ memory map, nhập yêu cầu, hiển thị số liệu và biểu đồ | Sẽ chốt sau họp nhóm |
| D. Kiểm thử và hiệu năng | Bộ test, workload ngẫu nhiên, đo hiệu năng, xuất CSV | Sẽ chốt sau họp nhóm |
| E. Điều phối và báo cáo | Quản lý repo, tiến độ, review, tổng hợp báo cáo và video | Trưởng nhóm |

## 3. Đặc tả bài toán

**Đầu vào**
- Tổng dung lượng bộ nhớ (KB).
- Chuỗi yêu cầu: cấp phát (mã tiến trình, kích thước) hoặc thu hồi (mã tiến trình).
- Chiến lược: First-Fit, Best-Fit hoặc Worst-Fit.

**Đầu ra**
- Memory map sau mỗi thao tác.
- Số liệu phân mảnh trong và phân mảnh ngoài.
- Bảng và biểu đồ so sánh 3 chiến lược; kết quả xuất ra file CSV.

**Phạm vi**
- Chỉ xét cấp phát bộ nhớ liên tục. Không làm paging, segmentation, bộ nhớ ảo.
- Các giả định chi tiết (đơn vị cấp phát, cách làm tròn kích thước) sẽ được
  chốt ở tuần 2 và ghi vào tài liệu.

## 4. Công nghệ
- Ngôn ngữ: Python
- Quản lý mã nguồn: Git, GitHub

## 5. Cấu trúc thư mục
- `source/`: mã nguồn
- `input/`: dữ liệu và bộ test đầu vào
- `output/`: kết quả CSV, biểu đồ
- `report/`: báo cáo, slide, link video

## 6. Kế hoạch 8 tuần

| Tuần | Nội dung | Trạng thái |
|---|---|---|
| 1 | Chọn đề tài, phân vai, đặc tả và repo | Đang thực hiện |
| 2 | Mô hình/pseudocode và test oracle | Chưa bắt đầu |
| 3–4 | Hiện thực lõi thuật toán | Chưa bắt đầu |
| 5 | GUI, CSV, trực quan hóa | Chưa bắt đầu |
| 6 | Kiểm thử đúng đắn và hiệu năng | Chưa bắt đầu |
| 7 | Hoàn thiện, review chéo và sửa lỗi | Chưa bắt đầu |
| 8 | Báo cáo, video, demo và bảo vệ ngắn | Chưa bắt đầu |

Tiến độ chi tiết theo từng tuần xem tại [PROGRESS.md](PROGRESS.md).

## 7. Cách chạy
Sẽ cập nhật khi có mã nguồn.

## 8. Nguồn tham khảo
Sẽ cập nhật (giáo trình, sách, bài báo, tài liệu môn học). Mọi nội dung
mượn sẽ được trích dẫn; nếu có dùng AI, nhóm sẽ khai báo rõ.
