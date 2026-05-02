# BÁO CÁO PHÂN TÍCH YÊU CẦU V2
## Dự án: Document Expiry Reminder

## 1. Tóm tắt phạm vi dự án

Dự án **Document Expiry Reminder** là hệ thống nội bộ dùng để theo dõi thời hạn của văn bản và gửi nhắc hạn tự động qua Email, về sau có thể mở rộng SMS nếu cần.

Hệ thống tập trung vào bài toán:

```text
Văn bản có ngày hiệu lực / ngày hết hạn / ngày cần rà soát / ngày cần gia hạn
→ Gán người hoặc phòng ban phụ trách
→ Hệ thống tự kiểm tra mốc thời gian
→ Gửi nhắc hạn cho người phụ trách
→ Lưu lịch sử nhắc hạn
```

Điểm cần chốt rõ: **MVP không xây dựng hệ thống xử lý văn bản, không mô phỏng luồng chuyển văn bản qua từng cấp, không làm phê duyệt văn bản và không làm workflow nghiệp vụ phức tạp.**

Tên repo đề xuất:

```text
document-expiry-reminder
```

## 2. Bối cảnh nghiệp vụ

Bên nghiệp vụ có mô tả một quy trình thực tế như sau:

```text
Văn thư
→ Chánh văn phòng ủy ban
→ Chủ tịch / các Phó chủ tịch
→ Văn thư phòng Văn thư
→ Lãnh đạo phòng
→ Phó phòng
→ Chuyên viên phụ trách
```

Cách hiểu trong phạm vi MVP:

Quy trình trên là **quy trình thực tế bên ngoài hệ thống để xác định người hoặc phòng ban chịu trách nhiệm cuối cùng đối với văn bản**.

Trong MVP, hệ thống **không cần mô phỏng từng bước chuyển này**. Nghĩa là không cần có màn hình để Văn thư chuyển cho Chánh văn phòng, Chánh văn phòng chuyển cho Chủ tịch/Phó chủ tịch, rồi tiếp tục chuyển qua từng cấp.

Thay vào đó, hệ thống chỉ cần lưu kết quả cuối cùng của quá trình phân công:

```text
Văn bản này thuộc phòng nào?
Ai là người phụ trách chính?
Ngày hết hạn/ngày cần nhắc là ngày nào?
Khi đến hạn thì nhắc ai?
```

## 3. Mục tiêu hệ thống

Mục tiêu chính của hệ thống là giúp cơ quan không bỏ sót các văn bản có thời hạn, đặc biệt là văn bản sắp hết hiệu lực, sắp hết hạn, cần rà soát hoặc cần gia hạn.

Hệ thống cần hỗ trợ:

- Quản lý danh sách văn bản cần theo dõi.
- Lưu các mốc thời gian quan trọng của văn bản.
- Gán người hoặc phòng ban phụ trách văn bản.
- Gửi Email nhắc hạn tự động theo mốc cấu hình.
- Lưu lịch sử gửi thông báo.
- Hiển thị dashboard văn bản còn hiệu lực, sắp hết hạn, đã hết hạn.
- Phân quyền xem/sửa dữ liệu theo vai trò hoặc phòng ban.

## 4. Những gì nằm trong scope MVP

MVP nên tập trung vào các chức năng sau:

1. Đăng nhập và phân quyền cơ bản.
2. Quản lý người dùng.
3. Quản lý phòng ban.
4. Quản lý văn bản.
5. Upload file đính kèm cho văn bản nếu cần.
6. Nhập ngày ban hành, ngày hiệu lực, ngày hết hạn, ngày rà soát, ngày gia hạn.
7. Gán người phụ trách chính hoặc phòng ban phụ trách.
8. Cấu hình mốc nhắc hạn.
9. Gửi Email nhắc hạn tự động.
10. Lưu lịch sử gửi thông báo.
11. Dashboard thống kê văn bản sắp hết hạn, đã hết hạn, còn hiệu lực.
12. Tìm kiếm và lọc văn bản theo trạng thái, phòng ban, người phụ trách, ngày hết hạn.

## 5. Những gì không nằm trong scope MVP

