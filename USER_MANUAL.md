# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG NHẮC HẠN VĂN BẢN
*(Tài liệu dành cho Quản trị viên và Nhân viên sử dụng)*

---

## 1. GIỚI THIỆU CHUNG
Hệ thống **Nhắc hạn Văn bản** là giải pháp phần mềm giúp các cơ quan, tổ chức số hóa và quản lý vòng đời của các văn bản, hợp đồng, giấy phép. Điểm nổi bật nhất của hệ thống là khả năng **tự động gửi email nhắc nhở** cho người phụ trách khi văn bản sắp đến hạn hoặc đã quá hạn, giúp ngăn chặn rủi ro pháp lý và tài chính do việc quên gia hạn giấy tờ gây ra.

---

## 2. PHÂN QUYỀN TRUY CẬP (ROLES)

Hệ thống được chia thành 2 cấp độ quyền:

### 2.1. Quản trị viên (Admin)
- **Toàn quyền hệ thống:** Có thể xem, thêm, sửa, xóa mọi dữ liệu.
- **Tính năng độc quyền:** 
  - Quản lý cơ cấu Phòng ban / Đơn vị.
  - Quản lý tài khoản Nhân viên (cấp quyền, khóa tài khoản).
  - Thiết lập các Quy tắc nhắc nhở (Gửi trước bao nhiêu ngày, nội dung mẫu email).
  - Truy cập **Thùng rác** để kiểm soát các văn bản đã bị nhân viên xóa (Tránh việc xóa nhầm hoặc phá hoại).
  - Kiểm tra Lịch sử gửi mail (Log) của toàn hệ thống.

### 2.2. Nhân viên (User)
- **Quyền hạn cơ bản:** 
  - Thêm mới, chỉnh sửa, xóa (xóa mềm) các văn bản do mình tạo ra hoặc phụ trách.
  - Xem danh sách văn bản của phòng ban mình.
  - Tải lên/Tải xuống file đính kèm của văn bản.
  - Nhận email nhắc nhở tự động.

---

## 3. HƯỚNG DẪN SỬ DỤNG CÁC TÍNH NĂNG CHÍNH

### 3.1. Đăng nhập hệ thống
1. Truy cập vào đường dẫn trang web.
2. Nhập **Email** và **Mật khẩu** do Quản trị viên cấp.
3. Bấm **Đăng nhập**.

### 3.2. Quản lý Văn bản / Giấy tờ (Dành cho mọi người)
Đây là tính năng cốt lõi. Mỗi văn bản đưa lên hệ thống sẽ đi kèm một **Ngày hết hạn**.

*   **Thêm mới văn bản:**
    *   Vào menu **Văn bản** > Bấm **Thêm mới**.
    *   Điền các thông tin: Số/Ký hiệu, Trích yếu (Tên văn bản), Phòng ban lưu trữ, Người phụ trách (sẽ nhận email).
    *   **Quan trọng:** Chọn chính xác *Ngày hết hạn*. Hệ thống sẽ tự động gán trạng thái (Còn hiệu lực / Sắp hết hạn / Hết hạn) dựa trên ngày này.
    *   Bấm Lưu lại.
*   **Tải file đính kèm:** Sau khi tạo xong văn bản, bấm vào biểu tượng đính kèm (Hình cái kẹp giấy) để upload bản scan (PDF, Word, ảnh) lên hệ thống.
*   **Xóa văn bản:** Khi xóa, văn bản sẽ không biến mất hoàn toàn mà được chuyển vào **Thùng rác** (Chỉ Admin mới thấy được).

### 3.3. Quản lý Phòng ban (Dành cho Admin)
*   Vào menu **Phòng ban**.
*   Có thể tạo phòng ban Cha/Con (Ví dụ: Khối Kinh Tế -> Khoa Quản trị kinh doanh).
*   *Lưu ý:* Không thể xóa một Phòng ban nếu bên trong đang có Nhân viên. Hệ thống sẽ cảnh báo yêu cầu chuyển nhân viên đi nơi khác trước khi xóa.

