"""Fix: Set Supabase Storage bucket to public"""
import sys
sys.path.insert(0, ".")

from app.core.config import settings
from app.core.security import supabase_admin

bucket = settings.supabase_storage_bucket

try:
    supabase_admin.storage.update_bucket(bucket, options={"public": True})
    print(f"Bucket '{bucket}' is now PUBLIC!")
    
    # Verify
    info = supabase_admin.storage.get_bucket(bucket)
    print(f"  Verified: public={info.public}")
except Exception as e:
    print(f"Error: {e}")
