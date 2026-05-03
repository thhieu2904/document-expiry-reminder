import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, and_
from app.core.database import async_session
from app.models.document import Document
from app.models.reminder_rule import ReminderRule
from app.models.reminder_log import ReminderLog
from app.models.user import User
from app.models.department import Department
from app.services.email_service import send_reminder_email, generate_reminder_html

def parse_template(template: str, doc: Document, owner: User, dept: Department, rule: ReminderRule, today) -> str:
    if not template:
        return ""
    
    doc_number = doc.document_number or "Không có"
    dept_name = dept.name if dept else "Không có"
    days_left = (doc.expiry_date - today).days if doc.expiry_date else 0
    owner_name = owner.full_name or owner.email
    
    text = template.replace("{{document_title}}", doc.title)
    text = text.replace("{{document_number}}", doc_number)
    text = text.replace("{{department_name}}", dept_name)
    text = text.replace("{{expiry_date}}", doc.expiry_date.strftime("%d/%m/%Y") if doc.expiry_date else "Không có")
    text = text.replace("{{rule_name}}", rule.name)
    text = text.replace("{{days_left}}", str(days_left))
    text = text.replace("{{owner_name}}", owner_name)
    
    return text

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

            # Load the owner and department
            owner_res = await db.execute(select(User).where(User.id == doc.owner_id))
            owner = owner_res.scalar_one_or_none()
            if not owner or not owner.email:
                continue
                
            dept = None
            if owner.department_id:
                dept_res = await db.execute(select(Department).where(Department.id == owner.department_id))
                dept = dept_res.scalar_one_or_none()

            for rule in active_rules:
                should_send = False

                if rule.is_overdue_rule:
                    # Overdue condition: today > expiry_date
                    if today > doc.expiry_date:
                        should_send = True
                else:
                    # Before expiry condition: today >= (expiry_date - days_before) and today <= expiry_date
                    target_date = doc.expiry_date - timedelta(days=rule.days_before)
                    if target_date <= today <= doc.expiry_date:
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
                        # Parse templates if available
                        if rule.subject_template:
                            subject = parse_template(rule.subject_template, doc, owner, dept, rule, today)
                        else:
                            subject = f"[{rule.name}] {doc.document_number or ''} - {doc.title}"
                            
                        custom_body = None
                        if rule.body_template:
                            custom_body = parse_template(rule.body_template, doc, owner, dept, rule, today)

                        # Generate HTML
                        html = generate_reminder_html(
                            doc_title=doc.title,
                            doc_number=doc.document_number or "Không có",
                            expiry_date=doc.expiry_date.strftime("%d/%m/%Y"),
                            rule_name=rule.name,
                            custom_body=custom_body
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
