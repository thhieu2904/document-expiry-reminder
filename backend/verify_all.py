"""
Full Backend API Verification Script for Document Expiry Reminder MVP.
Tests all critical endpoints across Phase 1-4.
"""
import asyncio
import httpx

BASE = "http://localhost:8000"
TOKEN = None

async def login():
    global TOKEN
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BASE}/api/auth/login", json={"email": "thhieu2904@gmail.com", "password": "password123"})
        if r.status_code == 200:
            TOKEN = r.json().get("access_token")
            print(f"✅ POST /api/auth/login          -> 200 (Token received)")
            return True
        else:
            print(f"❌ POST /api/auth/login          -> {r.status_code}: {r.text}")
            return False

def headers():
    return {"Authorization": f"Bearer {TOKEN}"}

async def test_endpoint(method, path, expected_status=200, json_body=None):
    async with httpx.AsyncClient(timeout=60.0) as c:
        if method == "GET":
            r = await c.get(f"{BASE}{path}", headers=headers())
        elif method == "POST":
            r = await c.post(f"{BASE}{path}", headers=headers(), json=json_body)
        elif method == "PUT":
            r = await c.put(f"{BASE}{path}", headers=headers(), json=json_body)
        elif method == "DELETE":
            r = await c.delete(f"{BASE}{path}", headers=headers())
        
        status_icon = "✅" if r.status_code == expected_status else "❌"
        
        # Get response summary
        try:
            data = r.json()
            if isinstance(data, list):
                summary = f"[{len(data)} items]"
            elif isinstance(data, dict):
                summary = str(data)[:120]
            else:
                summary = str(data)[:120]
        except Exception:
            summary = r.text[:120]
        
        print(f"{status_icon} {method:6} {path:40} -> {r.status_code} {summary}")
        return r.status_code == expected_status, r

async def main():
    print("=" * 80)
    print("  DOCUMENT EXPIRY REMINDER - FULL API VERIFICATION")
    print("=" * 80)
    
    results = []
    
    # Phase 1: Auth
    print("\n--- Phase 1: Authentication ---")
    if not await login():
        print("Login failed. Cannot continue.")
        return
    results.append(True)
    
    ok, r = await test_endpoint("GET", "/api/auth/me")
    results.append(ok)
    
    # Phase 1: Departments
    print("\n--- Phase 1: Departments CRUD ---")
    ok, r = await test_endpoint("GET", "/api/departments")
    results.append(ok)
    
    # Phase 1: Users
    print("\n--- Phase 1: Users CRUD ---")
    ok, r = await test_endpoint("GET", "/api/users")
    results.append(ok)
    
    # Phase 2: Documents
    print("\n--- Phase 2: Documents CRUD ---")
    ok, r = await test_endpoint("GET", "/api/documents")
    results.append(ok)
    if ok:
        docs = r.json()
        if len(docs) > 0:
            doc_id = docs[0]["id"]
            ok2, _ = await test_endpoint("GET", f"/api/documents/{doc_id}")
            results.append(ok2)
    
    # Phase 3: Reminder Rules
    print("\n--- Phase 3: Reminder Rules ---")
    ok, r = await test_endpoint("GET", "/api/reminders/rules")
    results.append(ok)
    if ok:
        rules = r.json()
        if len(rules) > 0:
            rule_id = rules[0]["id"]
            ok2, _ = await test_endpoint("PUT", f"/api/reminders/rules/{rule_id}", json_body={"is_active": True})
            results.append(ok2)
    
    # Phase 3: Reminder Logs
    print("\n--- Phase 3: Reminder Logs ---")
    ok, r = await test_endpoint("GET", "/api/reminders/logs")
    results.append(ok)
    
    # Phase 3: Manual Trigger
    print("\n--- Phase 3: Manual Trigger ---")
    ok, r = await test_endpoint("POST", "/api/reminders/trigger")
    results.append(ok)
    
    # Phase 4: Dashboard
    print("\n--- Phase 4: Dashboard ---")
    ok, r = await test_endpoint("GET", "/api/dashboard/summary")
    results.append(ok)
    
    # Summary
    passed = sum(results)
    total = len(results)
    print("\n" + "=" * 80)
    print(f"  RESULTS: {passed}/{total} passed")
    if passed == total:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print(f"  ⚠️  {total - passed} test(s) FAILED")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
