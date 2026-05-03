"""Quick test to check Supabase Storage bucket and upload"""
import sys
sys.path.insert(0, ".")

from app.core.config import settings
from app.core.security import supabase_admin

bucket = settings.supabase_storage_bucket
print(f"Bucket name: {bucket}")

# 1. List all buckets
try:
    buckets = supabase_admin.storage.list_buckets()
    print(f"\n--- All buckets ---")
    for b in buckets:
        print(f"  - {b.name} (public={b.public})")
except Exception as e:
    print(f"Error listing buckets: {e}")

# 2. Check if our bucket exists
try:
    bucket_info = supabase_admin.storage.get_bucket(bucket)
    print(f"\n--- Bucket '{bucket}' ---")
    print(f"  Name: {bucket_info.name}")
    print(f"  Public: {bucket_info.public}")
except Exception as e:
    print(f"\nBucket '{bucket}' NOT FOUND: {e}")
    print("Attempting to create bucket...")
    try:
        supabase_admin.storage.create_bucket(bucket, options={"public": True})
        print(f"  Created bucket '{bucket}' successfully!")
    except Exception as e2:
        print(f"  Failed to create bucket: {e2}")

# 3. Try upload a test file
try:
    test_content = b"Hello, this is a test file"
    res = supabase_admin.storage.from_(bucket).upload(
        path="test/test.txt",
        file=test_content,
        file_options={"content-type": "text/plain", "upsert": "true"}
    )
    print(f"\n--- Upload test ---")
    print(f"  Result: {res}")
    
    url = supabase_admin.storage.from_(bucket).get_public_url("test/test.txt")
    print(f"  Public URL: {url}")
except Exception as e:
    print(f"\nUpload FAILED: {e}")

# 4. List files in bucket
try:
    files = supabase_admin.storage.from_(bucket).list()
    print(f"\n--- Files in '{bucket}' ---")
    for f in files:
        print(f"  - {f.get('name', f)}")
except Exception as e:
    print(f"Error listing files: {e}")
