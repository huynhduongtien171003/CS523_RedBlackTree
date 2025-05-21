# CS523_Red-Black-Tree
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology" width="200">
  </a>
</p>

<h1 align="center"><b>CS523.P21 - Cấu trúc dữ liệu và giải thuật nâng cao</b></h1>

## 📑 Mục lục
- [Giới thiệu môn học](#-giới-thiệu-môn-học)
- [Giảng viên hướng dẫn](#-giảng-viên-hướng-dẫn)
- [Thành viên nhóm](#-thành-viên-nhóm)
- [Đồ án môn học](#-đồ-án-môn-học)
  - [Giới thiệu đồ án](#-giới-thiệu-đồ-án)
  - [Slide trình bày](#-slide-trình-bày)
  - [Demo Visualizer](#-demo-visualizer)
  - [Ứng dụng từ điển](#-ứng-dụng-từ-điển)

## 🏫 Giới thiệu môn học
<a name="-giới-thiệu-môn-học"></a>
* **Tên môn học**: Cấu trúc dữ liệu và giải thuật nâng cao  
* **Mã môn học**: CS523  
* **Lớp học**: CS523.P21  

## 👨‍🏫 Giảng viên hướng dẫn
<a name="-giảng-viên-hướng-dẫn"></a>
* **TS. Nguyễn Thanh Sơn**  
* Trường Đại học Công nghệ Thông tin - ĐHQG TP.HCM

## 👥 Thành viên nhóm
<a name="-thành-viên-nhóm"></a>
| STT | MSSV      | Họ và Tên         | Github | Email |
|-----|-----------|------------------|--------|-------|
| 1   | 22521465  | Huỳnh Dương Tiến | [![GitHub](https://img.shields.io/badge/GitHub-Tien-blue)](https://github.com/huynhduongtien171003) | 22521465@gm.uit.edu.vn | 
| 2   | 23520361  | Đặng Vân Duy     | [![GitHub](https://img.shields.io/badge/GitHub-Duy-green)](https://github.com/DuyDanga) | 23520361@gm.uit.edu.vn | 

## 🎓 Đồ án môn học: Cây Đỏ Đen (Red-Black Tree)
<a name="-đồ-án-môn-học"></a>

### 📌 Giới thiệu đồ án
<a name="-giới-thiệu-đồ-án"></a>
Đồ án nghiên cứu và triển khai cấu trúc dữ liệu Cây Đỏ Đen 

### 📚 Slide trình bày
<a name="-slide-trình-bày"></a>
[![Slide Preview](https://img.shields.io/badge/Download-Slides-blue)](https://github.com/huynhduongtien171003/CS523_Red-Black-Tree/blob/main/Red-Black%20Tree-Slide.pptx)

Nội dung chính:
1. Lý thuyết cơ bản về RBT
2. Các tính chất đặc trưng
3. Thuật toán chèn (Insertion) 
4. Thuật toán xóa (Deletion)
5. So sánh giữa AVL và RBT
6. Ứng dụng thực tế
7. Demo minh hoaj

### 🖥️ Demo Visualizer
<a name="-demo-visualizer"></a>
![Visualizer Demo](https://github.com/huynhduongtien171003/CS523_Red-Black-Tree/blob/main/visualizer_redblack_tree.html)

**Tính năng nổi bật**:
- Giao diện đồ họa trực quan
- Hiển thị  thao tác chèn/xóa
- Kiểm tra tính hợp lệ của cây
- Tùy chọn tự động/từng bước

## 📚 Ứng dụng Từ điển Anh-Việt sử dụng Red-Black Tree

### 🌟 Giới thiệu
Ứng dụng từ điển minh họa khả năng ứng dụng thực tế của cấu trúc Red-Black Tree trong bài toán tìm kiếm từ vựng  .

### 🎯 Tính năng chính
- **Tra cứu từ**: Tìm kiếm từ với thuật toán tìm kiếm trên RBT
- **Quản lý từ vựng**:
  - Thêm từ mới (tự động cân bằng cây)
  - Xóa từ (tự động cân bằng cây)
  - Cập nhật nghĩa từ
- **Import/Export**:
  - Đọc dữ liệu từ file text
  - Xuất dữ liệu ra file
- **Gợi ý thông minh**: Gợi ý từ gần đúng khi nhập

### 🖼️ Giao diện ứng dụng
![Dictionary Interface](https://drive.google.com/file/d/1ZNch6nVw41nxhpJJZnM6tPIHOs4NsOdO/view?usp=sharing)

### 🛠️ Công nghệ sử dụng
```python
- Python 
- Red-Black Tree tự triển khai
- Tkinter cho giao diện đồ họa
- Unidecode để chuẩn hóa từ nhập

