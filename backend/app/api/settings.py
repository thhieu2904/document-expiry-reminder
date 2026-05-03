from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.system_setting import SystemSetting
from app.core.scheduler import load_settings_and_configure_scheduler

router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("/cron")
async def get_cron_settings(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(SystemSetting))
    settings_list = res.scalars().all()
    settings_dict = {s.key: s.value for s in settings_list}
    
    # Return defaults if not set in DB
    return {
        "cron_time_1": settings_dict.get("cron_time_1", "08:00"),
        "cron_time_2": settings_dict.get("cron_time_2", "14:00"),
        "cron_enabled_2": settings_dict.get("cron_enabled_2", "true").lower() == "true"
    }

@router.put("/cron")
async def update_cron_settings(request: Request, payload: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    """
    Update cron settings and reload the scheduler dynamically.
    Payload should be:
    {
        "cron_time_1": "08:00",
        "cron_time_2": "14:00",
        "cron_enabled_2": true/false
    }
    """
    updates = {
        "cron_time_1": str(payload.get("cron_time_1", "08:00")),
        "cron_time_2": str(payload.get("cron_time_2", "14:00")),
        "cron_enabled_2": str(payload.get("cron_enabled_2", True)).lower()
    }
    
    for key, value in updates.items():
        res = await db.execute(select(SystemSetting).where(SystemSetting.key == key))
        setting = res.scalar_one_or_none()
        
        if setting:
            setting.value = value
        else:
            new_setting = SystemSetting(key=key, value=value)
            db.add(new_setting)
            
    await db.flush()
    
    # Reload the scheduler
    if hasattr(request.app.state, "scheduler"):
        await load_settings_and_configure_scheduler(request.app.state.scheduler)
        
    return {"message": "Cập nhật cấu hình tự động thành công", "settings": updates}
