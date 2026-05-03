# Hướng dẫn Deploy Production
# Backend: Render | Frontend: Vercel

## BƯỚC 1: Deploy Backend lên Render

### 1.1 Tạo Web Service trên Render
1. Vào https://dashboard.render.com → New → Web Service
2. Connect GitHub repo → chọn `document-expiry-reminder`
3. Cấu hình:
   - **Name:** `document-expiry-reminder-api`
   - **Region:** Singapore (gần VN nhất)
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Starter ($7/tháng) hoặc Pro

### 1.2 Thiết lập Environment Variables trên Render
Vào tab "Environment" và thêm TẤT CẢ các biến trong file `.env`:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJ...` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJ...` |
| `DATABASE_URL` | `postgresql+asyncpg://...` |
| `SUPABASE_STORAGE_BUCKET` | `documents` |
| `SUPABASE_S3_ENDPOINT` | `https://xxx.storage.supabase.co/storage/v1/s3` |
| `SUPABASE_S3_ACCESS_KEY` | `...` |
| `SUPABASE_S3_SECRET_KEY` | `...` |
| `SUPABASE_S3_REGION` | `ap-northeast-1` |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `your-email@gmail.com` |
| `SMTP_PASSWORD` | `xxxx xxxx xxxx xxxx` |
| `SMTP_FROM_EMAIL` | `your-email@gmail.com` |
| `SMTP_FROM_NAME` | `Hệ thống Nhắc hạn Văn bản` |
| `APP_NAME` | `Document Expiry Reminder` |
| `APP_ENV` | `production` |
| `CORS_ORIGINS` | `https://your-app.vercel.app` |

> ⚠️ **CORS_ORIGINS**: Phải là URL chính xác của Frontend trên Vercel (không có dấu `/` ở cuối).

### 1.3 Sau khi deploy xong
- Render sẽ cho bạn URL dạng: `https://document-expiry-reminder-api.onrender.com`
- Test: Mở `https://your-app.onrender.com/api/health` → phải trả về `{"status":"ok"}`

---

## BƯỚC 2: Deploy Frontend lên Vercel

### 2.1 Tạo project trên Vercel
1. Vào https://vercel.com → New Project → Import GitHub repo
2. Cấu hình:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### 2.2 Thiết lập Environment Variables trên Vercel
Chỉ cần **1 biến duy nhất**:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://document-expiry-reminder-api.onrender.com/api` |

> ⚠️ Phải có `/api` ở cuối URL.

### 2.3 Sau khi deploy xong
- Vercel sẽ cho bạn URL dạng: `https://your-app.vercel.app`
- **QUAN TRỌNG:** Quay lại Render → sửa `CORS_ORIGINS` thành URL Vercel này.

---

## BƯỚC 3: Kiểm tra cuối cùng
1. Mở `https://your-app.vercel.app` → Login bằng tài khoản Admin.
2. Thử thêm 1 văn bản → Kiểm tra trang Cấu hình Nhắc nhở.
3. Bấm "Chạy Nhắc nhở Ngay" → Kiểm tra Gmail có nhận được email không.
4. Đổi giờ Cronjob → Lưu → Xác nhận thông báo thành công.

---

## Lưu ý Quan trọng
- **Vercel** tự động redeploy khi push code lên GitHub.
- **Render** cũng tự động redeploy khi push code. Trong lúc deploy (~2-3 phút), app sẽ offline tạm thời.
- **Supabase Free Tier** sẽ pause DB sau 7 ngày không hoạt động. Nếu dùng cho production, nên upgrade lên Supabase Pro ($25/tháng) hoặc đảm bảo backend Render ping DB thường xuyên (APScheduler đã làm việc này tự động).
