# Tối ưu Email & Template Engine

Tài liệu này ghi lại quyết định chuyển đổi kiến trúc gửi mail sang Gmail và công cụ phân tích Template email.

## 1. Dịch vụ SMTP (Chuyển sang Gmail App Password)
Trong quá trình phát triển, dự án dùng Mailtrap Sandbox. Khi lên Production, dự án đã chốt sử dụng **Gmail App Password**.
Lý do:
- Không phụ thuộc bên thứ 3 (Mailtrap Sending, SendGrid giới hạn số lượng và rắc rối về domain).
- Bàn giao dễ dàng: Khách hàng chỉ cần cung cấp 1 địa chỉ Gmail mới tinh (VD: `nhachhan.coquan@gmail.com`). Admin tạo App Password (mật khẩu ứng dụng 16 ký tự) và điền vào `.env`. Khách hàng làm chủ 100% dữ liệu.

**Cấu hình kỹ thuật:**
- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `start_tls=True` (Bắt buộc với Gmail trên cổng 587, đã được sửa trong `email_service.py`).

## 2. Template Engine (Công cụ bóc tách thẻ nội dung)
Admin có thể tự viết tiêu đề và nội dung email thông qua giao diện Web thay vì Dev hardcode cứng.
Cơ chế hoạt động:
- Lớp `backend/app/services/reminder_engine.py` chứa hàm `parse_template`.
- Nó tiếp nhận chuỗi string từ DB (Ví dụ: `"Văn bản {{document_title}} sắp hết hạn"`).
- Nó tiến hành chuỗi lệnh `.replace()` để thay các chuỗi đại diện (tags) bằng dữ liệu thực tế (`doc.title`, `doc.document_number`, v.v.).
- Đã được bao phủ bằng **19 Unit Tests** (`tests/test_template_parser.py`) để đảm bảo không bị crash khi data trả về None (VD: văn bản không có phòng ban, tên user không có, quá hạn ngày âm).

## 3. Tối ưu Hiệu suất (N+1 Query)
Trong trang Lịch sử Gửi Email (`Reminders.jsx`), backend cần lấy Tên văn bản và Tên quy tắc.
Thay vì query lấy `ReminderLog` rồi dùng vòng lặp `for log in logs:` để query DB thêm 100 lần (Lỗi N+1 Query), hệ thống đã được tối ưu bằng SQLAlchemy `joinedload` (`selectinload` trong async).
- **Code tối ưu:** Trong `app/api/reminders.py`.
- **Kết quả:** Lấy 100 dòng logs chỉ tốn đúng 1 Query duy nhất thay vì 101 Query, giúp trang Web load nhanh dưới 100ms.
