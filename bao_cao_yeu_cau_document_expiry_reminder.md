# BÁO CÁO PHÂN TÍCH YÊU CẦU BAN ĐẦU
## Dự án: Hệ thống nhắc hạn văn bản theo phân cấp

## 1. Bối cảnh

Cơ quan cần xây dựng một hệ thống nội bộ để theo dõi các mốc thời gian quan trọng của văn bản, đặc biệt là ngày hết hạn, ngày hết hiệu lực, ngày cần rà soát hoặc ngày cần gia hạn. Khi văn bản sắp đến hạn hoặc đã quá hạn, hệ thống sẽ tự động gửi thông báo nhắc nhở qua Email hoặc SMS cho người phụ trách.

Điểm cần làm rõ là hệ thống này không phải là phần mềm xử lý văn bản, không phải hệ thống luân chuyển công văn qua nhiều cấp, cũng không phải hệ thống giao việc/phê duyệt văn bản. Trọng tâm của hệ thống là nhắc hạn tự động dựa trên thông tin văn bản và cơ cấu phân cấp người dùng trong cơ quan.

Nói ngắn gọn, bài toán là:

```text
Văn bản có thời hạn
→ Gán người hoặc đơn vị phụ trách
→ Hệ thống theo dõi mốc thời gian
→ Tự động gửi nhắc hạn
→ Nếu cần thì báo lên cấp trên theo phân cấp
```

## 2. Mục tiêu dự án

Mục tiêu chính của hệ thống là giúp cơ quan không bỏ sót các văn bản sắp hết hạn, hết hiệu lực, cần gia hạn hoặc cần rà soát định kỳ.

Hệ thống cần hỗ trợ:

- Lưu trữ thông tin cơ bản của văn bản.
- Quản lý ngày hiệu lực, ngày hết hạn, ngày cần rà soát hoặc ngày cần gia hạn.
- Gán người hoặc phòng ban chịu trách nhiệm theo dõi văn bản.
- Tự động gửi nhắc hạn qua Email, giai đoạn sau có thể mở rộng SMS.
- Nhắc theo phân cấp quản lý khi văn bản gần hết hạn hoặc đã quá hạn.
- Lưu lịch sử gửi thông báo để phục vụ kiểm tra và truy vết.
- Cung cấp dashboard để theo dõi văn bản còn hiệu lực, sắp hết hạn và đã hết hạn.

## 3. Phạm vi hiện tại

### 3.1. Trong phạm vi

Phiên bản đầu tiên nên tập trung vào các chức năng sau:

1. Đăng nhập và phân quyền cơ bản.
2. Quản lý người dùng.
3. Quản lý phòng ban, chức vụ và cấp trên trực tiếp.
4. Quản lý danh sách văn bản.
5. Upload file đính kèm cho văn bản nếu cần.
6. Nhập ngày ban hành, ngày hiệu lực, ngày hết hạn, ngày cần rà soát/gia hạn.
7. Gán người hoặc phòng ban phụ trách văn bản.
8. Cấu hình mốc nhắc hạn, ví dụ trước 30 ngày, 15 ngày, 7 ngày, 1 ngày.
9. Gửi Email nhắc hạn tự động.
10. Lưu lịch sử gửi thông báo.
11. Dashboard thống kê văn bản sắp hết hạn, đã hết hạn, còn hiệu lực.

### 3.2. Ngoài phạm vi giai đoạn đầu

Các chức năng sau không nên đưa vào MVP để tránh phình phạm vi:

- Luân chuyển văn bản qua nhiều cấp.
- Phê duyệt văn bản.
- Giao việc xử lý văn bản.
- Workflow phức tạp.
- Ký số.
- Chat nội bộ.
- Mobile app riêng.
- AI tóm tắt văn bản.
- Báo cáo hành chính quá chi tiết.
- Tích hợp sâu với hệ thống quản lý văn bản khác.

Nếu sau này cơ quan xác nhận cần xử lý văn bản hoặc giao việc, đó nên được xem là giai đoạn mở rộng riêng, không nên gộp vào MVP.

## 4. Cách hiểu đúng về “phân cấp” trong hệ thống

