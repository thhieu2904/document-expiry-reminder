# Hướng dẫn Bàn giao DB & Khởi tạo

Tài liệu này hướng dẫn cách deploy Database cho khách hàng mới một cách mượt mà nhất, dựa trên các file SQL đã được đóng gói sẵn.

## 1. Hai File SQL Quan Trọng
Tại thư mục gốc của dự án, bạn sẽ thấy 2 file:
- `database_schema.sql`: Chứa cấu trúc các bảng (Schema). Được xuất ra tự động bởi `Alembic`. KHÔNG có dữ liệu thực bên trong.
- `seed_data.sql`: Chứa dữ liệu mồi (Seed Data) bắt buộc phải có để hệ thống hoạt động.

## 2. Quy trình 4 Bước Setup Database (Cho Khách Hàng)
Khi bàn giao source code và yêu cầu khách tạo 1 Project Supabase mới, hãy làm theo 4 bước sau:

**Bước 1: Cấu hình biến môi trường (`.env`)**
- Lấy `URL`, `Anon Key`, `Service Role Key` của Supabase mới điền vào `.env` ở Backend.
- Điền tài khoản Gmail App Password (như đã hướng dẫn ở file `02_email_smtp_optimizations.md`).

**Bước 2: Tạo User Authentication (RẤT QUAN TRỌNG)**
- Vào Dashboard Supabase -> Mục **Authentication** -> Add User.
- Thêm một user tên là `admin@gmail.com` (hoặc email của khách hàng) với password tuỳ ý.
- Mục đích: Tạo ra user này để Lát nữa khi chạy `seed_data.sql` nó sẽ mapping email này vào bảng `users` để làm Admin.

**Bước 3: Chạy Schema (Tạo Bảng)**
- Mở Dashboard Supabase -> Mục **SQL Editor**.
- Mở file `database_schema.sql` -> Copy toàn bộ -> Dán vào SQL Editor -> Bấm RUN.
- Lúc này 6 bảng dữ liệu đã được tạo.

**Bước 4: Chạy Seed Data (Đổ Dữ Liệu mồi)**
- Mở file `seed_data.sql` -> Copy toàn bộ -> Dán vào SQL Editor -> Bấm RUN.
- Lúc này Database đã có sẵn Admin, 5 Quy tắc nhắc nhở mặc định và Cài đặt Cronjob sẵn sàng chạy.

*(Sau khi hoàn tất 4 bước, ứng dụng có thể chạy và login thành công ngay lập tức!)*
