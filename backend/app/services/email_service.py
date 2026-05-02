import aiosmtplib
from email.message import EmailMessage
from app.core.config import settings

async def send_reminder_email(
    recipient_email: str, 
    subject: str, 
    html_content: str
) -> bool:
    """
    Sends an email using the configured SMTP server (Mailtrap).
    Returns True if successful, False otherwise.
    """
    if not settings.smtp_host or not settings.smtp_user:
        print("SMTP is not configured. Skipping email send.")
        return False

    message = EmailMessage()
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content("Vui lòng bật chế độ xem HTML để đọc email này.")
    message.add_alternative(html_content, subtype='html')

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            start_tls=False, # Mailtrap doesn't strictly require TLS on 2525, but we can set it if needed.
        )
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False

def generate_reminder_html(doc_title: str, doc_number: str, expiry_date: str, rule_name: str) -> str:
    """Generates simple HTML for the reminder email."""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #d9534f;">Cảnh báo hết hạn văn bản</h2>
                <p>Xin chào,</p>
                <p>Hệ thống tự động thông báo về việc văn bản sắp/đã hết hạn (Theo quy định: <strong>{rule_name}</strong>).</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #d9534f; margin-top: 15px;">
                    <p><strong>Số/Ký hiệu:</strong> {doc_number}</p>
                    <p><strong>Trích yếu:</strong> {doc_title}</p>
                    <p><strong>Ngày hết hạn:</strong> {expiry_date}</p>
                </div>
                
                <p style="margin-top: 20px;">Vui lòng kiểm tra và xử lý kịp thời.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin-top: 30px;" />
                <p style="font-size: 12px; color: #999;">Đây là email tự động từ Hệ thống Quản lý Văn bản TVU, vui lòng không trả lời.</p>
            </div>
        </body>
    </html>
    """