Cụm “phân cấp” trong bài toán này không nên hiểu là văn bản phải đi qua từng cấp để xử lý. Thay vào đó, phân cấp được dùng để xác định người nhận thông báo và cấp quản lý cần được cảnh báo.

Ví dụ cơ cấu người dùng:

```text
Chuyên viên
↓
Phó phòng
↓
Trưởng phòng
↓
Chánh văn phòng / Lãnh đạo phụ trách
```

Khi một văn bản được gán cho chuyên viên phụ trách, hệ thống có thể nhắc theo mức độ như sau:

```text
Trước hạn 30 ngày:
→ Nhắc chuyên viên phụ trách

Trước hạn 15 ngày:
→ Nhắc chuyên viên + phó phòng

Trước hạn 7 ngày:
→ Nhắc chuyên viên + phó phòng + trưởng phòng

Sau khi quá hạn:
→ Cảnh báo chuyên viên + các cấp quản lý liên quan
```

Như vậy, phân cấp ở đây phục vụ cho cơ chế leo thang thông báo, không phải quy trình xử lý văn bản.

## 5. Đối tượng chính trong hệ thống

### 5.1. Văn bản

Văn bản là đối tượng trung tâm của hệ thống.

Thông tin đề xuất:

- Mã văn bản.
- Số/ký hiệu văn bản.
- Tên hoặc trích yếu văn bản.
- Loại văn bản.
- Cơ quan ban hành.
- Ngày ban hành.
- Ngày có hiệu lực.
- Ngày hết hiệu lực.
- Ngày cần rà soát.
- Ngày cần gia hạn.
- File đính kèm.
- Người phụ trách chính.
- Phòng ban phụ trách.
- Trạng thái văn bản.
- Ghi chú.

### 5.2. Người dùng

Người dùng là cán bộ, nhân sự hoặc tài khoản nội bộ trong cơ quan.

Thông tin đề xuất:

- Họ tên.
- Email.
- Số điện thoại.
- Tên đăng nhập.
- Mật khẩu đã mã hóa.
- Phòng ban.
- Chức vụ.
- Vai trò hệ thống.
- Cấp trên trực tiếp.
- Trạng thái tài khoản.

Trường quan trọng nhất để phục vụ phân cấp là `manager_id`. Trường này cho biết cấp trên trực tiếp của người dùng.

Ví dụ:

```text
Chuyên viên A.manager_id = Phó phòng B
Phó phòng B.manager_id = Trưởng phòng C
Trưởng phòng C.manager_id = Chánh văn phòng D
```

Từ đó hệ thống có thể tự xác định chuỗi cấp trên khi cần gửi thông báo leo thang.

### 5.3. Phòng ban

Phòng ban dùng để nhóm người dùng và gán trách nhiệm theo đơn vị.

Thông tin đề xuất:

- Tên phòng ban.
- Mã phòng ban.
- Phòng ban cha nếu có.
- Lãnh đạo phòng.
- Ghi chú.

### 5.4. Quy tắc nhắc hạn

Quy tắc nhắc hạn quy định khi nào hệ thống gửi thông báo và gửi cho ai.

Ví dụ các mốc nhắc:

- Trước hạn 30 ngày.
- Trước hạn 15 ngày.
- Trước hạn 7 ngày.
- Trước hạn 1 ngày.
- Khi đã quá hạn.

Mỗi mốc nhắc có thể cấu hình người nhận:

- Người phụ trách chính.
- Cấp trên trực tiếp.
- Lãnh đạo phòng.
- Admin hoặc người giám sát.

### 5.5. Lịch sử nhắc hạn

Hệ thống cần lưu lại log gửi thông báo để biết thông báo đã được gửi hay chưa, gửi lúc nào, gửi cho ai và kết quả gửi ra sao.

Thông tin đề xuất:

- Văn bản liên quan.
- Người nhận.
- Kênh gửi: Email/SMS.
- Nội dung thông báo.
- Thời điểm gửi.
- Trạng thái gửi: thành công/thất bại.
- Phản hồi từ hệ thống gửi mail/SMS nếu có.

## 6. Luồng nghiệp vụ chính

