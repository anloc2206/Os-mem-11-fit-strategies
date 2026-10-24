
from typing import List, Optional


def first_fit(holes: List[int], size: int) -> Optional[int]:
    """Chiến lược First-Fit: Duyệt qua danh sách các lỗ trống theo thứ tự địa chỉ và chọn lỗ trống đầu tiên có kích thước đủ chứa tiến trình
    
    Trả về chỉ số (index) của lỗ trống trong danh sách, hoặc None nếu không có lỗ nào đủ chỗ
    """
    for i, h in enumerate(holes):
        if h >= size:
            return i
    return None


def best_fit(holes: List[int], size: int) -> Optional[int]:
    """Chiến lược Best-Fit: Lọc qua toàn bộ danh sách lỗ trống để chọn ra lỗ trống có kích thước nhỏ nhất (đủ chứa tiến trình)
    
    Trả về chỉ số của lỗ trống phù hợp nhất, hoặc None nếu không có lỗ nào đủ chỗ
    """
    best_idx: Optional[int] = None
    best_size: Optional[int] = None
    for i, h in enumerate(holes):
        if h >= size and (best_size is None or h < best_size):
            best_size = h
            best_idx = i
    return best_idx


def worst_fit(holes: List[int], size: int) -> Optional[int]:
    """Chiến lược Worst-Fit: Lọc qua toàn bộ danh sách lỗ trống để chọn ra lỗ trống có kích thước lớn nhất
    
    Trả về chỉ số của lỗ trống lớn nhất để lại phần dư lớn sau khi cấp phát, hoặc None nếu không có lỗ nào đủ chỗ
    """
    worst_idx: Optional[int] = None
    worst_size: int = -1
    for i, h in enumerate(holes):
        if h >= size and h > worst_size:
            worst_size = h
            worst_idx = i
    return worst_idx



STRATEGIES = {
    "first_fit": first_fit,
    "best_fit": best_fit,
    "worst_fit": worst_fit,
}