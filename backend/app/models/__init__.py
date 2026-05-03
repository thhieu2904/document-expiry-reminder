"""
Models package - import all models for Alembic auto-detection.
"""
from app.models.user import User
from app.models.department import Department
from app.models.document import Document
from app.models.reminder_rule import ReminderRule
from app.models.reminder_log import ReminderLog
from app.models.system_setting import SystemSetting

__all__ = ["User", "Department", "Document", "ReminderRule", "ReminderLog", "SystemSetting"]
