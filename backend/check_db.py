"""
Verify database integrity: check all tables exist and have correct structure.
"""
import asyncio
from sqlalchemy import text
from app.core.database import async_session

EXPECTED_TABLES = [
    "users",
    "departments", 
    "documents",
    "reminder_rules",
    "reminder_logs",
    "system_settings",
]

async def main():
    print("=" * 60)
    print("DATABASE INTEGRITY CHECK")
    print("=" * 60)
    
    async with async_session() as db:
        # 1. Check all tables exist
        res = await db.execute(text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public' ORDER BY table_name"
        ))
        existing_tables = [row[0] for row in res.fetchall()]
        
        print("\n📋 Tables in database:")
        for t in existing_tables:
            marker = "✅" if t in EXPECTED_TABLES else "ℹ️ "
            print(f"  {marker} {t}")
        
        missing = [t for t in EXPECTED_TABLES if t not in existing_tables]
        if missing:
            print(f"\n❌ MISSING TABLES: {missing}")
        else:
            print(f"\n✅ All {len(EXPECTED_TABLES)} expected tables present")
        
        # 2. Check row counts
        print("\n📊 Row counts:")
        for table in EXPECTED_TABLES:
            if table in existing_tables:
                res = await db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = res.scalar()
                print(f"  {table}: {count} rows")
        
        # 3. Check system_settings data
        print("\n⚙️  System Settings:")
        res = await db.execute(text("SELECT key, value FROM system_settings ORDER BY key"))
        rows = res.fetchall()
        if rows:
            for row in rows:
                print(f"  {row[0]} = {row[1]}")
        else:
            print("  (empty - defaults will be used)")
        
        # 4. Check reminder_rules
        print("\n📌 Reminder Rules:")
        res = await db.execute(text(
            "SELECT name, days_before, is_active, is_overdue_rule FROM reminder_rules ORDER BY days_before DESC"
        ))
        for row in res.fetchall():
            status = "🟢 ON" if row[2] else "🔴 OFF"
            kind = "(Quá hạn)" if row[3] else f"({row[1]} ngày)"
            print(f"  {status} {row[0]} {kind}")
        
        # 5. Check users with admin role
        print("\n👤 Admin Users:")
        res = await db.execute(text(
            "SELECT email, full_name, role, can_login FROM users WHERE role = 'admin'"
        ))
        admins = res.fetchall()
        if admins:
            for a in admins:
                login = "✅ can login" if a[3] else "❌ cannot login"
                print(f"  {a[0]} ({a[1]}) - {login}")
        else:
            print("  ⚠️  NO ADMIN USERS FOUND!")
        
        # 6. Verify FK integrity (documents -> users, documents -> departments)
        print("\n🔗 FK Integrity Check:")
        res = await db.execute(text(
            "SELECT COUNT(*) FROM documents d "
            "LEFT JOIN users u ON d.owner_id = u.id "
            "WHERE u.id IS NULL"
        ))
        orphan_docs = res.scalar()
        print(f"  Documents with missing owner: {orphan_docs} {'✅' if orphan_docs == 0 else '❌'}")
        
        res = await db.execute(text(
            "SELECT COUNT(*) FROM reminder_logs rl "
            "LEFT JOIN documents d ON rl.document_id = d.id "
            "WHERE d.id IS NULL"
        ))
        orphan_logs = res.scalar()
        print(f"  Reminder logs with missing document: {orphan_logs} {'✅' if orphan_logs == 0 else '❌'}")

    print("\n" + "=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
