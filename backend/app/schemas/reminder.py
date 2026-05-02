from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from typing import Optional

class ReminderRuleBase(BaseModel):
    name: str
    days_before: int
    is_overdue_rule: bool = False
    channel: str = "email"
    is_active: bool = True

class ReminderRuleCreate(ReminderRuleBase):
    pass

class ReminderRuleUpdate(BaseModel):
    name: Optional[str] = None
    days_before: Optional[int] = None
    is_overdue_rule: Optional[bool] = None
    is_active: Optional[bool] = None

class ReminderRuleResponse(ReminderRuleBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReminderLogResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    rule_id: uuid.UUID
    recipient_email: str
    subject: Optional[str] = None
    status: str
    sent_at: Optional[datetime] = None
    created_at: datetime
    
    # We might want to inject document title or rule name later
    document_title: Optional[str] = None
    rule_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
