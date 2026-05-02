import asyncio
import httpx

async def debug_422():
    async with httpx.AsyncClient() as client:
        res = await client.post("http://localhost:8000/api/auth/login", json={"email": "thhieu2904@gmail.com", "password": "password123"})
        token = res.json().get("access_token")
        
        if not token:
            print("Login failed")
            return
            
        res2 = await client.get("http://localhost:8000/api/documents", headers={"Authorization": f"Bearer {token}"})
        print(f"Status: {res2.status_code}")
        print(f"Body: {res2.text}")

if __name__ == "__main__":
    asyncio.run(debug_422())
