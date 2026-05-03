# Kiến trúc Cronjob & System Settings

Tài liệu này ghi chú lại cách hệ thống lên lịch gửi email tự động (Cronjob) và quản lý cài đặt hệ thống, được xây dựng để dễ dàng mở rộng và không gây gián đoạn (Zero-downtime).

## 1. Bảng `system_settings` (Key-Value Store)
Thay vì lưu cài đặt vào file `.json` (dễ bị mất khi restart server hoặc deploy lên cloud), hệ thống sử dụng bảng `system_settings` trong PostgreSQL.
- **Model:** `backend/app/models/system_setting.py`
- **Cấu trúc:** Rất linh hoạt (`key`, `value`, `description`). Hiện tại dùng để lưu `cron_time_1`, `cron_time_2`, `cron_enabled_2`. 
- **Khả năng mở rộng:** Sau này nếu cần thêm cài đặt (VD: `max_emails_per_day`, `maintenance_mode`), AI hoặc Dev chỉ cần thêm key mới vào bảng này, không cần sửa schema DB.

## 2. Dynamic APScheduler (Lên lịch Động)
Hệ thống sử dụng `APScheduler` (`AsyncIOScheduler`) của Python, được gắn trực tiếp vào `app.state.scheduler` của FastAPI tại `main.py`.

### Cách hoạt động:
1. **Không phải Polling:** Cronjob KHÔNG chạy mỗi 15 phút để check DB. Nó tính toán chính xác số giây từ thời điểm hiện tại đến giờ được hẹn (VD: 08:00 sáng mai) và "ngủ đông" (sleep) đúng ngần ấy giây. Việc này tiêu tốn 0% CPU.
2. **Cập nhật Live (Real-time):** Khi Admin đổi giờ trên Frontend (React), API `PUT /api/settings/cron` được gọi. API này sẽ:
   - Lưu giờ mới xuống Database.
   - Gọi hàm `load_settings_and_configure_scheduler` (trong `backend/app/core/scheduler.py`).
   - Hàm này sẽ tìm các job cũ trong Scheduler, xoá chúng đi (`job.remove()`), và tạo job mới với giờ mới (`scheduler.add_job(...)`).
   - **Kết quả:** Lịch mới có hiệu lực ngay tắp lự mà không cần restart server FastAPI.

## 3. Chuyển đổi Múi giờ (Timezone)
- Frontend hiển thị và gửi giờ Việt Nam (UTC+7) (VD: "08:00").
- Hàm `convert_vn_to_utc` trong `scheduler.py` sẽ làm phép tính lùi 7 tiếng (VD: "01:00") để gán vào APScheduler.
- Do đó, Database Supabase (nằm ở server Mỹ/Nhật) dù chạy múi giờ chuẩn UTC vẫn sẽ trigger gửi mail đúng 8h sáng giờ Việt Nam.

## 4. UI/UX Frontend
- UI được viết trong `frontend/src/pages/Reminders.jsx`.
- Sử dụng trick CSS: Đặt một `<Switch style={{ visibility: 'hidden' }} />` ở ô Lần 1 để đảm bảo chiều cao (height) của ô Lần 1 và Lần 2 cân bằng pixel-perfect (đối xứng tuyệt đối).
- `TimePicker` được set `style={{ width: '120px' }}` để không bị phình to làm xấu giao diện.
