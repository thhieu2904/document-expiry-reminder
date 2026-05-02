import asyncio
import httpx
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.core.deps import get_current_user
from app.core.database import async_session

async def debug_auth():
    async with httpx.AsyncClient() as client:
        res = await client.post("http://localhost:8000/api/auth/login", json={"email": "thhieu2904@gmail.com", "password": "password123"})
        token = res.json()["access_token"]
        
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    async with async_session() as db:
        try:
            user = await get_current_user(creds, db)
            print("User:", user)
        except HTTPException as e:
            print("HTTP Exception:", e.status_code, e.detail)
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_auth())
