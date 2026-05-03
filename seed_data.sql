-- DỮ LIỆU MẪU CHO CƠ SỞ DỮ LIỆU MỚI (BÀN GIAO)
-- Chạy file này SAU KHI đã chạy file database_schema.sql

-- 1. Tạo một Admin User mặc định để có thể đăng nhập vào hệ thống
-- LƯU Ý: Phải tạo user này trong phần "Authentication" của Supabase trước với email "admin@gmail.com" và mật khẩu tùy ý.
INSERT INTO users (id, full_name, email, role, can_login, status, created_at, updated_at)
VALUES (
    gen_random_uuid(), 
    'Quản trị viên Hệ thống', 
    'admin@gmail.com', -- Sửa email này thành email của khách hàng
    'admin', 
    true, 
    'active', 
    now(), 
    now()
);

-- 2. Tạo các Quy tắc nhắc nhở (Reminder Rules) mặc định
INSERT INTO reminder_rules (id, name, days_before, is_overdue_rule, channel, is_active, created_at, updated_at) VALUES 
(gen_random_uuid(), 'Nhắc trước 30 ngày', 30, false, 'email', true, now(), now()),
(gen_random_uuid(), 'Nhắc trước 15 ngày', 15, false, 'email', true, now(), now()),
(gen_random_uuid(), 'Nhắc trước 7 ngày', 7, false, 'email', true, now(), now()),
(gen_random_uuid(), 'Nhắc trước 1 ngày', 1, false, 'email', true, now(), now()),
(gen_random_uuid(), 'Cảnh báo quá hạn', 0, true, 'email', true, now(), now());

-- 3. Tạo cấu hình Cronjob mặc định
INSERT INTO system_settings (key, value, description, updated_at) VALUES 
('cron_time_1', '08:00', 'Giờ chạy cron job bắt buộc (Lần 1)', now()),
('cron_time_2', '14:00', 'Giờ chạy cron job tùy chọn (Lần 2)', now()),
('cron_enabled_2', 'true', 'Bật/tắt chạy cron job lần 2', now());
