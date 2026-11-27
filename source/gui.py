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
        self.root.title("OS_MEM_11 — Memory Allocation Monitor")
        self.root.geometry("1040x740")
        self.root.minsize(900, 650)

        # Bảng màu Dark System Monitor
        self.c_bg = "#0F172A"         # Nền chính (xanh đen sâu)
        self.c_panel = "#1E293B"      # Nền card / khung
        self.c_input = "#0B1120"      # Nền ô nhập / canvas
        self.c_border = "#334155"     # Viền khung
        self.c_text = "#F1F5F9"       # Chữ chính
        self.c_muted = "#94A3B8"      # Chữ phụ
        self.c_accent = "#38BDF8"     # Nhấn xanh cyan

        self.root.configure(bg=self.c_bg)

        self.memory_manager = None
        self.strategy_var = tk.StringVar(value="first_fit")
        self.total = 1000
        self.history = []

        self.setup_style()
        self.build_ui()
        self.init_default()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Dropdown list của Combobox cũng theo nền tối
        self.root.option_add("*TCombobox*Listbox.background", self.c_panel)
        self.root.option_add("*TCombobox*Listbox.foreground", self.c_text)
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#2563EB")
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

        style.configure("TFrame", background=self.c_bg)
        style.configure("Panel.TFrame", background=self.c_panel)

        style.configure(
            "Card.TLabelframe",
            background=self.c_panel,
            borderwidth=1,
            relief="solid",
            bordercolor=self.c_border,
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.c_panel,
            foreground=self.c_accent,
            font=("Segoe UI", 9, "bold"),
        )

        style.configure("TLabel", background=self.c_panel, foreground=self.c_text, font=("Segoe UI", 9))
        style.configure("Muted.TLabel", background=self.c_panel, foreground=self.c_muted, font=("Segoe UI", 8))
        style.configure("Header.TLabel", background=self.c_bg, foreground=self.c_text, font=("Segoe UI", 14, "bold"))
        style.configure("SubHeader.TLabel", background=self.c_bg, foreground=self.c_muted, font=("Segoe UI", 9))

        style.configure(
            "Dark.TEntry",
            fieldbackground=self.c_input,
            foreground=self.c_text,
            insertcolor=self.c_text,
            bordercolor=self.c_border,
            lightcolor=self.c_border,
            darkcolor=self.c_border,
            padding=5,
        )
        style.configure(
            "Dark.TCombobox",
            fieldbackground=self.c_input,
            background=self.c_panel,
            foreground=self.c_text,
            arrowcolor=self.c_text,
            bordercolor=self.c_border,
            padding=5,
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", self.c_input)],
            foreground=[("readonly", self.c_text)],
            selectbackground=[("readonly", self.c_input)],
            selectforeground=[("readonly", self.c_text)],
        )

        # Nút phân màu theo chức năng
        def make_btn(name, bg, hover, fg="#FFFFFF"):
            style.configure(
                name,
                background=bg,
                foreground=fg,
                font=("Segoe UI", 9, "bold"),
                padding=(12, 6),
                borderwidth=0,
                focuscolor=bg,
            )
            style.map(name, background=[("active", hover), ("pressed", hover)])

        make_btn("Init.TButton", "#2563EB", "#1D4ED8")
        make_btn("Alloc.TButton", "#16A34A", "#15803D")
        make_btn("Free.TButton", "#DC2626", "#B91C1C")
        make_btn("Compare.TButton", "#0284C7", "#0369A1")
        make_btn("Neutral.TButton", "#334155", "#475569")

        # Bảng Treeview nền tối
        style.configure(
            "Dark.Treeview",
            background=self.c_input,
            foreground=self.c_text,
            fieldbackground=self.c_input,
            bordercolor=self.c_border,
            font=("Consolas", 9),
            rowheight=26,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background="#263348",
            foreground="#E2E8F0",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=(6, 6),
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#1D4ED8")],
            foreground=[("selected", "#FFFFFF")],
        )
        style.map("Dark.Treeview.Heading", background=[("active", "#334155")])

        style.configure(
            "Vertical.TScrollbar",
            background="#334155",
            troughcolor=self.c_input,
            bordercolor=self.c_input,
            arrowcolor=self.c_muted,
        )

    def _create_kpi_card(self, parent, title, default_val, accent_color):
        card = tk.Frame(parent, bg=self.c_panel, highlightbackground=self.c_border, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=4)
        bar = tk.Frame(card, bg=accent_color, height=3)
        bar.pack(fill="x", side="top")
        tk.Label(card, text=title, bg=self.c_panel, fg=self.c_muted, font=("Segoe UI", 8, "bold")).pack(
            anchor="w", padx=10, pady=(6, 0)
        )
        val_lbl = tk.Label(card, text=default_val, bg=self.c_panel, fg=self.c_text, font=("Consolas", 13, "bold"))
        val_lbl.pack(anchor="w", padx=10, pady=(2, 8))
        return val_lbl

    def build_ui(self):
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=16, pady=(12, 6))
        ttk.Label(header, text="OS_MEM_11  |  MEMORY ALLOCATION MONITOR", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="First-Fit  •  Best-Fit  •  Worst-Fit", style="SubHeader.TLabel").pack(
            side="right", pady=(4, 0)
        )

        # Hàng trên: Khung 1 (Khởi tạo) & Khung 3 (CSV & So sánh)
        top_row = ttk.Frame(self.root)
        top_row.pack(fill="x", padx=16, pady=4)

        f1 = ttk.LabelFrame(top_row, text=" 1. KHỞI TẠO BỘ NHỚ ", style="Card.TLabelframe", padding=10)
        f1.pack(side="left", fill="both", expand=True, padx=(0, 6))
        ttk.Label(f1, text=f"Tổng RAM (KB, bội của {UNIT}):").pack(side="left", padx=(0, 8))
        self.e_total = ttk.Entry(f1, width=11, style="Dark.TEntry", font=("Consolas", 10))
        self.e_total.pack(side="left", padx=(0, 10))
        self.e_total.insert(0, "1000")
        ttk.Button(f1, text="Khởi tạo", style="Init.TButton", command=self.do_init).pack(side="left")

        f3 = ttk.LabelFrame(top_row, text=" 3. KỊCH BẢN CSV & ĐỐI CHIẾU ", style="Card.TLabelframe", padding=10)
        f3.pack(side="left", fill="both", expand=True, padx=(6, 0))
        ttk.Button(f3, text="Mở CSV", style="Neutral.TButton", command=self.do_load_csv).pack(side="left", padx=4)
        ttk.Button(f3, text="So sánh 3 chiến lược", style="Compare.TButton", command=self.do_compare).pack(
            side="left", padx=4
        )
        ttk.Button(f3, text="Xuất Trace CSV", style="Neutral.TButton", command=self.do_export).pack(side="left", padx=4)

        # Khung 2: Thao tác & Chiến lược
        f2 = ttk.LabelFrame(self.root, text=" 2. THAO TÁC CẤP PHÁT & THU HỒI ", style="Card.TLabelframe", padding=10)
        f2.pack(fill="x", padx=16, pady=6)

        ttk.Label(f2, text="Chiến lược:").pack(side="left", padx=(0, 6))
        ttk.Combobox(
            f2,
            textvariable=self.strategy_var,
            values=list(STRATEGIES.keys()),
            state="readonly",
            width=13,
            style="Dark.TCombobox",
            font=("Consolas", 9),
        ).pack(side="left", padx=(0, 16))

        ttk.Label(f2, text="PID:").pack(side="left", padx=(0, 6))
        self.e_pid = ttk.Entry(f2, width=11, style="Dark.TEntry", font=("Consolas", 10))
        self.e_pid.pack(side="left", padx=(0, 16))

        ttk.Label(f2, text="Size (KB):").pack(side="left", padx=(0, 6))
        self.e_size = ttk.Entry(f2, width=11, style="Dark.TEntry", font=("Consolas", 10))
        self.e_size.pack(side="left", padx=(0, 18))

        ttk.Button(f2, text="+ Cấp phát", style="Alloc.TButton", command=self.do_alloc).pack(side="left", padx=4)
        ttk.Button(f2, text="- Thu hồi", style="Free.TButton", command=self.do_free).pack(side="left", padx=4)

        # Hàng KPI Cards
        kpi_row = ttk.Frame(self.root)
        kpi_row.pack(fill="x", padx=12, pady=(4, 6))
        self.kpi_used = self._create_kpi_card(kpi_row, "ĐÃ SỬ DỤNG", "0 / 1000 KB (0.0%)", "#38BDF8")
        self.kpi_free = self._create_kpi_card(kpi_row, "TỔNG VÙNG TRỐNG", "1000 KB (1 hole)", "#34D399")
        self.kpi_ext = self._create_kpi_card(kpi_row, "PHÂN MẢNH NGOÀI", "0.0000", "#F59E0B")
        self.kpi_int = self._create_kpi_card(kpi_row, "PHÂN MẢNH TRONG", "0 KB", "#A78BFA")

        # Khung 4: Bản đồ Bộ nhớ & Bảng chi tiết
        f4 = ttk.LabelFrame(self.root, text=" 4. BẢN ĐỒ BỘ NHỚ (MEMORY MAP) & CHI TIẾT BLOCK ", style="Card.TLabelframe", padding=10)
        f4.pack(fill="both", expand=True, padx=16, pady=(2, 8))

        self.canvas = tk.Canvas(
            f4, bg=self.c_input, height=130, highlightthickness=1, highlightbackground=self.c_border
        )
        self.canvas.pack(fill="x", pady=(2, 8))
        self.canvas.bind("<Configure>", lambda _e: self.update_display())

        # Chú thích màu
        legend = ttk.Frame(f4, style="Panel.TFrame")
        legend.pack(fill="x", pady=(0, 6))
        tk.Label(legend, text="   ", bg="#0EA5E9", relief="flat").pack(side="left", padx=(0, 5))
        ttk.Label(legend, text="Tiến trình đang cấp phát", style="Muted.TLabel").pack(side="left", padx=(0, 16))
        tk.Label(
            legend, text="   ", bg="#0B1120", highlightbackground="#64748B", highlightthickness=1
        ).pack(side="left", padx=(0, 5))
        ttk.Label(legend, text="Vùng trống (Hole)", style="Muted.TLabel").pack(side="left")

        # Bảng Treeview + Scrollbar
        tree_wrap = ttk.Frame(f4, style="Panel.TFrame")
        tree_wrap.pack(fill="both", expand=True)

        cols = ("idx", "range", "size", "status", "req", "int_frag")
        self.block_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", height=7, style="Dark.Treeview")
        headers = {
            "idx": "#",
            "range": "Khoảng địa chỉ",
            "size": "Kích thước (KB)",
            "status": "Trạng thái / PID",
            "req": "Yêu cầu thực (KB)",
            "int_frag": "Phân mảnh trong (KB)",
        }
        widths = {"idx": 50, "range": 160, "size": 135, "status": 180, "req": 145, "int_frag": 155}
        for c in cols:
            self.block_tree.heading(c, text=headers[c])
            self.block_tree.column(c, width=widths[c], anchor="center")

        self.block_tree.tag_configure("alloc_even", background="#111C2E", foreground="#F1F5F9")
        self.block_tree.tag_configure("alloc_odd", background="#162338", foreground="#F1F5F9")
        self.block_tree.tag_configure("hole_row", background="#0B1120", foreground="#64748B")

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.block_tree.yview)
        self.block_tree.configure(yscrollcommand=vsb.set)
        self.block_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Status bar ở đáy cửa sổ
        status_frame = tk.Frame(self.root, bg="#0B1120", height=26)
        status_frame.pack(fill="x", side="bottom")
        self.lbl_status = tk.Label(
            status_frame,
            text=" Sẵn sàng — Đã khởi tạo bộ nhớ mặc định 1000 KB.",
            bg="#0B1120",
            fg=self.c_muted,
            font=("Consolas", 9),
            anchor="w",
        )
        self.lbl_status.pack(fill="x", padx=12, pady=4)

    def set_status(self, msg, level="info"):
        colors = {"info": "#94A3B8", "ok": "#4ADE80", "warn": "#FBBF24", "err": "#F87171"}
        self.lbl_status.config(text=f" {msg}", fg=colors.get(level, "#94A3B8"))

    def init_default(self):
        try:
            self.total = 1000
            self.history = []
            self.memory_manager = MemoryManager(self.total)
            self.update_display()
        except Exception:
            pass

    def do_init(self):
        raw = self.e_total.get().strip()
        if not raw:
            self.set_status("[LỖI] Chưa nhập tổng dung lượng bộ nhớ.", "err")
            return messagebox.showerror("Lỗi", "Vui lòng nhập tổng dung lượng bộ nhớ!")
        try:
            total = int(raw)
        except ValueError:
            self.set_status(f"[LỖI] Tổng bộ nhớ không hợp lệ: '{raw}'.", "err")
            return messagebox.showerror("Lỗi", "Dung lượng bộ nhớ phải là số nguyên dương!")
        try:
            self.memory_manager = MemoryManager(total)
            self.total = total
            self.history = []
            self.update_display()
            self.set_status(f"[OK] Đã khởi tạo bộ nhớ mới: {total} KB (UNIT={UNIT}).", "ok")
        except ValueError as e:
            self.set_status(f"[LỖI] {e}", "err")
            messagebox.showerror("Lỗi", str(e))

    def do_alloc(self):
        if not self.memory_manager:
            return messagebox.showwarning("Cảnh báo", "Chưa khởi tạo bộ nhớ!")
        pid, size_str = self.e_pid.get().strip(), self.e_size.get().strip()
        if not pid:
            self.set_status("[CẢNH BÁO] PID không được để trống.", "warn")
            return messagebox.showwarning("Cảnh báo", "PID không được trống!")
        if not size_str:
            self.set_status("[CẢNH BÁO] Chưa nhập kích thước (Size).", "warn")
            return messagebox.showwarning("Cảnh báo", "Vui lòng nhập kích thước (Size)!")
        try:
            size = int(size_str)
        except ValueError:
            self.set_status(f"[LỖI] Size không phải số nguyên: '{size_str}'.", "err")
            return messagebox.showerror("Lỗi", "Kích thước (Size) phải là số nguyên!")
        if size <= 0:
            self.set_status(f"[LỖI] Size phải > 0 (nhận được {size}).", "err")
            return messagebox.showerror("Lỗi", "Kích thước (Size) phải lớn hơn 0!")

        strat_name = self.strategy_var.get()
        self.history.append(("alloc", pid, size))
        if self.memory_manager.allocate(pid, size, STRATEGIES[strat_name]):
            self.update_display()
            self.e_pid.delete(0, tk.END)
            self.e_size.delete(0, tk.END)
            self.set_status(f"[OK] Đã cấp phát {pid} ({size} KB) bằng {strat_name}.", "ok")
        else:
            self.set_status(f"[THẤT BẠI] Không thể cấp phát {pid} ({size} KB) — hết chỗ hoặc trùng PID.", "warn")
            messagebox.showwarning("Thất bại", "Không thể cấp phát (Hết chỗ hoặc trùng PID).")

    def do_free(self):
        if not self.memory_manager:
            return messagebox.showwarning("Cảnh báo", "Chưa khởi tạo bộ nhớ!")
        pid = self.e_pid.get().strip()
        if not pid:
            self.set_status("[CẢNH BÁO] Chưa nhập PID cần thu hồi.", "warn")
            return messagebox.showwarning("Cảnh báo", "Vui lòng nhập PID cần thu hồi!")

        self.history.append(("free", pid, None))
        if self.memory_manager.free(pid):
            self.update_display()
            self.e_pid.delete(0, tk.END)
            self.set_status(f"[OK] Đã thu hồi tiến trình {pid} và gộp vùng trống liền kề.", "ok")
        else:
            self.set_status(f"[LỖI] Không tìm thấy tiến trình '{pid}'.", "err")
            messagebox.showerror("Lỗi", f"Không tìm thấy tiến trình {pid}.")

    def do_load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            total, reqs = io_csv.read_requests(path)
            self.memory_manager = MemoryManager(total)
            self.total = total
            self.history = list(reqs)
            self.e_total.delete(0, tk.END)
            self.e_total.insert(0, str(total))

            strat_name = self.strategy_var.get()
            strat = STRATEGIES[strat_name]
            for act, pid, sz in self.history:
                if act == "alloc":
                    self.memory_manager.allocate(pid, sz, strat)
                elif act == "free":
                    self.memory_manager.free(pid)
            self.update_display()
            self.set_status(
                f"[OK] Đã nạp {len(self.history)} yêu cầu từ '{os.path.basename(path)}' ({strat_name}).", "ok"
            )
            messagebox.showinfo("Thành công", f"Đã nạp thành công {len(self.history)} yêu cầu từ CSV!")
        except Exception as e:
            self.set_status(f"[LỖI CSV] {e}", "err")
            messagebox.showerror("Lỗi CSV", str(e))

    def do_compare(self):
        if not self.history:
            return messagebox.showwarning("Cảnh báo", "Chưa có thao tác hoặc dữ liệu CSV để so sánh!")

        win = tk.Toplevel(self.root)
        win.title("So sánh 3 chiến lược")
        win.geometry("660x250")
        win.configure(bg=self.c_bg)

        tk.Label(
            win,
            text=f"ĐỐI CHIẾU 3 CHIẾN LƯỢC  (RAM: {self.total} KB  |  Số yêu cầu: {len(self.history)})",
            bg=self.c_bg,
            fg=self.c_accent,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 6))

        tree = ttk.Treeview(
            win,
            columns=("strat", "succ", "ext", "int"),
            show="headings",
            height=4,
            style="Dark.Treeview",
        )
        for col, text in zip(
            ("strat", "succ", "ext", "int"),
            ("Chiến lược", "Thành công", "Phân mảnh ngoài", "Phân mảnh trong (KB)"),
        ):
            tree.heading(col, text=text)
            tree.column(col, width=155, anchor="center")
        tree.tag_configure("row0", background="#111C2E", foreground="#F1F5F9")
        tree.tag_configure("row1", background="#162338", foreground="#F1F5F9")
        tree.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        try:
            for i, name in enumerate(STRATEGIES):
                trace = simulator.run_simulation(self.total, self.history, name)
                if trace:
                    last = trace[-1]
                    succ = sum(int(r["success"]) for r in trace)
                    tree.insert(
                        "",
                        "end",
                        tags=(f"row{i % 2}",),
                        values=(
                            name,
                            f"{succ}/{len(self.history)}",
                            f"{float(last['external_frag']):.4f}",
                            last["internal_frag"],
                        ),
                    )
        except Exception as e:
            win.destroy()
            messagebox.showerror("Lỗi so sánh", str(e))

    def do_export(self):
        if not self.history:
            return messagebox.showwarning("Cảnh báo", "Chưa có thao tác hoặc dữ liệu CSV để xuất!")
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return
        try:
            trace = simulator.run_simulation(
                self.total, self.history, self.strategy_var.get()
            )
            io_csv.write_trace(path, trace)
            self.set_status(f"[OK] Đã xuất file trace tại: {path}", "ok")
            messagebox.showinfo("Thành công", f"Đã xuất file tại:\n{path}")
        except Exception as e:
            self.set_status(f"[LỖI] Xuất CSV thất bại: {e}", "err")
            messagebox.showerror("Lỗi", str(e))

    def update_display(self):
        self.canvas.delete("all")
        if not self.memory_manager:
            return
        snap = self.memory_manager.snapshot()
        total = sum(b[1] for b in snap)
        if total <= 0:
            return
        w = max(self.canvas.winfo_width(), 840)

        x, y1, y2 = 26, 22, 94
        usable = w - 52
        palette = [
            "#0EA5E9",  # Sky
            "#10B981",  # Emerald
            "#F59E0B",  # Amber
            "#EF4444",  # Red
            "#8B5CF6",  # Violet
            "#EC4899",  # Pink
            "#14B8A6",  # Teal
            "#F97316",  # Orange
        ]
        p_map, idx = {}, 0

        for item in self.block_tree.get_children():
            self.block_tree.delete(item)

        alloc_count = 0
        for block_i, (start, size, pid, req) in enumerate(snap, start=1):
            if pid and pid not in p_map:
                p_map[pid] = palette[idx % len(palette)]
                idx += 1
            r_w = (size / total) * usable
            x_end = x + r_w

            if pid:
                self.canvas.create_rectangle(
                    x, y1, x_end, y2, fill=p_map[pid], outline="#0F172A", width=2
                )
                if r_w >= 38:
                    self.canvas.create_text(
                        (x + x_end) / 2,
                        (y1 + y2) / 2,
                        text=f"{pid}\n{size}K",
                        fill="#FFFFFF",
                        font=("Segoe UI", 8, "bold"),
                    )
                tag = "alloc_even" if alloc_count % 2 == 0 else "alloc_odd"
                alloc_count += 1
            else:
                self.canvas.create_rectangle(
                    x, y1, x_end, y2, fill="#131C2E", outline="#475569", width=1, dash=(4, 3)
                )
                if r_w >= 42:
                    self.canvas.create_text(
                        (x + x_end) / 2,
                        (y1 + y2) / 2,
                        text=f"Hole\n{size}K",
                        fill="#94A3B8",
                        font=("Consolas", 8),
                    )
                tag = "hole_row"

            self.canvas.create_text(x, y2 + 16, text=str(start), fill="#94A3B8", font=("Consolas", 8))
            x = x_end

            self.block_tree.insert(
                "",
                "end",
                tags=(tag,),
                values=(
                    block_i,
                    f"{start} -> {start + size}",
                    size,
                    f"Tiến trình {pid}" if pid else "Hole (Trống)",
                    req if pid else "-",
                    (size - req) if pid else 0,
                ),
            )

        self.canvas.create_text(x, y2 + 16, text=str(total), fill="#94A3B8", font=("Consolas", 8))

        # Cập nhật 4 thẻ KPI
        holes = [b[1] for b in snap if b[2] is None]
        free_total = sum(holes)
        used_total = total - free_total
        used_pct = (used_total / total) * 100.0
        ext_f = metrics.external_fragmentation(snap)
        int_f = metrics.internal_fragmentation(snap)

        self.kpi_used.config(text=f"{used_total} / {total} KB ({used_pct:.1f}%)")
        self.kpi_free.config(text=f"{free_total} KB ({len(holes)} hole)")
        self.kpi_ext.config(text=f"{ext_f:.4f}")
        self.kpi_int.config(text=f"{int_f} KB")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimApp(root)
    root.mainloop()