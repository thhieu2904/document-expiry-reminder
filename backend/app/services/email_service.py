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
        # Use port 465 with implicit SSL (use_tls=True) for cloud hosting compatibility.
        # Port 587 with STARTTLS is blocked by many cloud providers (Render, Railway, etc.)
        use_ssl = settings.smtp_port == 465
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            use_tls=use_ssl,
            start_tls=not use_ssl,
            timeout=30,
        )
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False

def generate_reminder_html(
    doc_title: str, 
    doc_number: str, 
    expiry_date: str, 
    rule_name: str,
    custom_body: str = None
) -> str:
    """Generates simple HTML for the reminder email, allowing custom body injection."""
    
    # Render body content
    if custom_body:
        # Convert simple line breaks to <br> for HTML rendering
        body_content = custom_body.replace('\n', '<br>')
    else:
        # Default content
        body_content = f"""
        <p>Hệ thống tự động thông báo về việc văn bản sắp/đã hết hạn (Theo quy định: <strong>{rule_name}</strong>).</p>
        <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #d9534f; margin-top: 15px; border-radius: 0 4px 4px 0;">
            <p style="margin: 0 0 8px 0;"><strong>Số/Ký hiệu:</strong> {doc_number}</p>
            <p style="margin: 0 0 8px 0;"><strong>Trích yếu:</strong> {doc_title}</p>
            <p style="margin: 0;"><strong>Ngày hết hạn:</strong> <span style="color: #dc2626; font-weight: bold;">{expiry_date}</span></p>
        </div>
        <p style="margin-top: 20px;">Vui lòng kiểm tra và xử lý kịp thời.</p>
        """

    return f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #334155; background-color: #f1f5f9; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                
                {body_content}
                
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin-top: 30px; margin-bottom: 20px;" />
                <p style="font-size: 12px; color: #94a3b8; margin: 0; text-align: center;">
                    Đây là email tự động từ Hệ thống Nhắc hạn Văn bản, vui lòng không trả lời.
                </p>
            </div>
        </body>
    </html>
    """
