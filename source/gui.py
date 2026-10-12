import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from memory import UNIT, MemoryManager
from strategies import STRATEGIES
import io_csv
import metrics
import simulator


class MemorySimApp:

    def __init__(self, root):
        self.root = root
        self.root.title("OS_MEM_11 - Mô phỏng Quản lý Bộ nhớ")
        self.root.geometry("900x650")
        self.memory_manager = None
        self.strategy_var = tk.StringVar(value="first_fit")
        self.requests_data = []
        self.build_ui()
        self.init_default()

    def build_ui(self):
        # 1. Khung Khởi tạo
        f1 = ttk.LabelFrame(
            self.root, text="1. Khởi tạo & Cấu hình", padding=8
        )
        f1.pack(fill="x", padx=10, pady=5)
        ttk.Label(f1, text="Tổng bộ nhớ (KB):").pack(side="left", padx=5)
        self.e_total = ttk.Entry(f1, width=8)
        self.e_total.pack(side="left", padx=5)
        self.e_total.insert(0, "1000")
        ttk.Button(f1, text="Khởi tạo", command=self.do_init).pack(
            side="left", padx=5
        )

        # 2. Khung Thao tác
        f2 = ttk.LabelFrame(self.root, text="2. Thao tác & Chiến lược", padding=8)
        f2.pack(fill="x", padx=10, pady=5)
        ttk.Label(f2, text="Chiến lược:").grid(row=0, column=0, padx=5)
        ttk.Combobox(
            f2,
            textvariable=self.strategy_var,
            values=list(STRATEGIES.keys()),
            state="readonly",
            width=12,
        ).grid(row=0, column=1, padx=5)

        ttk.Label(f2, text="PID:").grid(row=0, column=2, padx=5)
        self.e_pid = ttk.Entry(f2, width=8)
        self.e_pid.grid(row=0, column=3, padx=5)

        ttk.Label(f2, text="Size:").grid(row=0, column=4, padx=5)
        self.e_size = ttk.Entry(f2, width=8)
        self.e_size.grid(row=0, column=5, padx=5)

        ttk.Button(f2, text="Cấp phát", command=self.do_alloc).grid(
            row=0, column=6, padx=5
        )
        ttk.Button(f2, text="Thu hồi", command=self.do_free).grid(
            row=0, column=7, padx=5
        )

        # 3. Khung Tiện ích CSV & So sánh
        f3 = ttk.LabelFrame(self.root, text="3. File & So sánh", padding=8)
        f3.pack(fill="x", padx=10, pady=5)
        ttk.Button(f3, text="Mở CSV", command=self.do_load_csv).pack(
            side="left", padx=5
        )
        ttk.Button(f3, text="So sánh 3 chiến lược", command=self.do_compare).pack(
            side="left", padx=5
        )
        ttk.Button(f3, text="Xuất Trace CSV", command=self.do_export).pack(
            side="left", padx=5
        )

        # 4. Khung Hiển thị Map & Phân mảnh
        f4 = ttk.LabelFrame(
            self.root, text="4. Bản đồ Bộ nhớ & Phân mảnh", padding=8
        )
        f4.pack(fill="both", expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(f4, bg="white", height=140)
        self.canvas.pack(fill="x", padx=5, pady=5)
        self.lbl_metrics = ttk.Label(
            f4, text="Phân mảnh ngoài: 0.0 | Phân mảnh trong: 0 KB"
        )
        self.lbl_metrics.pack(anchor="w", padx=5, pady=5)

    def init_default(self):
        try:
            self.memory_manager = MemoryManager(1000)
            self.update_display()
        except:
            pass

    def do_init(self):
        try:
            total = int(self.e_total.get())
            if total <= 0:
                raise ValueError
            self.memory_manager = MemoryManager(total)
            self.update_display()
            messagebox.showinfo("Thành công", f"Đã tạo bộ nhớ {total} KB.")
        except ValueError:
            messagebox.showerror(
                "Lỗi", "Dung lượng bộ nhớ phải là số nguyên lớn hơn 0!"
            )

    def do_alloc(self):
        if not self.memory_manager:
            return messagebox.showwarning("Cảnh báo", "Chưa khởi tạo bộ nhớ!")
        pid, size_str = self.e_pid.get().strip(), self.e_size.get().strip()
        if not pid:
            return messagebox.showwarning("Cảnh báo", "PID không được trống!")
        try:
            size = int(size_str)
        except ValueError:
            return messagebox.showerror(
                "Lỗi", "Kích thước (Size) phải là số nguyên!"
            )

        strat = STRATEGIES[self.strategy_var.get()]
        if self.memory_manager.allocate(pid, size, strat):
            self.update_display()
            self.e_pid.delete(0, tk.END)
            self.e_size.delete(0, tk.END)
        else:
            messagebox.showwarning(
                "Thất bại", "Không thể cấp phát (Hết chỗ hoặc trùng PID)."
            )

    def do_free(self):
        if not self.memory_manager:
            return messagebox.showwarning("Cảnh báo", "Chưa khởi tạo bộ nhớ!")
        pid = self.e_pid.get().strip()
        if not pid:
            return messagebox.showwarning("Cảnh báo", "Vui lòng nhập PID cần thu hồi!")
        if self.memory_manager.free(pid):
            self.update_display()
            self.e_pid.delete(0, tk.END)
            messagebox.showinfo("Thành công", f"Đã thu hồi tiến trình {pid}.")
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy tiến trình {pid}.")

    def do_load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            total, reqs = io_csv.read_requests(path)
            self.memory_manager = MemoryManager(total)
            self.requests_data = reqs
            strat = STRATEGIES[self.strategy_var.get()]
            for act, pid, sz in reqs:
                if act == "alloc":
                    self.memory_manager.allocate(pid, sz, strat)
                elif act == "free":
                    self.memory_manager.free(pid)
            self.update_display()
            messagebox.showinfo(
                "Thành công", f"Đã nạp thành công {len(reqs)} yêu cầu từ CSV!"
            )
        except Exception as e:
            messagebox.showerror("Lỗi CSV", str(e))

    def do_compare(self):
        total = (
            sum(b[1] for b in self.memory_manager.snapshot())
            if self.memory_manager
            else 1000
        )
        reqs = (
            self.requests_data
            if self.requests_data
            else [("alloc", "P1", 100)]
        )

        win = tk.Toplevel(self.root)
        win.title("So sánh 3 chiến lược")
        win.geometry("550+250")

        tree = ttk.Treeview(
            win,
            columns=("strat", "succ", "ext", "int"),
            show="headings",
            height=4,
        )
        for col, text in zip(
            ("strat", "succ", "ext", "int"),
            (
                "Chiến lược",
                "Thành công",
                "Phân mảnh ngoài",
                "Phân mảnh trong (KB)",
            ),
        ):
            tree.heading(col, text=text)
            tree.column(col, width=130, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for name in STRATEGIES:
            trace = simulator.run_simulation(total, reqs, name)
            if trace:
                last = trace[-1]
                succ = sum(int(r["success"]) for r in trace)
                tree.insert(
                    "",
                    "end",
                    values=(
                        name,
                        f"{succ}/{len(reqs)}",
                        f"{float(last['external_frag']):.4f}",
                        last["internal_frag"],
                    ),
                )

    def do_export(self):
        if not self.requests_data:
            return messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu yêu cầu!")
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return
        try:
            total = sum(b[1] for b in self.memory_manager.snapshot())
            trace = simulator.run_simulation(
                total, self.requests_data, self.strategy_var.get()
            )
            io_csv.write_trace(path, trace)
            messagebox.showinfo("Thành công", f"Đã xuất file tại:\n{path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_display(self):
        self.canvas.delete("all")
        if not self.memory_manager:
            return
        snap = self.memory_manager.snapshot()
        total = sum(b[1] for b in snap)
        w = max(self.canvas.winfo_width(), 850)

        x, y1, y2 = 20, 25, 105
        usable = w - 40
        colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF"]
        p_map, idx = {}, 0

        for start, size, pid, _ in snap:
            if pid and pid not in p_map:
                p_map[pid] = colors[idx % len(colors)]
                idx += 1
            r_w = (size / total) * usable
            x_end = x + r_w
            color = p_map.get(pid, "#D3D3D3")

            self.canvas.create_rectangle(
                x, y1, x_end, y2, fill=color, outline="black"
            )
            self.canvas.create_text(
                (x + x_end) / 2,
                (y1 + y2) / 2,
                text=f"{pid}\n({size}K)" if pid else f"Hole\n({size}K)",
                font=("Arial", 8, "bold"),
            )
            self.canvas.create_text(x, y2 + 12, text=str(start), font=("Arial", 7))
            x = x_end
        self.canvas.create_text(x, y2 + 12, text=str(total), font=("Arial", 7))

        self.lbl_metrics.config(
            text=f"Phân mảnh ngoài: {metrics.external_fragmentation(snap):.4f}  |  Phân mảnh trong: {metrics.internal_fragmentation(snap)} KB"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimApp(root)
    root.mainloop()