Các chức năng sau không nên đưa vào giai đoạn đầu để tránh phình scope:

- Luân chuyển văn bản qua nhiều cấp.
- Mô phỏng quy trình Văn thư → Chánh văn phòng → Chủ tịch/Phó chủ tịch → Văn thư phòng → Lãnh đạo phòng → Phó phòng → Chuyên viên.
- Phê duyệt văn bản.
- Giao việc xử lý văn bản.
- Theo dõi tiến độ xử lý văn bản.
- Ý kiến chỉ đạo nhiều cấp.
- Ký số.
- Chat nội bộ.
- Mobile app riêng.
- AI tóm tắt văn bản.
- Báo cáo hành chính phức tạp.
- Tích hợp hệ thống quản lý file/tài liệu khác.

Nếu sau này bên nghiệp vụ yêu cầu xử lý văn bản hoặc luân chuyển văn bản qua từng cấp, nên xem đó là một phase mở rộng riêng, không gộp vào MVP hiện tại.

## 6. Cách hiểu về “phân cấp” trong hệ thống

Trong dự án này, “phân cấp” cần được hiểu cẩn thận. Có 3 khái niệm khác nhau:

### 6.1. Phân quyền truy cập

Dùng để xác định ai được xem, thêm, sửa, xóa hoặc cấu hình dữ liệu.

Ví dụ:

```text
Admin xem toàn bộ dữ liệu.
Lãnh đạo phòng xem văn bản thuộc phòng mình.
Chuyên viên chỉ xem văn bản được giao phụ trách hoặc thuộc phạm vi được phân quyền.
Phòng ban A không mặc định xem được văn bản của phòng ban B.
```

Đây là phần nên có trong MVP ở mức cơ bản.

### 6.2. Phân công trách nhiệm

Dùng để xác định văn bản thuộc về ai hoặc phòng ban nào.

Ví dụ:

```text
Văn bản A
→ Phòng phụ trách: Phòng Nội vụ
→ Người phụ trách chính: Nguyễn Văn A
```

Đây là phần bắt buộc cần có trong MVP.

### 6.3. Leo thang thông báo

Dùng để gửi thêm thông báo cho cấp trên khi văn bản gần hết hạn hoặc đã quá hạn.

Ví dụ:

```text
Trước hạn 30 ngày → nhắc người phụ trách chính.
Quá hạn → nhắc người phụ trách chính, có thể CC lãnh đạo phòng nếu nghiệp vụ yêu cầu.
```

Phần này **không nên hard-code trong MVP nếu chưa được xác nhận**. Có thể thiết kế database đủ mềm để mở rộng sau, nhưng triển khai ban đầu nên đơn giản.

Kết luận:

```text
MVP bắt buộc có phân quyền truy cập và gán người/phòng phụ trách.
MVP không bắt buộc có leo thang thông báo nhiều cấp.
```

## 7. Luồng nghiệp vụ chính trong MVP

### 7.1. Luồng nhập văn bản

```text
Người dùng có quyền đăng nhập
↓
Tạo văn bản mới
↓
Nhập thông tin văn bản
↓
Nhập ngày hiệu lực / ngày hết hạn / ngày rà soát / ngày gia hạn nếu có
↓
Upload file đính kèm nếu cần
↓
Gán phòng ban hoặc người phụ trách chính
↓
Bật/tắt nhắc hạn cho văn bản
↓
Lưu văn bản
```

### 7.2. Luồng nhắc hạn tự động

```text
Background job chạy định kỳ
↓
Lấy danh sách văn bản đang bật nhắc hạn
↓
Kiểm tra các mốc ngày liên quan
↓
So sánh với rule nhắc hạn
↓
Nếu đến mốc nhắc thì tạo thông báo
↓
Gửi Email cho người phụ trách
↓
Lưu reminder log
↓
Không gửi trùng cùng một mốc nhắc
```

### 7.3. Luồng xem dashboard

```text
Người dùng đăng nhập
↓
Hệ thống xác định quyền xem dữ liệu
↓
Hiển thị danh sách văn bản theo phạm vi được phép xem
↓
Hiển thị thống kê: còn hiệu lực, sắp hết hạn, đã hết hạn
```

