"""
Document Expiry Reminder - FastAPI Application Entry Point.

A lightweight internal system for tracking document validity and expiry dates,
then sending automated email reminders to responsible users.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, users, departments, documents, reminders, dashboard, settings as settings_api


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.document_tasks import update_document_statuses
from app.services.reminder_engine import process_reminders
from app.core.scheduler import load_settings_and_configure_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    print(f"🚀 {settings.app_name} starting in {settings.app_env} mode...")
    
    # Init scheduler
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler
    
    # Static job: Update document statuses at midnight and noon UTC (7:00 AM & 7:00 PM VN)
    scheduler.add_job(update_document_statuses, 'cron', hour='0,12', minute=0, id="doc_status_job")
    
    # Dynamic jobs: Load from database
    await load_settings_and_configure_scheduler(scheduler)
    
    scheduler.start()
    
    # Run once on startup to catch up
    import asyncio
    async def startup_jobs():
        await update_document_statuses()
        await process_reminders()
    
    asyncio.create_task(startup_jobs())
    
    yield
    
    print(f"👋 {settings.app_name} shutting down...")
    scheduler.shutdown()


app = FastAPI(
    title=settings.app_name,
    description="Internal system for tracking document expiry dates and sending automated email reminders.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(departments.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["settings"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