### 3.4. Quản lý Nhân viên (Dành cho Admin)
*   Vào menu **Nhân viên**.
*   Có thể thêm nhân viên mới, gán vào các phòng ban tương ứng.
*   Thiết lập Quyền: Chọn `Admin` hoặc `User`.
*   Khóa tài khoản: Nếu nhân viên nghỉ việc, có thể chuyển trạng thái từ `Đang hoạt động` sang `Bị khóa` để chặn đăng nhập mà không làm mất lịch sử dữ liệu của họ.

### 3.5. Cấu hình Quy tắc Nhắc nhở (Dành cho Admin)
Đây là "bộ não" của hệ thống gửi mail.
*   Vào menu **Cấu hình Nhắc nhở** > Tab **Quy tắc**.
*   **Thêm quy tắc mới:**
    *   Tên quy tắc: Ví dụ *"Nhắc trước 30 ngày"*.
    *   Thời gian: Nhập số `30` (Hệ thống sẽ đếm ngược từ ngày hết hạn trừ đi 30 ngày để gửi mail).
    *   Check vào **Dành cho văn bản đã quá hạn** nếu bạn muốn tạo quy tắc nhắc nhở các văn bản đã trễ hạn.
*   **Tùy biến Mẫu Email (Template):** Bạn có thể tự soạn nội dung email gửi đi. Sử dụng các biến sau để hệ thống tự điền dữ liệu tự động:
    *   `{{document_title}}`: Tên văn bản
    *   `{{document_number}}`: Số ký hiệu
    *   `{{expiry_date}}`: Ngày hết hạn
    *   `{{days_left}}`: Số ngày còn lại

### 3.6. Giám sát Lịch sử gửi Email & Thùng rác (Dành cho Admin)
*   **Lịch sử Nhắc nhở:** Chuyển sang Tab "Lịch sử nhắc nhở" để xem hệ thống đã gửi mail cho ai, giờ nào, thành công hay thất bại. Nếu thất bại, Admin có thể kiểm tra lại cấu hình.
*   **Thùng rác:** Nằm ở menu bên trái. Admin có thể xem toàn bộ các văn bản đã bị nhân viên xóa (Soft delete). Có thể đọc lại thông tin nhưng không thể tác động thêm, dùng để đối soát khi có sự cố.

---

## 4. CƠ CHẾ HOẠT ĐỘNG CỦA CRON JOB (TỰ ĐỘNG HÓA)
Hệ thống không cần con người bấm nút để gửi mail. Nó hoạt động theo cơ chế **Cron Job** (Chạy ngầm tự động):
1. Mỗi ngày vào đúng **15h00 chiều (Giờ VN)**, hệ thống sẽ tự động thức dậy.
2. Nó quét toàn bộ kho văn bản, cập nhật lại trạng thái (từ Còn hiệu lực -> Sắp hết hạn -> Hết hạn).
3. Đem đối chiếu với các *Quy tắc nhắc nhở*. Nếu phát hiện văn bản nào rơi vào "điểm rơi" cần nhắc nhở, nó sẽ gửi 1 email duy nhất cho người phụ trách văn bản đó.
4. Tránh Spam: Nếu văn bản đã được gửi email thành công, hệ thống sẽ ghi nhớ và không gửi lại nữa (Cho đến khi chạm mốc quy tắc tiếp theo, ví dụ: Nhắc trước 30 ngày, sau đó Nhắc trước 7 ngày).

*(Nút "Chạy Nhắc nhở Ngay" trên giao diện chỉ dùng để Admin test hệ thống tức thời mà không cần chờ đến 15h chiều).*

---
**Chúc bạn thao tác thành công và trải nghiệm tốt với Hệ thống Nhắc hạn Văn bản!**