## 8. Trạng thái văn bản đề xuất

MVP có thể dùng bộ trạng thái đơn giản:

```text
Còn hiệu lực
Sắp hết hạn
Đã hết hạn
Đã hủy theo dõi
```

Nếu cần chi tiết hơn, có thể mở rộng:

```text
Chưa có hiệu lực
Còn hiệu lực
Sắp hết hạn
Đã hết hạn
Đã gia hạn
Đã được thay thế
Đã hủy theo dõi
```

Lưu ý: trạng thái này là trạng thái hiệu lực hoặc theo dõi hạn của văn bản, không phải trạng thái xử lý nghiệp vụ.

## 9. Loại ngày cần theo dõi

Một văn bản có thể có nhiều mốc thời gian. MVP có thể hỗ trợ các field sau:

```text
issued_date: ngày ban hành
effective_date: ngày có hiệu lực
expiry_date: ngày hết hạn / hết hiệu lực
review_date: ngày cần rà soát
renewal_date: ngày cần gia hạn
```

Trong MVP, nên ưu tiên `expiry_date` trước. Các ngày `review_date` và `renewal_date` có thể hỗ trợ nếu không làm phức tạp đáng kể UI và reminder logic.

## 10. Quy tắc nhắc hạn

MVP nên có bộ mốc mặc định:

```text
Trước hạn 30 ngày
Trước hạn 15 ngày
Trước hạn 7 ngày
Trước hạn 1 ngày
Khi quá hạn
```

Có thể cho admin bật/tắt hoặc chỉnh số ngày nhắc.

Người nhận mặc định:

```text
Người phụ trách chính của văn bản
```

Tùy chọn mở rộng:

```text
CC lãnh đạo phòng hoặc cấp trên trực tiếp khi văn bản đã quá hạn.
```

Không nên triển khai mặc định cơ chế leo thang nhiều cấp nếu nghiệp vụ chưa xác nhận.

## 11. Yêu cầu phân quyền MVP

Phân quyền MVP nên đủ dùng, không quá phức tạp.

### 11.1. Vai trò đề xuất

```text
Admin
Manager / Lãnh đạo phòng
Staff / Chuyên viên
Viewer nếu cần
```

### 11.2. Quyền đề xuất

Admin:

```text
- Quản lý toàn bộ người dùng, phòng ban, văn bản, rule nhắc hạn.
- Xem toàn bộ dashboard và reminder logs.
```

Manager / Lãnh đạo phòng:

```text
- Xem văn bản thuộc phòng ban mình.
- Có thể tạo/sửa văn bản trong phạm vi phòng nếu được cấp quyền.
- Xem dashboard của phòng ban.
```

Staff / Chuyên viên:

```text
- Xem văn bản được giao phụ trách hoặc văn bản thuộc phạm vi được phân quyền.
- Cập nhật một số thông tin được phép nếu là người phụ trách.
```

Viewer:

```text
- Chỉ xem dữ liệu được phân quyền.
```

## 12. Mô hình dữ liệu đề xuất

### 12.1. Bảng `users`

```text
id
full_name
username
password_hash
email
phone
department_id
position
role
manager_id
status
created_at
updated_at
```

Ghi chú:

- `manager_id` dùng để lưu cấp trên trực tiếp nếu cần.
- Trong MVP, `manager_id` chủ yếu phục vụ tham chiếu tổ chức và có thể dùng cho rule CC cấp trên nếu được bật.
- Không nên mặc định dùng `manager_id` để leo thang nhiều cấp nếu chưa được xác nhận.

### 12.2. Bảng `departments`

```text
id
name
code
parent_id
manager_id
created_at
updated_at
```

### 12.3. Bảng `documents`

```text
id
document_code
document_number
title
summary
document_type
issuer
issued_date
effective_date
expiry_date
review_date
renewal_date
status
reminder_enabled
file_url
created_by
created_at
updated_at
```

### 12.4. Bảng `document_assignments`

```text
id
document_id
user_id
department_id
assignment_type
is_primary
created_at
```

`assignment_type` đề xuất:

