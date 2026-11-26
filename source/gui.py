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
        self.root.geometry("980x700")
        self.root.minsize(860, 620)
        self.root.configure(bg="#F4F6F9")

        self.memory_manager = None
        self.strategy_var = tk.StringVar(value="first_fit")
        self.requests_data = []

        self.setup_style()
        self.build_ui()
        self.init_default()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#F4F6F9"
        card_bg = "#FFFFFF"
        primary = "#2563EB"
        primary_hover = "#1D4ED8"

        style.configure("TFrame", background=bg)
        style.configure("Card.TLabelframe", background=card_bg, borderwidth=1, relief="solid")
        style.configure(
            "Card.TLabelframe.Label",
            background=card_bg,
            foreground="#1E293B",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("TLabel", background=card_bg, foreground="#334155", font=("Segoe UI", 9))
        style.configure("Header.TLabel", background=bg, foreground="#0F172A", font=("Segoe UI", 13, "bold"))
        style.configure("Metric.TLabel", background=card_bg, foreground="#0F172A", font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", padding=4)
        style.configure("TCombobox", padding=4)

        style.configure(
            "Primary.TButton",
            background=primary,
            foreground="white",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 5),
            borderwidth=0,
        )
        style.map("Primary.TButton", background=[("active", primary_hover)])

        style.configure(
            "Secondary.TButton",
            background="#E2E8F0",
            foreground="#1E293B",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 5),
            borderwidth=0,
        )
        style.map("Secondary.TButton", background=[("active", "#CBD5E1")])

        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#E2E8F0", foreground="#0F172A")

    def build_ui(self):
        # Thanh tiêu đề
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=16, pady=(12, 4))
        ttk.Label(header, text="MÔ PHỎNG CẤP PHÁT & QUẢN LÝ BỘ NHỚ", style="Header.TLabel").pack(side="left")

        # Hàng trên: Khung 1 (Khởi tạo) & Khung 3 (File & So sánh)
        top_row = ttk.Frame(self.root)
        top_row.pack(fill="x", padx=16, pady=6)

        f1 = ttk.LabelFrame(top_row, text=" 1. Khởi tạo & Cấu hình ", style="Card.TLabelframe", padding=10)
        f1.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ttk.Label(f1, text="Tổng bộ nhớ (KB):").pack(side="left", padx=(0, 6))
        self.e_total = ttk.Entry(f1, width=10)
        self.e_total.pack(side="left", padx=(0, 8))
        self.e_total.insert(0, "1000")
        ttk.Button(f1, text="Khởi tạo", style="Primary.TButton", command=self.do_init).pack(side="left")

        f3 = ttk.LabelFrame(top_row, text=" 3. Kịch bản CSV & Đối chiếu ", style="Card.TLabelframe", padding=10)
        f3.pack(side="left", fill="both", expand=True, padx=(8, 0))
        ttk.Button(f3, text="Mở CSV", style="Secondary.TButton", command=self.do_load_csv).pack(side="left", padx=4)
        ttk.Button(f3, text="So sánh 3 chiến lược", style="Primary.TButton", command=self.do_compare).pack(side="left", padx=4)
        ttk.Button(f3, text="Xuất Trace CSV", style="Secondary.TButton", command=self.do_export).pack(side="left", padx=4)

        # Khung 2: Thao tác & Chiến lược
        f2 = ttk.LabelFrame(self.root, text=" 2. Thao tác & Chiến lược ", style="Card.TLabelframe", padding=10)
        f2.pack(fill="x", padx=16, pady=6)

        ttk.Label(f2, text="Chiến lược:").pack(side="left", padx=(0, 6))
        ttk.Combobox(
            f2,
            textvariable=self.strategy_var,
            values=list(STRATEGIES.keys()),
            state="readonly",
            width=14,
        ).pack(side="left", padx=(0, 14))

        ttk.Label(f2, text="PID:").pack(side="left", padx=(0, 6))
        self.e_pid = ttk.Entry(f2, width=10)
        self.e_pid.pack(side="left", padx=(0, 14))

        ttk.Label(f2, text="Size (KB):").pack(side="left", padx=(0, 6))
        self.e_size = ttk.Entry(f2, width=10)
        self.e_size.pack(side="left", padx=(0, 16))

        ttk.Button(f2, text="+ Cấp phát", style="Primary.TButton", command=self.do_alloc).pack(side="left", padx=4)
        ttk.Button(f2, text="- Thu hồi", style="Secondary.TButton", command=self.do_free).pack(side="left", padx=4)

        # Khung 4: Bản đồ Bộ nhớ & Phân mảnh
        f4 = ttk.LabelFrame(self.root, text=" 4. Bản đồ Bộ nhớ & Chỉ số Phân mảnh ", style="Card.TLabelframe", padding=12)
        f4.pack(fill="both", expand=True, padx=16, pady=(6, 14))

        self.canvas = tk.Canvas(f4, bg="#F8FAFC", height=135, highlightthickness=1, highlightbackground="#CBD5E1")
        self.canvas.pack(fill="x", pady=(2, 8))
        self.canvas.bind("<Configure>", lambda _e: self.update_display())

        # Dòng chỉ số & chú thích màu
        info_bar = ttk.Frame(f4, style="Card.TLabelframe")
        info_bar.pack(fill="x", pady=(0, 8))
        self.lbl_metrics = ttk.Label(
            info_bar,
            text="Phân mảnh ngoài: 0.0000   |   Phân mảnh trong: 0 KB",
            style="Metric.TLabel",
        )
        self.lbl_metrics.pack(side="left")

        legend = ttk.Frame(info_bar, style="Card.TLabelframe")
        legend.pack(side="right")
        tk.Label(legend, text="  ", bg="#3B82F6", relief="solid", bd=1).pack(side="left", padx=(0, 4))
        ttk.Label(legend, text="Tiến trình đang cấp phát").pack(side="left", padx=(0, 12))
        tk.Label(legend, text="  ", bg="#E2E8F0", relief="solid", bd=1).pack(side="left", padx=(0, 4))
        ttk.Label(legend, text="Vùng trống (Hole)").pack(side="left")

        # Bảng chi tiết từng block bên dưới bản đồ
        cols = ("idx", "range", "size", "status", "req", "int_frag")
        self.block_tree = ttk.Treeview(f4, columns=cols, show="headings", height=7)
        headers = {
            "idx": "#",
            "range": "Khoảng địa chỉ",
            "size": "Kích thước (KB)",
            "status": "Trạng thái / PID",
            "req": "Yêu cầu thực (KB)",
            "int_frag": "Phân mảnh trong (KB)",
        }
        widths = {"idx": 50, "range": 150, "size": 130, "status": 160, "req": 140, "int_frag": 150}
        for c in cols:
            self.block_tree.heading(c, text=headers[c])
            self.block_tree.column(c, width=widths[c], anchor="center")
        self.block_tree.pack(fill="both", expand=True)

    def init_default(self):
        try:
            self.memory_manager = MemoryManager(1000)
            self.update_display()
        except Exception:
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
            messagebox.showerror("Lỗi", "Dung lượng bộ nhớ phải là số nguyên lớn hơn 0!")

    def do_alloc(self):
        if not self.memory_manager:
            return messagebox.showwarning("Cảnh báo", "Chưa khởi tạo bộ nhớ!")
        pid, size_str = self.e_pid.get().strip(), self.e_size.get().strip()
        if not pid:
            return messagebox.showwarning("Cảnh báo", "PID không được trống!")
        try:
            size = int(size_str)
        except ValueError:
            return messagebox.showerror("Lỗi", "Kích thước (Size) phải là số nguyên!")

        strat = STRATEGIES[self.strategy_var.get()]
        if self.memory_manager.allocate(pid, size, strat):
            self.update_display()
            self.e_pid.delete(0, tk.END)
            self.e_size.delete(0, tk.END)
        else:
            messagebox.showwarning("Thất bại", "Không thể cấp phát (Hết chỗ hoặc trùng PID).")

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
            messagebox.showinfo("Thành công", f"Đã nạp thành công {len(reqs)} yêu cầu từ CSV!")
        except Exception as e:
            messagebox.showerror("Lỗi CSV", str(e))

    def do_compare(self):
        total = (
            sum(b[1] for b in self.memory_manager.snapshot())
            if self.memory_manager
            else 1000
        )
        reqs = self.requests_data if self.requests_data else [("alloc", "P1", 100)]

        win = tk.Toplevel(self.root)
        win.title("So sánh 3 chiến lược")
        win.geometry("600x240")
        win.configure(bg="#F4F6F9")

        tree = ttk.Treeview(
            win,
            columns=("strat", "succ", "ext", "int"),
            show="headings",
            height=4,
        )
        for col, text in zip(
            ("strat", "succ", "ext", "int"),
            ("Chiến lược", "Thành công", "Phân mảnh ngoài", "Phân mảnh trong (KB)"),
        ):
            tree.heading(col, text=text)
            tree.column(col, width=140, anchor="center")
        tree.pack(fill="both", expand=True, padx=12, pady=12)

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
        w = max(self.canvas.winfo_width(), 820)

        x, y1, y2 = 24, 24, 98
        usable = w - 48
        palette = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]
        p_map, idx = {}, 0

        for item in self.block_tree.get_children():
            self.block_tree.delete(item)

        for block_i, (start, size, pid, req) in enumerate(snap, start=1):
            if pid and pid not in p_map:
                p_map[pid] = palette[idx % len(palette)]
                idx += 1
            r_w = (size / total) * usable
            x_end = x + r_w
            fill_color = p_map.get(pid, "#E2E8F0")
            text_color = "#FFFFFF" if pid else "#475569"

            self.canvas.create_rectangle(
                x, y1, x_end, y2, fill=fill_color, outline="#334155", width=1
            )
            if r_w >= 34:
                self.canvas.create_text(
                    (x + x_end) / 2,
                    (y1 + y2) / 2,
                    text=f"{pid}\n({size}K)" if pid else f"Hole\n({size}K)",
                    fill=text_color,
                    font=("Segoe UI", 8, "bold"),
                )
            self.canvas.create_text(x, y2 + 14, text=str(start), fill="#475569", font=("Segoe UI", 8))
            x = x_end

            self.block_tree.insert(
                "",
                "end",
                values=(
                    block_i,
                    f"{start} -> {start + size}",
                    size,
                    f"Tiến trình {pid}" if pid else "Hole (Trống)",
                    req if pid else "-",
                    (size - req) if pid else 0,
                ),
            )

        self.canvas.create_text(x, y2 + 14, text=str(total), fill="#475569", font=("Segoe UI", 8))

        self.lbl_metrics.config(
            text=f"Phân mảnh ngoài: {metrics.external_fragmentation(snap):.4f}   |   Phân mảnh trong: {metrics.internal_fragmentation(snap)} KB"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimApp(root)
    root.mainloop()
