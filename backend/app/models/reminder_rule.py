import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class ReminderRule(Base):
    __tablename__ = "reminder_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    days_before: Mapped[int] = mapped_column(Integer, nullable=False)
    is_overdue_rule: Mapped[bool] = mapped_column(Boolean, default=False)
    channel: Mapped[str] = mapped_column(String(20), default="email")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Custom email templates
    subject_template: Mapped[str] = mapped_column(String(255), nullable=True)
    body_template: Mapped[str] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<ReminderRule {self.name} (Days: {self.days_before}, Active: {self.is_active})>"
