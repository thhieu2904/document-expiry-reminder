"""Check all documents in DB and their file status"""
import asyncio
import sys
sys.path.insert(0, ".")

from sqlalchemy import select
from app.core.database import async_session
from app.models.document import Document

async def check():
    async with async_session() as db:
        result = await db.execute(select(Document))
        docs = result.scalars().all()
        
        print(f"Total documents: {len(docs)}\n")
        for doc in docs:
            print(f"  [{doc.id}] {doc.title}")
            print(f"    file_path: {doc.file_path}")
            print(f"    file_name: {doc.file_name}")
            print(f"    file_size: {doc.file_size}")
            print()

asyncio.run(check())
