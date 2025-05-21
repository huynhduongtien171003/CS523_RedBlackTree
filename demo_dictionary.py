import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math

RED = True
BLACK = False

class RBNode:
    def __init__(self, key, value, color=RED):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.root = None

    def is_red(self, node):
        return node is not None and node.color == RED

    def rotate_left(self, node):
        x = node.right
        node.right = x.left
        x.left = node
        x.color = node.color
        node.color = RED
        return x

    def rotate_right(self, node):
        x = node.left
        node.left = x.right
        x.right = node
        x.color = node.color
        node.color = RED
        return x

    def flip_colors(self, node):
        node.color = not node.color
        if node.left: node.left.color = not node.left.color
        if node.right: node.right.color = not node.right.color

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
        self.root.color = BLACK

    def _insert(self, node, key, value):
        if node is None:
            return RBNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value

        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        return node.value

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Từ điển Anh-Việt - Red-Black Tree")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f4f8")
        
        # Thiết lập style
        self.setup_styles()
        
        # Cây chính lưu từ Anh -> Việt
        self.eng_viet_tree = RedBlackTree()
        # Cây phụ lưu từ Việt -> Anh
        self.viet_eng_tree = RedBlackTree()
        
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0
        self.node_radius = 25  # Tăng kích thước node
        self.level_height = 80  # Tăng chiều cao giữa các cấp
        self.h_spacing = 60  # Tăng khoảng cách ngang
        self.tree_visible = False
        self.mode = "lookup"  # Chế độ mặc định: tra từ
        
        self.create_widgets()
        self.add_sample_words()

    def setup_styles(self):
            style = ttk.Style()
            style.configure('TFrame', background='#f0f4f8')
            style.configure('TLabelframe', background='#f0f4f8')
            style.configure('TLabelframe.Label', background='#f0f4f8', font=('Helvetica', 10, 'bold'))
            
            # Thiết lập chữ màu đen cho cả 2 trạng thái
            style.configure('Primary.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('Primary.TButton', 
                    background=[('active', '#345d8a'), ('!active', '#4a6fa5')],
                    foreground=[('active', 'black'), ('!active', 'black')])  # Chữ đen cả 2 trạng thái
            
            style.configure('Secondary.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('Secondary.TButton', 
                    background=[('active', '#5a6268'), ('!active', '#6c757d')],
                    foreground=[('active', 'black'), ('!active', 'black')])
            
            style.configure('Success.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('Success.TButton', 
                    background=[('active', '#218838'), ('!active', '#28a745')],
                    foreground=[('active', 'black'), ('!active', 'black')])
            
            style.configure('Info.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('Info.TButton', 
                    background=[('active', '#138496'), ('!active', '#17a2b8')],
                    foreground=[('active', 'black'), ('!active', 'black')])
            
            # Nút hiển thị cây với chữ đen
            style.configure('ToggleTree.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('ToggleTree.TButton', 
                    background=[('active', '#d63031'), ('!active', '#e74c3c')],
                    foreground=[('active', 'black'), ('!active', 'black')])
            
            # Nút Load File với chữ đen
            style.configure('LoadFile.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('LoadFile.TButton', 
                    background=[('active', '#7158e2'), ('!active', '#8854d0')],
                    foreground=[('active', 'black'), ('!active', 'black')])
            
            # Nút Save File với chữ đen
            style.configure('SaveFile.TButton', 
                        font=('Helvetica', 11, 'bold'),
                        foreground='black')  # Chữ màu đen
            
            style.map('SaveFile.TButton', 
                    background=[('active', '#20bf6b'), ('!active', '#26de81')],
                    foreground=[('active', 'black'), ('!active', 'black')])
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = ttk.Label(header_frame, text="Từ điển Anh-Việt", 
                              style='Header.TLabel')
        header_label.pack(side=tk.LEFT, padx=5)
        
        # Mode selection frame
        mode_frame = ttk.Frame(main_frame, style='TFrame')
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.mode_var = tk.StringVar(value="lookup")
        
        mode_label = ttk.Label(mode_frame, text="Chế độ:", style='Mode.TLabel')
        mode_label.pack(side=tk.LEFT, padx=5)
        
        lookup_radio = ttk.Radiobutton(mode_frame, text="Tra từ", value="lookup", 
                                      variable=self.mode_var, command=self.change_mode)
        lookup_radio.pack(side=tk.LEFT, padx=10)
        
        add_radio = ttk.Radiobutton(mode_frame, text="Thêm từ", value="add", 
                                  variable=self.mode_var, command=self.change_mode)
        add_radio.pack(side=tk.LEFT, padx=10)
        
        # Control frame
        self.control_frame = ttk.LabelFrame(main_frame, text="Tra từ", padding=15)
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # Lookup widgets
        self.create_lookup_widgets()
        
        # Add word widgets (hidden initially)
        self.create_add_widgets()
        
        # Tree visualization frame
        self.tree_frame = ttk.LabelFrame(main_frame, text="Cây đỏ-đen", padding=10)
        self.canvas = tk.Canvas(self.tree_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Result frame
        result_frame = ttk.Frame(main_frame, style='TFrame')
        result_frame.pack(fill=tk.X, pady=10)
        
        self.result_frame = ttk.LabelFrame(main_frame, text="Kết quả tra từ", padding=15)
        self.result_frame.pack(fill=tk.X, pady=10)
        
        self.result_word = ttk.Label(self.result_frame, text="", font=('Helvetica', 14, 'bold'), foreground="#4a6fa5")
        self.result_word.pack(anchor=tk.W)
        
        self.result_meaning = ttk.Label(self.result_frame, text="", font=('Helvetica', 12), wraplength=1000)
        self.result_meaning.pack(anchor=tk.W, pady=5)
        
        # Bottom button bar với nút có style riêng biệt
        button_bar = ttk.Frame(main_frame, style='TFrame')
        button_bar.pack(fill=tk.X, pady=10)
        
       
        
        # Nút nạp từ file với màu riêng
        ttk.Button(button_bar, text="NẠP TỪ FILE", command=self.load_from_file, 
                style='LoadFile.TButton', width=15).pack(side=tk.LEFT, padx=8)
        
        # Nút lưu vào file với màu riêng
        ttk.Button(button_bar, text="LƯU VÀO FILE", command=self.save_to_file, 
                style='SaveFile.TButton', width=15).pack(side=tk.LEFT, padx=8)
        
        # Zoom controls
        zoom_frame = ttk.Frame(button_bar, style='TFrame')
        zoom_frame.pack(side=tk.RIGHT)
        
        ttk.Label(zoom_frame, text="Thu phóng:", font=('Helvetica', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="+", width=3, command=lambda: self.adjust_zoom(1.2), 
                style='Primary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="-", width=3, command=lambda: self.adjust_zoom(0.8), 
                style='Secondary.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Reset", command=lambda: self.adjust_zoom(1.0, reset=True), 
                style='Info.TButton', width=6).pack(side=tk.LEFT, padx=5)
        self.tree_btn = ttk.Button(self.control_frame, text="Hiện Cây Đỏ Đen", 
                              command=self.toggle_tree_display,
                              style='ToggleTree.TButton')
        self.tree_btn.pack(side=tk.LEFT, padx=5)

        # Frame chứa cây đỏ đen
        self.tree_frame = ttk.Frame(self.root, padding=10)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.tree_frame.pack_forget()  # Ẩn ban đầu

        # Canvas để vẽ cây
        self.tree_canvas = tk.Canvas(self.tree_frame, bg="white", width=800, height=500)
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)

        # Nhãn giải thích
        legend_frame = ttk.Frame(self.tree_frame)
        legend_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(legend_frame, text="Chú thích:").pack(side=tk.LEFT, padx=5)
        
        # Node đỏ
        self.tree_canvas.create_oval(10, 10, 30, 30, fill="#ff6b6b", outline="black")
        ttk.Label(legend_frame, text="Node đỏ").pack(side=tk.LEFT, padx=5)
        
        # Node đen
        self.tree_canvas.create_oval(10, 10, 30, 30, fill="#2b2d42", outline="black")
        ttk.Label(legend_frame, text="Node đen").pack(side=tk.LEFT, padx=15)
        # Thêm nút hiển thị cây đỏ đen
        self.tree_btn = ttk.Button(self.control_frame, text="Hiện Cây Đỏ Đen", 
                                command=self.toggle_tree_display,
                                style='ToggleTree.TButton')
        self.tree_btn.pack(side=tk.LEFT, padx=5)

        # Frame chứa cây đỏ đen
        self.tree_frame = ttk.Frame(self.root, padding=10)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.tree_frame.pack_forget()  # Ẩn ban đầu

        # Canvas để vẽ cây
        self.tree_canvas = tk.Canvas(self.tree_frame, bg="white", width=800, height=500)
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)

        # Nhãn giải thích
        legend_frame = ttk.Frame(self.tree_frame)
        legend_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(legend_frame, text="Chú thích:").pack(side=tk.LEFT, padx=5)
        
        # Node đỏ
        self.tree_canvas.create_oval(10, 10, 30, 30, fill="#ff6b6b", outline="black")
        ttk.Label(legend_frame, text="Node đỏ").pack(side=tk.LEFT, padx=5)
        
        # Node đen
        self.tree_canvas.create_oval(10, 10, 30, 30, fill="#2b2d42", outline="black")
        ttk.Label(legend_frame, text="Node đen").pack(side=tk.LEFT, padx=15)
        

    def toggle_tree_display(self):
        if self.tree_frame.winfo_ismapped():
            self.tree_frame.pack_forget()
            self.tree_btn.config(text="Hiện Cây Đỏ Đen")
        else:
            self.tree_frame.pack(fill=tk.BOTH, expand=True)
            self.tree_btn.config(text="Ẩn Cây Đỏ Đen")
            self.draw_red_black_tree()

    def draw_red_black_tree(self):
        self.tree_canvas.delete("all")
        
        if not self.eng_viet_tree.root:
            self.tree_canvas.create_text(400, 250, text="Cây trống", font=("Arial", 14))
            return
        
        # Tính toán vị trí các node
        self.node_positions = {}
        self.calculate_positions(self.eng_viet_tree.root, 400, 50, 200)
        
        # Vẽ các đường nối trước
        for node in self.node_positions.values():
            x, y = node['x'], node['y']
            if node['left']:
                left_x, left_y = self.node_positions[node['left']]['x'], self.node_positions[node['left']]['y']
                self.tree_canvas.create_line(x, y, left_x, left_y, fill="black", width=2)
            if node['right']:
                right_x, right_y = self.node_positions[node['right']]['x'], self.node_positions[node['right']]['y']
                self.tree_canvas.create_line(x, y, right_x, right_y, fill="black", width=2)
        
        # Vẽ các node sau
        for key, node in self.node_positions.items():
            x, y = node['x'], node['y']
            color = "#ff6b6b" if node['color'] == RED else "#2b2d42"
            text_color = "white"
            
            # Vẽ node
            self.tree_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black")
            self.tree_canvas.create_text(x, y, text=key, fill=text_color, font=("Arial", 10, "bold"))

    def calculate_positions(self, node, x, y, h_space):
        if node is None:
            return
        
        # Lưu vị trí node hiện tại
        node_info = {
            'x': x,
            'y': y,
            'color': node.color,
            'left': node.left.key if node.left else None,
            'right': node.right.key if node.right else None
        }
        self.node_positions[node.key] = node_info
        
        # Tính toán vị trí cho node con
        if node.left:
            self.calculate_positions(node.left, x - h_space, y + 80, h_space / 2)
        if node.right:
            self.calculate_positions(node.right, x + h_space, y + 80, h_space / 2)
        

    def create_lookup_widgets(self):
        self.lookup_frame = ttk.Frame(self.control_frame)
        self.lookup_frame.pack(fill=tk.X)
        
        ttk.Label(self.lookup_frame, text="Tra từ:", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=5, sticky=tk.W)
        self.lookup_entry = ttk.Entry(self.lookup_frame, width=40, font=('Helvetica', 12))
        self.lookup_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        self.lookup_entry.bind('<Return>', lambda e: self.lookup_word())
        
        self.direction_var = tk.StringVar(value="eng_to_viet")
        eng_radio = ttk.Radiobutton(self.lookup_frame, text="Anh → Việt", 
                                 variable=self.direction_var, value="eng_to_viet")
        eng_radio.grid(row=0, column=2, padx=15)
        
        viet_radio = ttk.Radiobutton(self.lookup_frame, text="Việt → Anh", 
                                  variable=self.direction_var, value="viet_to_eng")
        viet_radio.grid(row=0, column=3, padx=15)
        
        lookup_btn = ttk.Button(self.lookup_frame, text="TRA CỨU", 
                              command=self.lookup_word, style='Primary.TButton', width=15)
        lookup_btn.grid(row=0, column=4, padx=20)

    def create_add_widgets(self):
        self.add_frame = ttk.Frame(self.control_frame)
        
        ttk.Label(self.add_frame, text="Từ tiếng Anh:", font=('Helvetica', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.word_entry = ttk.Entry(self.add_frame, width=40, font=('Helvetica', 12))
        self.word_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.add_frame, text="Nghĩa tiếng Việt:", font=('Helvetica', 11, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.meaning_entry = ttk.Entry(self.add_frame, width=40, font=('Helvetica', 12))
        self.meaning_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        add_btn = ttk.Button(self.add_frame, text="THÊM TỪ", 
                          command=self.add_word, style='Success.TButton', width=15)
        add_btn.grid(row=0, column=3, rowspan=2, padx=20)

    def change_mode(self):
        mode = self.mode_var.get()
        if mode == "lookup":
            self.add_frame.pack_forget()
            self.lookup_frame.pack(fill=tk.X)
            self.control_frame.configure(text="Tra từ")
        else:  # add mode
            self.lookup_frame.pack_forget()
            self.add_frame.pack(fill=tk.X)
            self.control_frame.configure(text="Thêm từ mới")

    def toggle_tree(self):
        if self.tree_visible:
            self.tree_frame.pack_forget()
            self.tree_visible = False
        else:
            self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            self.tree_visible = True
            self.draw_tree()

    def adjust_zoom(self, factor, reset=False):
        if reset:
            self.zoom = 1.0
        else:
            self.zoom *= factor
            self.zoom = max(self.min_zoom, min(self.zoom, self.max_zoom))

        self.node_radius = int(25 * self.zoom)  # Kích thước node lớn hơn
        self.level_height = int(90 * self.zoom)  # Chiều cao giữa các cấp lớn hơn
        self.h_spacing = int(70 * self.zoom)  # Khoảng cách ngang lớn hơn

        if self.tree_visible:
            self.draw_tree()

    def add_sample_words(self):
        # 50 từ vựng cơ bản Anh-Việt
        words = {
            # Danh từ thông dụng
            "book": "quyển sách",
            "apple": "quả táo",
            "dog": "con chó",
            "cat": "con mèo",
            "house": "ngôi nhà",
            "car": "xe hơi",
            "phone": "điện thoại",
            "computer": "máy tính",
            "school": "trường học",
            "teacher": "giáo viên",
            "student": "học sinh",
            "friend": "bạn bè",
            "family": "gia đình",
            "mother": "mẹ",
            "father": "cha",
            "water": "nước",
            "food": "thức ăn",
            "money": "tiền",
            "time": "thời gian",
            "day": "ngày",
            
            # Động từ thông dụng
            "go": "đi",
            "come": "đến",
            "eat": "ăn",
            "drink": "uống",
            "sleep": "ngủ",
            "study": "học",
            "work": "làm việc",
            "talk": "nói chuyện",
            "read": "đọc",
            "write": "viết",
            
            # Tính từ thông dụng
            "good": "tốt",
            "bad": "xấu",
            "big": "to lớn",
            "small": "nhỏ",
            "hot": "nóng",
            "cold": "lạnh",
            "new": "mới",
            "old": "cũ",
            "happy": "vui vẻ",
            "sad": "buồn",
            
            # Các từ khác
            "hello": "xin chào",
            "goodbye": "tạm biệt",
            "yes": "vâng, có",
            "no": "không",
            "thank you": "cảm ơn",
            "please": "làm ơn",
            "sorry": "xin lỗi",
            "here": "ở đây",
            "there": "ở đó",
            "now": "bây giờ"
        }
        
        # Thêm từ vào cả hai cây
        for eng, viet in words.items():
            self.eng_viet_tree.insert(eng, viet)
            self.viet_eng_tree.insert(viet, eng)

    def add_word(self):
        word = self.word_entry.get().strip()
        meaning = self.meaning_entry.get().strip()
        
        if not word:
            messagebox.showerror("Lỗi", "Vui lòng nhập từ tiếng Anh")
            return
        if not meaning:
            messagebox.showerror("Lỗi", "Vui lòng nhập nghĩa tiếng Việt")
            return
            
        # Thêm vào cả hai cây
        self.eng_viet_tree.insert(word, meaning)
        self.viet_eng_tree.insert(meaning, word)
        
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        
        # Cập nhật hiển thị
        self.result_word.config(text=f"{word}")
        self.result_meaning.config(text=f"{meaning}")
        
        messagebox.showinfo("Thành công", f"Đã thêm từ mới: {word} - {meaning}")
        
        if self.tree_visible:
            self.draw_tree()

    def lookup_word(self):
        search_term = self.lookup_entry.get().strip()
        if not search_term:
            messagebox.showerror("Lỗi", "Vui lòng nhập từ cần tra")
            return
            
        direction = self.direction_var.get()
        if direction == "eng_to_viet":
            # Tra từ Anh -> Việt
            result = self.eng_viet_tree.search(search_term)
            if result:
                self.show_result(search_term, result, is_eng_to_viet=True)
            else:
                self.show_no_result(search_term)
        else:
            # Tra từ Việt -> Anh
            result = self.viet_eng_tree.search(search_term)
            if result:
                self.show_result(search_term, result, is_eng_to_viet=False)
            else:
                self.show_no_result(search_term)

    def show_result(self, word, meaning, is_eng_to_viet=True):
        self.result_word.config(text=word)
        
        if is_eng_to_viet:
            prefix = "Nghĩa tiếng Việt: "
        else:
            prefix = "Nghĩa tiếng Anh: "
            
        self.result_meaning.config(text=f"{prefix}{meaning}")

    def show_no_result(self, word):
        self.result_word.config(text=f"Không tìm thấy: {word}")
        self.result_meaning.config(text="")

    def load_from_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    count = 0
                    for line in f:
                        if ':' in line:
                            word, meaning = line.strip().split(':', 1)
                            word = word.strip()
                            meaning = meaning.strip()
                            self.eng_viet_tree.insert(word, meaning)
                            self.viet_eng_tree.insert(meaning, word)
                            count += 1
                if self.tree_visible:
                    self.draw_tree()
                messagebox.showinfo("Thành công", f"Đã nạp {count} từ từ file")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")

    def save_to_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                count = 0
                with open(filepath, 'w', encoding='utf-8') as f:
                    stack = []
                    node = self.eng_viet_tree.root
                    while stack or node:
                        while node:
                            stack.append(node)
                            node = node.left
                        node = stack.pop()
                        f.write(f"{node.key}:{node.value}\n")
                        count += 1
                        node = node.right
                messagebox.showinfo("Thành công", f"Đã lưu {count} từ vào file")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể ghi file: {str(e)}")

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.eng_viet_tree.root:
            self.canvas.create_text(400, 50, text="Cây từ điển trống", font=("Arial", 14))
            return
            
        # Vẽ cây Anh-Việt
        depth = self.get_tree_depth(self.eng_viet_tree.root)
        canvas_width = max(800, (2 ** depth) * self.h_spacing)
        canvas_height = depth * self.level_height + 100
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        # Thêm nền để cây nổi bật hơn
        self.canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill="#f8f9fa", outline="")
        
        # Tiêu đề cây
        self.canvas.create_text(canvas_width//2, 20, text="CÂY TỪ ĐIỂN ANH-VIỆT", 
                            font=("Arial", 14, "bold"), fill="#2c3e50")
        
        # Thêm hướng dẫn màu sắc
        self.canvas.create_oval(30, 20, 45, 35, fill="#e74c3c", outline="#333", width=1.5)
        self.canvas.create_text(80, 20, text="Node đỏ", font=("Arial", 10), anchor=tk.W)
        
        self.canvas.create_oval(130, 20, 145, 35, fill="#2c3e50", outline="#333", width=1.5)
        self.canvas.create_text(180, 20, text="Node đen", font=("Arial", 10), anchor=tk.W)
        
        self.draw_node(self.eng_viet_tree.root, canvas_width//2, 60, canvas_width//4)

    def get_tree_depth(self, node):
        if not node:
            return 0
        return max(self.get_tree_depth(node.left), self.get_tree_depth(node.right)) + 1

    def draw_node(self, node, x, y, spacing):
        if not node:
            return
        if node.left:
            left_x = x - spacing
            left_y = y + self.level_height
            # Đường kết nối với node con bên trái
            self.canvas.create_line(x, y, left_x, left_y, fill="#555", width=2)
            self.draw_node(node.left, left_x, left_y, spacing / 2)
        if node.right:
            right_x = x + spacing
            right_y = y + self.level_height
            # Đường kết nối với node con bên phải
            self.canvas.create_line(x, y, right_x, right_y, fill="#555", width=2)
            self.draw_node(node.right, right_x, right_y, spacing / 2)
            
        # Chọn màu rõ ràng hơn cho node đỏ và đen
        if node.color == RED:
            node_color = "#e74c3c"  # Đỏ rõ hơn
            text_color = "white"
        else:
            node_color = "#2c3e50"  # Xanh đen rõ hơn
            text_color = "white"
        
        # Shadow effect - đổ bóng làm cho node nổi bật hơn
        self.canvas.create_oval(x-self.node_radius+3, y-self.node_radius+3, 
                             x+self.node_radius+3, y+self.node_radius+3, 
                             fill="#00000033", outline="")
        
        # Node circle với viền rõ nét hơn
        self.canvas.create_oval(x-self.node_radius, y-self.node_radius, 
                             x+self.node_radius, y+self.node_radius, 
                             fill=node_color, outline="#333", width=2)
        
        # Node text (key) với font lớn hơn
        display_text = node.key if len(node.key) <= 8 else node.key[:6] + ".."
        self.canvas.create_text(x, y, text=display_text, fill=text_color, 
                             font=('Arial', int(11*self.zoom), 'bold'))

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
