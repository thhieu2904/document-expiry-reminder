"""
Quick test script to verify Gmail SMTP configuration.
Sends a test email to yourself.
"""
import asyncio
from app.core.config import settings
from app.services.email_service import send_reminder_email, generate_reminder_html

async def main():
    print(f"SMTP Host: {settings.smtp_host}")
    print(f"SMTP Port: {settings.smtp_port}")
    print(f"SMTP User: {settings.smtp_user}")
    print(f"From: {settings.smtp_from_name} <{settings.smtp_from_email}>")
    print(f"Sending to: {settings.smtp_user}")
    print("---")

    html = generate_reminder_html(
        doc_title="Giấy phép xây dựng số 123/GP",
        doc_number="GP-2025-001",
        expiry_date="15/06/2025",
        rule_name="Nhắc trước 7 ngày"
    )

    success = await send_reminder_email(
        recipient_email=settings.smtp_user,  # Send to yourself
        subject="[TEST] Hệ thống Nhắc hạn Văn bản - Kiểm tra Gmail SMTP",
        html_content=html
    )

    if success:
        print("✅ Email sent successfully! Check your Gmail inbox.")
    else:
        print("❌ Failed to send email. Check the error above.")

if __name__ == "__main__":
    asyncio.run(main())
