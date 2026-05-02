import asyncio
from sqlalchemy import delete
from app.core.database import async_session
from app.models.reminder_log import ReminderLog

async def clear_logs():
    async with async_session() as db:
        await db.execute(delete(ReminderLog))
        await db.commit()
        print('Logs cleared')

if __name__ == '__main__':
    asyncio.run(clear_logs())
