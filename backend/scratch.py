import asyncio
from app.core.database import async_session
from app.models.reminder_log import ReminderLog
from sqlalchemy import select, delete

async def run():
    async with async_session() as db:
        res = await db.execute(select(ReminderLog.status))
        logs = res.scalars().all()
        print('LOGS IN DB:', logs)
        
        # Now delete ALL logs so it can trigger fresh for everything
        await db.execute(delete(ReminderLog))
        await db.commit()
        print('DELETED ALL LOGS')

if __name__ == '__main__':
    asyncio.run(run())