### 6.1. Luồng nhập văn bản

```text
Người dùng đăng nhập
↓
Tạo văn bản mới
↓
Nhập thông tin văn bản
↓
Nhập ngày hiệu lực, ngày hết hạn hoặc ngày cần rà soát
↓
Upload file đính kèm nếu có
↓
Gán người hoặc phòng ban phụ trách
↓
Lưu văn bản
```

Sau khi lưu, văn bản sẽ được hệ thống đưa vào danh sách theo dõi hạn.

### 6.2. Luồng kiểm tra hạn tự động

```text
Background job chạy định kỳ
↓
Lấy danh sách văn bản đang được theo dõi
↓
So sánh ngày hiện tại với ngày hết hạn/ngày cần nhắc
↓
Nếu đến mốc nhắc, tạo thông báo
↓
Gửi Email/SMS cho người liên quan
↓
Lưu lịch sử gửi thông báo
```

Background job có thể chạy theo chu kỳ, ví dụ mỗi ngày một lần vào buổi sáng, hoặc mỗi vài giờ nếu cần kiểm tra sát hơn.

### 6.3. Luồng nhắc theo phân cấp

```text
Văn bản sắp đến hạn
↓
Nhắc người phụ trách chính
↓
Nếu gần hạn hơn hoặc đã quá hạn
↓
Nhắc thêm cấp trên trực tiếp
↓
Nếu vẫn quá hạn
↓
Báo lên cấp cao hơn theo cấu hình
```

Ví dụ:

```text
Ngày hết hạn: 31/12/2026

Ngày 01/12/2026:
→ Nhắc chuyên viên phụ trách

Ngày 16/12/2026:
→ Nhắc chuyên viên + phó phòng

Ngày 24/12/2026:
→ Nhắc chuyên viên + phó phòng + trưởng phòng

Ngày 01/01/2027:
→ Gửi cảnh báo quá hạn
```

## 7. Trạng thái văn bản đề xuất

Phiên bản MVP có thể dùng các trạng thái đơn giản:

- Còn hiệu lực.
- Sắp hết hạn.
- Đã hết hạn.
- Đã hủy theo dõi.

Nếu cần chi tiết hơn, có thể mở rộng:

- Chưa có hiệu lực.
- Còn hiệu lực.
- Sắp hết hạn.
- Đã hết hạn.
- Đã gia hạn.
- Đã được thay thế.
- Đã hủy theo dõi.

Cần lưu ý: trạng thái này là trạng thái hiệu lực/theo dõi hạn của văn bản, không phải trạng thái xử lý nghiệp vụ.

## 8. Chức năng đề xuất cho MVP

### 8.1. Quản lý tài khoản

- Đăng nhập.
- Đăng xuất.
- Đổi mật khẩu.
- Admin tạo/sửa/khóa tài khoản.
- Gán vai trò và phòng ban.
- Gán cấp trên trực tiếp.

### 8.2. Quản lý phòng ban

- Tạo phòng ban.
- Sửa thông tin phòng ban.
- Gán lãnh đạo phòng.
- Thiết lập phòng ban cha nếu có phân cấp đơn vị.

### 8.3. Quản lý văn bản

- Tạo văn bản mới.
- Cập nhật thông tin văn bản.
- Upload file đính kèm.
- Tìm kiếm văn bản.
- Lọc theo trạng thái, phòng ban, người phụ trách, thời gian hết hạn.
- Hủy theo dõi văn bản nếu không còn cần nhắc.

### 8.4. Gán trách nhiệm theo dõi

- Gán người phụ trách chính.
- Gán phòng ban phụ trách.
- Gán người xem hoặc người nhận thông báo bổ sung nếu cần.

### 8.5. Cấu hình nhắc hạn

- Cấu hình các mốc nhắc trước hạn.
- Cấu hình kênh gửi thông báo.
- Cấu hình người nhận theo từng mốc.
- Cấu hình nội dung email mẫu.

### 8.6. Gửi thông báo tự động

- Gửi email khi văn bản đến mốc nhắc.
- Gửi email cảnh báo khi văn bản quá hạn.
- Ghi nhận trạng thái gửi.
- Tránh gửi trùng một mốc nhắc nhiều lần.