```text
owner
viewer
notification_recipient
```

Trong MVP, cần ưu tiên `owner` là người phụ trách chính.

### 12.5. Bảng `reminder_rules`

```text
id
name
date_field
days_before
channel
recipient_scope
is_overdue_rule
is_active
created_at
updated_at
```

`date_field` dùng để xác định rule áp dụng cho ngày nào:

```text
expiry_date
review_date
renewal_date
```

`recipient_scope` đề xuất:

```text
owner
owner_and_direct_manager
custom_users
```

Trong MVP, mặc định dùng:

```text
owner
```

### 12.6. Bảng `reminder_logs`

```text
id
document_id
rule_id
recipient_user_id
channel
recipient_address
subject
message
scheduled_at
sent_at
status
provider_response
date_reference
created_at
```

Cần có unique constraint để chống gửi trùng:

```text
document_id + rule_id + recipient_user_id + date_reference
```

## 13. Reminder Engine

Reminder Engine là phần quan trọng nhất của backend.

Nhiệm vụ:

```text
- Chạy định kỳ bằng background job.
- Lấy danh sách văn bản cần nhắc.
- Tính toán mốc nhắc dựa trên expiry_date/review_date/renewal_date.
- Xác định người nhận.
- Kiểm tra log để tránh gửi trùng.
- Gửi email.
- Ghi reminder log.
```

Pseudo flow:

```text
for each active document where reminder_enabled = true:
    for each active reminder_rule:
        get target_date from document based on rule.date_field
        if target_date is empty:
            skip

        calculate reminder_date = target_date - rule.days_before

        if today matches reminder_date or overdue condition:
            resolve recipients based on rule.recipient_scope
            for each recipient:
                if reminder_log does not exist:
                    send email
                    save reminder_log
```

MVP nên tính theo ngày lịch trước. Chưa nên xử lý ngày làm việc, cuối tuần hoặc ngày lễ nếu nghiệp vụ chưa yêu cầu.

## 14. Email

MVP chỉ cần Email. SMS để phase sau.

Email cần có các nội dung tối thiểu:

```text
- Tiêu đề: Văn bản sắp hết hạn / Văn bản đã quá hạn
- Tên văn bản
- Số/ký hiệu văn bản
- Ngày hết hạn hoặc ngày cần rà soát/gia hạn
- Số ngày còn lại hoặc số ngày quá hạn
- Người/phòng ban phụ trách
- Link mở chi tiết văn bản trong hệ thống
```

Template email MVP có thể cố định. Không nên làm trình chỉnh sửa template phức tạp trong giai đoạn đầu.

## 15. Dashboard và báo cáo MVP

Dashboard nên có:

```text
- Tổng số văn bản đang theo dõi
- Số văn bản còn hiệu lực
- Số văn bản sắp hết hạn
- Số văn bản đã hết hạn
- Danh sách văn bản sắp hết hạn trong 7 ngày
- Danh sách văn bản sắp hết hạn trong 15 ngày
- Danh sách văn bản sắp hết hạn trong 30 ngày
- Danh sách văn bản đã quá hạn
- Thống kê theo phòng ban
- Thống kê theo người phụ trách
```

Bộ lọc nên có:

```text
- Trạng thái
- Phòng ban
- Người phụ trách
- Loại văn bản
- Khoảng ngày hết hạn
```

## 16. Tech stack đề xuất

Với quy mô dưới 100 người dùng, không cần kiến trúc phức tạp.

Đề xuất:

```text
Frontend: Next.js hoặc React + Vite
Backend: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Migration: Alembic
Auth: JWT
File storage: Local storage cho MVP, S3-compatible storage sau này nếu cần
Scheduler: APScheduler cho MVP
Email: SMTP
Deploy: Docker Compose
```

Nếu muốn đơn giản nhất:

```text
Frontend: React + Vite
Backend: FastAPI
Database: PostgreSQL
Scheduler: APScheduler chạy cùng backend
```

Không cần microservices cho MVP.

## 17. Phase triển khai đề xuất

### Phase 1: Foundation

Mục tiêu: dựng nền backend, database, auth, phân quyền cơ bản.

