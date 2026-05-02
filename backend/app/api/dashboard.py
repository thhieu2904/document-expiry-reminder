from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.document import Document
from app.models.reminder_log import ReminderLog

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(require_admin)])

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    # 1. Total Documents
    total_res = await db.execute(select(func.count(Document.id)))
    total_docs = total_res.scalar() or 0

    # 2. Status counts
    # Active
    active_res = await db.execute(select(func.count(Document.id)).where(Document.status == "active"))
    active_docs = active_res.scalar() or 0
    
    # Expiring Soon
    expiring_res = await db.execute(select(func.count(Document.id)).where(Document.status == "expiring_soon"))
    expiring_docs = expiring_res.scalar() or 0
    
    # Expired
    expired_res = await db.execute(select(func.count(Document.id)).where(Document.status == "expired"))
    expired_docs = expired_res.scalar() or 0

    # 3. Emails Sent (Successful vs Failed)
    success_email_res = await db.execute(select(func.count(ReminderLog.id)).where(ReminderLog.status == "sent"))
    success_emails = success_email_res.scalar() or 0
    
    failed_email_res = await db.execute(select(func.count(ReminderLog.id)).where(ReminderLog.status == "failed"))
    failed_emails = failed_email_res.scalar() or 0

    return {
        "documents": {
            "total": total_docs,
            "active": active_docs,
            "expiring_soon": expiring_docs,
            "expired": expired_docs
        },
        "emails": {
            "success": success_emails,
            "failed": failed_emails,
            "total": success_emails + failed_emails
        }
    }

@router.get("/expiring-soon")
async def get_expiring_soon(db: AsyncSession = Depends(get_db)):
    query = (
        select(Document)
        .where(Document.status == "expiring_soon")
        .order_by(Document.expiry_date.asc())
        .limit(5)
    )
    result = await db.execute(query)
    docs = result.scalars().all()
    
    from app.api.documents import inject_file_url
    return [inject_file_url(d) for d in docs]
