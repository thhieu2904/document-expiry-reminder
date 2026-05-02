import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.reminder_rule import ReminderRule
from app.models.reminder_log import ReminderLog
from app.models.document import Document
from app.schemas.reminder import (
    ReminderRuleCreate,
    ReminderRuleUpdate,
    ReminderRuleResponse,
    ReminderLogResponse
)
from app.services.reminder_engine import process_reminders

router = APIRouter(dependencies=[Depends(require_admin)])

# --- Rules ---

@router.get("/rules", response_model=List[ReminderRuleResponse])
async def list_rules(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ReminderRule).order_by(ReminderRule.days_before.desc()))
    return res.scalars().all()

@router.post("/rules", response_model=ReminderRuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(data: ReminderRuleCreate, db: AsyncSession = Depends(get_db)):
    rule = ReminderRule(**data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.put("/rules/{rule_id}", response_model=ReminderRuleResponse)
async def update_rule(rule_id: uuid.UUID, data: ReminderRuleUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ReminderRule).where(ReminderRule.id == rule_id))
    rule = res.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(rule, k, v)
        
    await db.commit()
    await db.refresh(rule)
    return rule

@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(rule_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ReminderRule).where(ReminderRule.id == rule_id))
    rule = res.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    await db.delete(rule)
    await db.commit()

# --- Logs ---

@router.get("/logs", response_model=List[ReminderLogResponse])
async def list_logs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Join with document and rule to get titles (optional enhancement)
    # For now, just return logs and we can fetch relations if needed.
    res = await db.execute(
        select(ReminderLog)
        .order_by(ReminderLog.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    logs = res.scalars().all()
    
    # We will manually inject document title and rule name for the frontend
    response_logs = []
    for log in logs:
        # Avoid N+1 in production by using joinedload, but this is fine for MVP small data
        doc_res = await db.execute(select(Document.title).where(Document.id == log.document_id))
        doc_title = doc_res.scalar_one_or_none()
        
        rule_res = await db.execute(select(ReminderRule.name).where(ReminderRule.id == log.rule_id))
        rule_name = rule_res.scalar_one_or_none()
        
        log_dict = {
            "id": log.id,
            "document_id": log.document_id,
            "rule_id": log.rule_id,
            "recipient_email": log.recipient_email,
            "subject": log.subject,
            "status": log.status,
            "sent_at": log.sent_at,
            "created_at": log.created_at,
            "document_title": doc_title,
            "rule_name": rule_name
        }
        response_logs.append(ReminderLogResponse(**log_dict))
        
    return response_logs

# --- Manual Trigger ---

@router.post("/trigger")
async def trigger_reminders(db: AsyncSession = Depends(get_db)):
    """Manually trigger the reminder engine (Admin only)."""
    # Run it in the background or await it directly
    # Since it might take time, best to await it for immediate feedback in MVP
    await process_reminders()
    return {"message": "Reminder engine triggered successfully"}