```text
- Setup repo
- Setup backend FastAPI
- Setup PostgreSQL + Alembic
- Tạo bảng users, departments
- Auth: login, refresh token, change password
- CRUD users
- CRUD departments
- Setup frontend layout
- Login page
```

### Phase 2: Document Management

Mục tiêu: quản lý văn bản và gán người/phòng phụ trách.

```text
- Tạo bảng documents
- Tạo bảng document_assignments
- API CRUD documents
- Upload file
- Search/filter/pagination
- UI danh sách văn bản
- UI tạo/sửa văn bản
- UI gán người/phòng phụ trách
```

### Phase 3: Reminder Engine

Mục tiêu: nhắc hạn tự động qua Email.

```text
- Tạo bảng reminder_rules
- Tạo bảng reminder_logs
- CRUD reminder_rules
- Background scheduler
- Logic tính mốc nhắc
- Logic xác định người nhận mặc định: owner
- Chống gửi trùng bằng reminder_logs
- Gửi Email qua SMTP
- Trang xem lịch sử nhắc hạn
```

Optional nếu nghiệp vụ xác nhận:

```text
- CC cấp trên trực tiếp khi văn bản quá hạn
```

Không triển khai mặc định:

```text
- Leo thang nhiều cấp theo manager_id chain
- Nhắc lặp lại quá hạn nhiều lần
```

### Phase 4: Dashboard, Testing, Deploy

```text
- API thống kê dashboard
- UI dashboard
- Test reminder engine
- Test phân quyền
- Test gửi email bằng Mailtrap/MailHog
- Docker Compose
- Viết README hướng dẫn chạy dự án
```

## 18. Giả định MVP cần chốt

Các giả định sau nên được gửi cho bên nghiệp vụ hoặc PM xác nhận:

| STT | Vấn đề | Giả định MVP |
|---|---|---|
| 1 | Hệ thống có xử lý/luân chuyển văn bản không? | Không. Chỉ nhắc hạn văn bản. |
| 2 | Quy trình phân cấp thực tế có đưa vào hệ thống không? | Không mô phỏng từng bước trong MVP. |
| 3 | Hệ thống có upload file không? | Có, ở mức file đính kèm đơn giản. |
| 4 | Một văn bản gán cho ai? | Gán người phụ trách chính, có thể kèm phòng ban. |
| 5 | Nhắc cho ai? | Mặc định nhắc người phụ trách chính. |
| 6 | Có nhắc cấp trên không? | Optional, chỉ bật nếu nghiệp vụ xác nhận. |
| 7 | Có SMS trong MVP không? | Không. MVP chỉ Email. |
| 8 | Mốc nhắc cố định hay tùy chỉnh? | Có mốc mặc định, admin có thể cấu hình. |
| 9 | Tính ngày lịch hay ngày làm việc? | MVP tính theo ngày lịch. |
| 10 | Có xác nhận đã nhận thông báo không? | Không trong MVP. |
| 11 | Ai xem toàn bộ dữ liệu? | Admin. Có thể thêm lãnh đạo cấp cao nếu cần. |
| 12 | User thường xem gì? | Chỉ xem văn bản thuộc phạm vi được phân quyền. |
| 13 | Ai sửa ngày hết hạn? | Admin hoặc người có quyền quản lý văn bản. |
| 14 | Có nhắc lặp lại khi quá hạn không? | Chưa làm mặc định. Có thể mở rộng sau. |
| 15 | Có quản lý file phân quyền đầy đủ không? | Không trong scope hiện tại. |

## 19. Câu hỏi cần hỏi lại bên nghiệp vụ

Trước khi dev chính thức, nên chốt các câu sau:

