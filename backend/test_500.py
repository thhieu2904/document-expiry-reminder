import asyncio
import httpx

async def test_api():
    async with httpx.AsyncClient() as client:
        # Login
        print("Logging in...")
        res = await client.post("http://localhost:8000/api/auth/login", json={"email": "thhieu2904@gmail.com", "password": "password123"})
        if res.status_code != 200:
            print("Login failed:", res.status_code, res.text)
            return
            
        token = res.json()["access_token"]
        print("Got token. Fetching /auth/me...")
        
        # Get me
        res2 = await client.get("http://localhost:8000/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        print("Response:", res2.status_code)
        print("Body:", res2.text)

if __name__ == "__main__":
    asyncio.run(test_api())
