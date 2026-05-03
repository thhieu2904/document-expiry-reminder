"""
Scheduler configuration and management.
"""
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.core.database import async_session
from app.models.system_setting import SystemSetting
from app.tasks.document_tasks import update_document_statuses
from app.services.reminder_engine import process_reminders

def convert_vn_to_utc(time_str: str) -> tuple[int, int]:
    """Convert a time string (HH:MM) in VN time (UTC+7) to UTC hour and minute."""
    try:
        parts = time_str.split(':')
        hour = int(parts[0])
        minute = int(parts[1])
        # Use timedelta to handle day wrapping
        dt = datetime(2000, 1, 1, hour, minute)
        dt_utc = dt - timedelta(hours=7)
        return dt_utc.hour, dt_utc.minute
    except Exception:
        # Default fallback
        return 1, 0 # 08:00 VN -> 01:00 UTC

async def load_settings_and_configure_scheduler(scheduler: AsyncIOScheduler):
    """
    Load cron settings from the database and configure the scheduler jobs.
    This can be called on startup or when settings are updated.
    """
    # Remove job 2 if it exists but will be disabled
    # (job 1 is always re-added with replace_existing=True)
            
    async with async_session() as db:
        res = await db.execute(select(SystemSetting))
        settings_list = res.scalars().all()
        settings_dict = {s.key: s.value for s in settings_list}
        
    cron_time_1 = settings_dict.get("cron_time_1", "08:00")
    cron_time_2 = settings_dict.get("cron_time_2", "14:00")
    cron_enabled_2 = settings_dict.get("cron_enabled_2", "true").lower() == "true"
    
    hour1, min1 = convert_vn_to_utc(cron_time_1)
    
    # Always schedule job 1
    scheduler.add_job(
        process_reminders, 
        'cron', 
        hour=hour1, 
        minute=min1, 
        id="reminder_job_1",
        replace_existing=True
    )
    print(f"Scheduled reminder_job_1 at {hour1:02d}:{min1:02d} UTC ({cron_time_1} VN)")
    
    if cron_enabled_2:
        hour2, min2 = convert_vn_to_utc(cron_time_2)
        scheduler.add_job(
            process_reminders, 
            'cron', 
            hour=hour2, 
            minute=min2, 
            id="reminder_job_2",
            replace_existing=True
        )
        print(f"Scheduled reminder_job_2 at {hour2:02d}:{min2:02d} UTC ({cron_time_2} VN)")
    else:
        # Remove job 2 if it was previously scheduled
        try:
            scheduler.remove_job("reminder_job_2")
            print("Removed reminder_job_2 (disabled by admin)")
        except Exception:
            pass  # Job didn't exist, that's fine
