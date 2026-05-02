import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.core.database import async_session
from app.models.document import Document

async def update_document_statuses():
    """
    Background job to update document statuses based on their expiry date.
    Rules:
    - active -> expiring_soon if expiry_date <= today + 30 days
    - active/expiring_soon -> expired if expiry_date < today
    """
    print(f"[{datetime.now(timezone.utc)}] Running document status update job...")
    
    today = datetime.now(timezone.utc).date()
    thirty_days_later = today + timedelta(days=30)
    
    async with async_session() as db:
        # Find active documents that should be expiring_soon
        query_soon = select(Document).where(
            Document.status == "active",
            Document.expiry_date <= thirty_days_later,
            Document.expiry_date >= today
        )
        res_soon = await db.execute(query_soon)
        docs_soon = res_soon.scalars().all()
        for doc in docs_soon:
            doc.status = "expiring_soon"
            
        # Find active or expiring_soon documents that are expired
        query_expired = select(Document).where(
            Document.status.in_(["active", "expiring_soon"]),
            Document.expiry_date < today
        )
        res_expired = await db.execute(query_expired)
        docs_expired = res_expired.scalars().all()
        for doc in docs_expired:
            doc.status = "expired"
            
        if docs_soon or docs_expired:
            await db.commit()
            print(f"Updated {len(docs_soon)} to expiring_soon, {len(docs_expired)} to expired.")
        else:
            print("No documents needed status update.")