### 8.7. Dashboard và báo cáo cơ bản

Dashboard nên có:

- Tổng số văn bản đang theo dõi.
- Số văn bản còn hiệu lực.
- Số văn bản sắp hết hạn.
- Số văn bản đã hết hạn.
- Danh sách văn bản sắp hết hạn trong 7/15/30 ngày.
- Danh sách văn bản quá hạn.
- Thống kê theo phòng ban.
- Thống kê theo người phụ trách.

## 9. Đề xuất mô hình dữ liệu ban đầu

### 9.1. Bảng `users`

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

### 9.2. Bảng `departments`

```text
id
name
code
parent_id
manager_id
created_at
updated_at
```

### 9.3. Bảng `documents`

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
file_url
created_by
created_at
updated_at
```

### 9.4. Bảng `document_assignments`

```text
id
document_id
user_id
department_id
assignment_type
is_primary
created_at
```

`assignment_type` có thể gồm:

```text
owner
manager
viewer
notification_recipient
```

### 9.5. Bảng `reminder_rules`

```text
id
name
days_before_expiry
channel
recipient_scope
is_active
created_at
updated_at
```

`recipient_scope` có thể gồm:

```text
owner
owner_and_direct_manager
owner_and_department_manager
custom
```

### 9.6. Bảng `reminder_logs`

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
created_at
```

## 10. Gợi ý kiến trúc kỹ thuật

Với quy mô dưới 100 người dùng, không cần dùng kiến trúc phức tạp. Một backend monolith là đủ.

Đề xuất:

```text
Frontend: React / Next.js
Backend: FastAPI / NestJS / Laravel
Database: PostgreSQL
File storage: Local storage hoặc S3-compatible storage
Background job: APScheduler / Celery / BullMQ
Email: SMTP nội bộ hoặc SMTP provider
SMS: tích hợp sau qua SMS gateway nếu cần
```

Kiến trúc tổng quát:

```text
Web App
↓
Backend API
↓
PostgreSQL
↓
Background Worker
↓
Email/SMS Provider
```

Email và SMS nên được xử lý qua background job, không gửi trực tiếp trong request chính để tránh làm chậm giao diện.

## 11. Một số rule kỹ thuật cần lưu ý

### 11.1. Không gửi trùng thông báo

Cần đảm bảo một mốc nhắc chỉ gửi một lần cho một văn bản và một người nhận.

Ví dụ:

```text
Văn bản A - mốc trước hạn 30 ngày - gửi cho user X
```

Sau khi đã gửi, hệ thống phải lưu log. Lần chạy background job tiếp theo không được gửi lại cùng mốc đó nếu chưa có lý do rõ ràng.

### 11.2. Tính ngày nhắc

Cần xác định rõ hệ thống tính theo ngày lịch hay ngày làm việc.

Ví dụ:

- Nếu văn bản hết hạn ngày 31/12/2026.
- Rule nhắc trước 30 ngày.
- Ngày gửi nhắc là 01/12/2026 nếu tính theo ngày lịch.

Nếu tính theo ngày làm việc thì logic sẽ phức tạp hơn vì cần cấu hình thứ Bảy, Chủ nhật và ngày nghỉ lễ.

### 11.3. Cấp trên trực tiếp

Nên lưu `manager_id` trong bảng người dùng để xác định cấp trên trực tiếp. Cách này đơn giản và phù hợp cho MVP.

Khi cần gửi thông báo lên cấp trên, hệ thống có thể truy ngược chuỗi `manager_id`.

### 11.4. Trạng thái văn bản

Có thể cập nhật trạng thái bằng background job:

```text
Nếu ngày hiện tại < ngày hết hạn và chưa vào ngưỡng sắp hết hạn → Còn hiệu lực
Nếu ngày hiện tại nằm trong ngưỡng sắp hết hạn → Sắp hết hạn
Nếu ngày hiện tại > ngày hết hạn → Đã hết hạn
```

Ngưỡng “sắp hết hạn” có thể lấy theo rule lớn nhất, ví dụ 30 ngày.

