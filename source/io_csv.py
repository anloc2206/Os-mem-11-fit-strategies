"""Đọc file CSV yêu cầu đầu vào và ghi file trace kết quả (Task 5)."""
import csv
import os

# Các cột của file trace, đúng thứ tự theo hợp đồng chung của nhóm
TRACE_COLUMNS = [
    "step", "strategy", "action", "pid", "size", "success",
    "free_total", "largest_hole", "external_frag", "internal_frag",
]


def _to_positive_int(text):
    """Đổi chuỗi thành số nguyên dương; không hợp lệ thì trả về None."""
    text = text.strip()
    if text.isdigit() and int(text) > 0:
        return int(text)
    return None


def read_requests(path):
    """Đọc file CSV, trả về (total, requests); sai dữ liệu thì raise ValueError 'dòng N: lý do'.

    Đầu vào : đường dẫn file CSV có tiêu đề action,pid,size; dòng đầu tiên của dữ liệu là init.
    Đầu ra  : total = tổng bộ nhớ (KB); requests = list các tuple (action, pid, size),
              với free thì size = None.
    """
    if not os.path.isfile(path):
        raise ValueError(f"Không tìm thấy file: {path}")

    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
    except UnicodeDecodeError:
        raise ValueError("File không đọc được, hãy lưu file ở dạng UTF-8")

    # File rỗng hoặc chỉ toàn dòng trắng
    if not any(any(cell.strip() for cell in row) for row in rows):
        raise ValueError("File rỗng")

    # Dòng 1: tiêu đề, phải có đủ 3 cột (thứ tự cột nào cũng được)
    header = [cell.strip().lower() for cell in rows[0]]
    missing = [name for name in ("action", "pid", "size") if name not in header]
    if missing:
        raise ValueError("dòng 1: thiếu cột " + ", ".join(missing))
    col = {name: header.index(name) for name in ("action", "pid", "size")}

    def cell_of(row, name):
        # Lấy giá trị của một cột; dòng ngắn hơn thì coi như ô trống
        i = col[name]
        return row[i].strip() if i < len(row) else ""

    total = None
    requests = []
    for line_no, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue  # bỏ qua dòng trắng
        action = cell_of(row, "action").lower()
        pid = cell_of(row, "pid")
        size_text = cell_of(row, "size")

        if total is None:  # dòng dữ liệu đầu tiên bắt buộc là init
            if action != "init":
                raise ValueError(f"dòng {line_no}: dòng dữ liệu đầu tiên phải là init (ví dụ: init,,1000)")
            total = _to_positive_int(size_text)
            if total is None:
                raise ValueError(f"dòng {line_no}: init cần size là số nguyên dương, nhận được '{size_text}'")
            continue

        if action == "init":
            raise ValueError(f"dòng {line_no}: init chỉ được có một lần ở dòng dữ liệu đầu tiên")
        if action not in ("alloc", "free"):
            raise ValueError(f"dòng {line_no}: action '{action}' không hợp lệ (chỉ có init, alloc, free)")
        if pid == "":
            raise ValueError(f"dòng {line_no}: pid không được để trống")

        if action == "alloc":
            size = _to_positive_int(size_text)
            if size is None:
                raise ValueError(f"dòng {line_no}: alloc cần size là số nguyên dương, nhận được '{size_text}'")
            requests.append(("alloc", pid, size))
        else:
            requests.append(("free", pid, None))

    if total is None:
        raise ValueError("File không có dữ liệu: thiếu dòng init")
    return total, requests


def write_trace(path, rows):
    """Ghi file trace CSV theo TRACE_COLUMNS (rows là list dict do run_simulation trả về)."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)  # tự tạo thư mục output nếu chưa có
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
