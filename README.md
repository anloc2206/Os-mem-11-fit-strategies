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
| 1 | Hồ An Lộc | 082207006118    | anloc2206 |
| 2 | Trần Huy Bảo | 079207005017 |huybaotran307-thb|
| 3 | Vũ Minh Khôi | 075207011378  | khoiminhvu2303-sudo |
| 4 | Phạm Minh Tân |  079207043105 |
| 5 | Nguyễn Hưng Duy | 079207019278|ngduymeomeo|

## 2. Phân công công việc

Dự án được chia thành 5 mảng việc nhằm đảm bảo khối lượng lập trình và báo cáo cân bằng cho cả 5 thành viên. Mỗi mảng có một người chịu trách nhiệm chính và một người kiểm tra chéo (review chéo mã nguồn của nhau trước khi gộp nhánh).

| Mảng việc | Nội dung chính | Người phụ trách |
|---|---|---|
| **A. Lõi bộ nhớ** | Cấu trúc block, hàm cấp phát, tách block, thu hồi và gộp lỗ trống | Trần Huy Bảo |
| **B. Chiến lược và thuật toán** | Xây dựng logic First-Fit, Best-Fit, Worst-Fit và tính phân mảnh | Vũ Minh Khôi |
| **C. Giao diện và Điều phối** | Code giao diện Tkinter (memory map) và quản lý tiến độ, repo chung | Hồ An Lộc (Leader) |
| **D. Mô phỏng và xử lý dữ liệu** | Đọc/ghi file input/output CSV, kết nối Simulator chạy luồng chính | Phạm Minh Tân |
| **E. Kiểm thử và hiệu năng** | Viết test tích hợp, sinh workload ngẫu nhiên, đo benchmark hiệu năng | Nguyễn Hưng Duy |
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
| 1 | Chọn đề tài, phân vai, đặc tả và repo | Đã thực hiện|
| 2 | Mô hình/pseudocode và test oracle | Đã thực hiện |
| 3–4 | Hiện thực lõi thuật toán | Đã thực hiện |
| 5 | GUI, CSV, trực quan hóa | Đang tiến hành |
| 6 | Kiểm thử đúng đắn và hiệu năng | Chưa bắt đầu |
| 7 | Hoàn thiện, review chéo và sửa lỗi | Chưa bắt đầu |
| 8 | Báo cáo, video, demo và bảo vệ ngắn | Chưa bắt đầu |

Tiến độ chi tiết theo từng tuần xem tại [PROGRESS.md](PROGRESS.md).


## 7. Nguồn tham khảo
Sẽ cập nhật (giáo trình, sách, bài báo, tài liệu môn học). Mọi nội dung
mượn sẽ được trích dẫn; nếu có dùng AI, nhóm sẽ khai báo rõ.
