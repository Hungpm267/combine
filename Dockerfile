# 1. Bắt đầu từ một base image có sẵn Python
# Sử dụng 'slim' để có image gọn nhẹ nhất
FROM python:3.10-slim

# 2. Thiết lập biến môi trường
# Ngăn Python tạo file .pyc (không cần thiết trong container)
ENV PYTHONDONTWRITEBYTECODE 1
# Đảm bảo output (như 'print') ra thẳng console (tốt cho việc xem log)
ENV PYTHONUNBUFFERED 1

# 3. Tạo thư mục làm việc bên trong container
WORKDIR /app

# 4. Cài đặt dependencies (phụ thuộc)
# Copy 'requirements.txt' VÀO TRƯỚC
COPY requirements.txt .

# Chạy 'pip install'
# Dùng '--no-cache-dir' để giữ image gọn nhẹ
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy toàn bộ code dự án vào container
COPY . .

# 6. Expose port (Mở cổng)
# Cho Docker biết rằng ứng dụng bên trong container sẽ chạy ở cổng 8000
EXPOSE 8000

# 7. Lệnh chạy ứng dụng khi container khởi động
# Đây là lúc Gunicorn xuất hiện!
# THAY "your_project_name" bằng tên thư mục chứa file wsgi.py của bạn
CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]