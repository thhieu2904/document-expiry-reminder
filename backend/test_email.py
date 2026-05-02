import asyncio
from app.services.email_service import send_reminder_email
from app.core.config import settings

async def test_email():
    print(f"SMTP Host: {settings.smtp_host}")
    print(f"SMTP Port: {settings.smtp_port}")
    print(f"SMTP User: {settings.smtp_user}")
    print(f"SMTP Pass length: {len(settings.smtp_password) if settings.smtp_password else 0}")
    
    success = await send_reminder_email(
        "test@example.com",
        "Test Mailtrap",
        "<h1>Hello from TVU test</h1>"
    )
    print(f"Success: {success}")

if __name__ == "__main__":
    asyncio.run(test_email())