1. Hệ thống chỉ nhắc hạn văn bản, đúng không? Không cần luân chuyển văn bản qua từng cấp trong phần mềm?
2. Quy trình Văn thư → Chánh văn phòng → Chủ tịch/Phó chủ tịch → Văn thư phòng → Lãnh đạo phòng → Phó phòng → Chuyên viên chỉ là quy trình thực tế để xác định người phụ trách cuối cùng, đúng không?
3. Văn bản cần theo dõi loại ngày nào: ngày hết hiệu lực, ngày hết hạn, ngày rà soát, ngày gia hạn?
4. Một văn bản có thể có nhiều ngày cần nhắc không?
5. Mỗi văn bản gán cho một người phụ trách chính hay một phòng ban phụ trách?
6. Nếu gán phòng ban, email nhắc gửi cho ai trong phòng ban?
7. Khi sắp hết hạn, chỉ nhắc người phụ trách hay có cần CC cấp trên?
8. Khi quá hạn, có cần nhắc cấp trên không?
9. Nếu cần nhắc cấp trên, cấp trên là lãnh đạo phòng, phó phòng hay người được cấu hình riêng?
10. Các mốc nhắc mặc định là 30/15/7/1 ngày có phù hợp không?
11. Email là đủ cho MVP hay bắt buộc có SMS ngay?
12. Người dùng có cần xác nhận đã nhận thông báo không?
13. Có cần upload file văn bản không?
14. Phân quyền xem văn bản theo phòng ban cần chặt tới mức nào?
15. Admin có quyền sửa toàn bộ ngày hết hạn và người phụ trách không?

## 20. Rủi ro scope

Rủi ro lớn nhất là dự án bị kéo từ “nhắc hạn văn bản” thành “hệ thống xử lý văn bản”.

Hai bài toán này khác nhau:

### Nhắc hạn văn bản

```text
Văn bản
→ Ngày hết hạn
→ Người phụ trách
→ Rule nhắc
→ Email
```

Scope nhỏ đến trung bình, phù hợp MVP.

### Xử lý văn bản / workflow

```text
Văn bản
→ Luân chuyển nhiều cấp
→ Phê duyệt
→ Ý kiến chỉ đạo
→ Phân công
→ Theo dõi xử lý
→ Báo cáo tiến độ
```

Scope lớn hơn nhiều, không nên đưa vào MVP.

Vì vậy, trong tài liệu và khi trao đổi với dev, cần nhấn mạnh:

```text
MVP không triển khai workflow chuyển văn bản qua từng cấp.
Chỉ quản lý văn bản, thời hạn, người/phòng phụ trách và nhắc hạn tự động.
```

## 21. Định nghĩa MVP cuối cùng

MVP của Document Expiry Reminder là:

```text
Một hệ thống web nội bộ cho phép người dùng có quyền nhập văn bản, khai báo ngày hiệu lực/ngày hết hạn/ngày rà soát, gán người hoặc phòng ban phụ trách, sau đó hệ thống tự động gửi Email nhắc hạn cho người phụ trách theo các mốc được cấu hình và lưu lịch sử gửi thông báo.
```

Không làm trong MVP:

```text
Không luân chuyển văn bản qua từng cấp.
Không xử lý/phê duyệt văn bản.
Không giao việc chi tiết.
Không workflow nhiều bước.
Không leo thang thông báo nhiều cấp nếu chưa xác nhận.
```

## 22. README description đề xuất

Tiếng Việt:

```text
Document Expiry Reminder là hệ thống nội bộ dùng để theo dõi ngày hiệu lực, ngày hết hạn, ngày rà soát hoặc ngày gia hạn của văn bản và gửi Email nhắc hạn tự động cho người/phòng ban phụ trách.
```

Tiếng Anh:

```text
Document Expiry Reminder is a lightweight internal web system for tracking document validity, expiry, review, and renewal dates, then sending automated email reminders to responsible users or departments.
```

## 23. Kết luận

Tên repo `document-expiry-reminder` vẫn phù hợp với scope hiện tại.

Dự án nên được triển khai theo hướng nhỏ gọn:

```text
Document management metadata
+ Expiry/review/renewal dates
+ Owner assignment
+ Email reminder engine
+ Reminder logs
+ Basic access control
+ Dashboard
```

Không nên thiết kế thành hệ thống workflow xử lý văn bản. Quy trình phân cấp bên nghiệp vụ chỉ nên được dùng để hiểu cách cơ quan xác định người/phòng ban phụ trách cuối cùng, còn trong MVP hệ thống chỉ cần lưu người/phòng phụ trách và gửi nhắc hạn.

