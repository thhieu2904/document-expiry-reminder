import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, and_
from app.core.database import async_session
from app.models.document import Document
from app.models.reminder_rule import ReminderRule
from app.models.reminder_log import ReminderLog
from app.models.user import User
from app.services.email_service import send_reminder_email, generate_reminder_html

async def process_reminders():
    """
    Core engine to evaluate reminder rules against documents and send emails.
    """
    print(f"[{datetime.now(timezone.utc)}] Running reminder engine...")
    today = datetime.now(timezone.utc).date()

    async with async_session() as db:
        # Fetch active rules
        rules_res = await db.execute(select(ReminderRule).where(ReminderRule.is_active == True))
        active_rules = rules_res.scalars().all()
        
        if not active_rules:
            print("No active reminder rules found.")
            return

        # Fetch active and expiring_soon documents
        docs_res = await db.execute(select(Document).where(Document.status.in_(["active", "expiring_soon", "expired"])))
        documents = docs_res.scalars().all()

        for doc in documents:
            if not doc.expiry_date:
                continue

            # Load the owner
            owner_res = await db.execute(select(User).where(User.id == doc.owner_id))
            owner = owner_res.scalar_one_or_none()
            if not owner or not owner.email:
                continue

            for rule in active_rules:
                should_send = False

                if rule.is_overdue_rule:
                    # Overdue condition: today > expiry_date
                    if today > doc.expiry_date:
                        should_send = True
                else:
                    # Before expiry condition: today >= (expiry_date - days_before) and today <= expiry_date
                    # We check if today has reached the milestone
                    target_date = doc.expiry_date - timedelta(days=rule.days_before)
                    if today >= target_date and today <= doc.expiry_date:
                        should_send = True

                if should_send:
                    # Check if we already logged this rule for this document and user
                    log_res = await db.execute(
                        select(ReminderLog).where(
                            and_(
                                ReminderLog.document_id == doc.id,
                                ReminderLog.rule_id == rule.id,
                                ReminderLog.recipient_user_id == owner.id
                            )
                        )
                    )
                    existing_log = log_res.scalar_one_or_none()

                    if not existing_log:
                        # Send email
                        subject = f"[{rule.name}] {doc.document_number or ''} - {doc.title}"
                        html = generate_reminder_html(
                            doc_title=doc.title,
                            doc_number=doc.document_number or "Không có",
                            expiry_date=doc.expiry_date.strftime("%d/%m/%Y"),
                            rule_name=rule.name
                        )
                        
                        success = await send_reminder_email(owner.email, subject, html)
                        
                        # Create log
                        log = ReminderLog(
                            document_id=doc.id,
                            rule_id=rule.id,
                            recipient_user_id=owner.id,
                            recipient_email=owner.email,
                            subject=subject,
                            message=html, # or simple text
                            status="sent" if success else "failed",
                            scheduled_at=datetime.now(timezone.utc),
                            sent_at=datetime.now(timezone.utc) if success else None
                        )
                        db.add(log)
                        
                        # Commit immediately to avoid duplicates in case of crash
                        await db.commit()
                        print(f"[{'SUCCESS' if success else 'FAIL'}] Reminder sent to {owner.email} for document {doc.id}")

    print(f"[{datetime.now(timezone.utc)}] Reminder engine finished.")
