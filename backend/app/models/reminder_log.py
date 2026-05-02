import uuid
from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

class ReminderLog(Base):
    __tablename__ = "reminder_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reminder_rules.id"), nullable=False
    )
    recipient_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, sent, failed
    provider_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Prevent sending the same rule to the same user for the same document
    __table_args__ = (
        UniqueConstraint("document_id", "rule_id", "recipient_user_id", name="uq_reminder_log_doc_rule_user"),
    )

    # Relationships
    document = relationship("Document")
    rule = relationship("ReminderRule")
    recipient = relationship("User")

    def __repr__(self) -> str:
        return f"<ReminderLog (Doc: {self.document_id}, Rule: {self.rule_id}, Status: {self.status})>"
