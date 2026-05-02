import asyncio
from sqlalchemy import select
from app.core.database import async_session
from app.models.reminder_rule import ReminderRule

DEFAULT_RULES = [
    {"name": "Nhắc trước 30 ngày", "days_before": 30, "is_overdue_rule": False},
    {"name": "Nhắc trước 15 ngày", "days_before": 15, "is_overdue_rule": False},
    {"name": "Nhắc trước 7 ngày", "days_before": 7, "is_overdue_rule": False},
    {"name": "Nhắc trước 1 ngày", "days_before": 1, "is_overdue_rule": False},
    {"name": "Cảnh báo quá hạn", "days_before": 0, "is_overdue_rule": True},
]

async def seed():
    async with async_session() as db:
        res = await db.execute(select(ReminderRule))
        existing_rules = res.scalars().all()
        
        if existing_rules:
            print("Rules already seeded.")
            return

        for rule_data in DEFAULT_RULES:
            rule = ReminderRule(**rule_data)
            db.add(rule)
        
        await db.commit()
        print("Successfully seeded default reminder rules.")

if __name__ == "__main__":
    asyncio.run(seed())
