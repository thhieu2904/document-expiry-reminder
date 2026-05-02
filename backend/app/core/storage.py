import asyncio
from typing import Optional
from app.core.security import supabase_admin
from app.core.config import settings

def upload_file_sync(file_bytes: bytes, file_path: str, content_type: str) -> str:
    """Uploads file to Supabase Storage (Synchronous)"""
    bucket = settings.supabase_storage_bucket
    
    res = supabase_admin.storage.from_(bucket).upload(
        path=file_path,
        file=file_bytes,
        file_options={"content-type": content_type, "upsert": "true"}
    )
    return file_path

async def upload_file_async(file_bytes: bytes, file_path: str, content_type: str) -> str:
    """Wrapper to run synchronous upload in a threadpool"""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, upload_file_sync, file_bytes, file_path, content_type)

def get_file_url(file_path: str) -> str:
    """Gets public URL for a file"""
    bucket = settings.supabase_storage_bucket
    return supabase_admin.storage.from_(bucket).get_public_url(file_path)

def delete_file_sync(file_path: str):
    """Deletes file from Supabase Storage"""
    bucket = settings.supabase_storage_bucket
    supabase_admin.storage.from_(bucket).remove([file_path])

async def delete_file_async(file_path: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, delete_file_sync, file_path)