## 12. Các câu hỏi cần chốt với bên nghiệp vụ

Trước khi dev chính thức, cần hỏi lại bên yêu cầu các điểm sau:

1. Hệ thống chỉ nhắc hạn văn bản, đúng không? Không xử lý luân chuyển văn bản?
2. Loại hạn cần theo dõi là ngày hết hiệu lực, ngày hết hạn, ngày rà soát hay ngày gia hạn?
3. Một văn bản có thể có nhiều ngày cần nhắc không?
4. Mỗi văn bản gán cho một người phụ trách hay một phòng ban phụ trách?
5. Nếu gán phòng ban, thông báo gửi cho ai trong phòng ban?
6. Cấp trên được xác định theo sơ đồ tổ chức hay chọn riêng cho từng văn bản?
7. Các mốc nhắc là cố định hay tùy chỉnh theo từng loại văn bản?
8. Email là bắt buộc, SMS có cần trong MVP không?
9. Khi quá hạn, hệ thống nhắc bao nhiêu lần?
10. Có cần người dùng xác nhận đã nhận thông báo không?
11. Có cần trạng thái “đã gia hạn” hoặc “đã thay thế” không?
12. Có cần upload file văn bản không?
13. Có cần phân quyền theo phòng ban không?
14. Ai được xem toàn bộ văn bản?
15. Ai được sửa ngày hết hạn của văn bản?

## 13. Rủi ro phạm vi

Rủi ro lớn nhất là bài toán bị kéo từ “nhắc hạn văn bản” sang “quản lý xử lý văn bản”. Hai bài toán này khác nhau rất nhiều.

Nếu làm nhắc hạn văn bản, hệ thống tương đối gọn:

```text
Văn bản
→ Ngày hết hạn
→ Người phụ trách
→ Rule nhắc
→ Email/SMS
```

Nếu làm xử lý văn bản, hệ thống sẽ lớn hơn nhiều:

```text
Văn bản
→ Quy trình luân chuyển
→ Phê duyệt
→ Giao việc
→ Ý kiến chỉ đạo
→ Theo dõi xử lý
→ Báo cáo tiến độ
```

Vì vậy, cần chốt rõ phạm vi với bên yêu cầu trước khi dev.

## 14. Đề xuất tên repo

Tên repo nên phản ánh đúng phạm vi hiện tại, tránh dùng các từ như `workflow`, `task`, `processing` nếu hệ thống không xử lý văn bản.

Tên đề xuất chính:

```text
document-expiry-reminder
```

Ý nghĩa:

```text
document = văn bản
expiry = hết hạn/hết hiệu lực
reminder = nhắc hạn
```

Tên thay thế:

```text
document-validity-tracker
document-reminder-system
hierarchical-document-reminder
```

Khuyến nghị dùng:

```text
document-expiry-reminder
```

Tên này sát với bài toán ban đầu, không quá rộng và không gây hiểu nhầm thành hệ thống xử lý văn bản.

## 15. Kết luận

Dự án nên được định nghĩa là hệ thống nhắc hạn văn bản theo phân cấp người dùng. Hệ thống không xử lý nội dung văn bản, không luân chuyển văn bản qua nhiều cấp, không phê duyệt và không giao việc phức tạp trong giai đoạn đầu.

Phạm vi MVP nên tập trung vào việc nhập văn bản, gán người phụ trách, theo dõi ngày hết hạn/ngày hiệu lực, gửi nhắc tự động qua Email và lưu lịch sử thông báo. Phần phân cấp được dùng để xác định người nhận thông báo và cấp quản lý cần được cảnh báo khi gần đến hạn hoặc quá hạn.

Mô tả ngắn cho dự án:

```text
Hệ thống nội bộ dùng để theo dõi ngày hiệu lực, ngày hết hạn của văn bản và tự động gửi nhắc hạn qua Email/SMS cho người phụ trách theo phân cấp quản lý.
```

Mô tả tiếng Anh cho README:

```text
A lightweight internal system for tracking document validity and expiry dates, then sending automated email/SMS reminders to responsible users and their managers based on organizational hierarchy.
```

