import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.core.database import async_session
from app.models.department import Department
from app.models.user import User
from app.models.document import Document

async def seed():
    async with async_session() as db:
        # Check if already seeded
        res = await db.execute(select(Department).where(Department.name == "Phòng Đào tạo"))
        if res.scalar_one_or_none():
            print("Seed data already exists.")
            return

        print("Seeding sample data...")
        
        # 1. Create Departments
        d1 = Department(id=uuid.uuid4(), name="Phòng Đào tạo", code="PDT")
        d2 = Department(id=uuid.uuid4(), name="Phòng Hành chính - Tổng hợp", code="PHC")
        db.add_all([d1, d2])
        await db.commit()

        # 2. Create Users (Receivers)
        u1 = User(
            id=uuid.uuid4(), 
            full_name="Nguyễn Văn A", 
            email="nguyenvana@tvu.edu.vn", 
            department_id=d1.id,
            can_login=False,
            status="active"
        )
        u2 = User(
            id=uuid.uuid4(), 
            full_name="Trần Thị B", 
            email="tranthib@tvu.edu.vn", 
            department_id=d2.id,
            can_login=False,
            status="active"
        )
        db.add_all([u1, u2])
        await db.commit()

        # 3. Create Documents
        today = datetime.now(timezone.utc).date()
        
        doc1 = Document(
            id=uuid.uuid4(),
            title="Quy chế đào tạo Đại học",
            document_number="123/QC-TVU",
            owner_id=u1.id,
            department_id=d1.id,
            expiry_date=today + timedelta(days=30), # Hits the 30-day rule
            status="active"
        )
        
        doc2 = Document(
            id=uuid.uuid4(),
            title="Kế hoạch tuyển sinh 2026",
            document_number="456/KH-TVU",
            owner_id=u1.id,
            department_id=d1.id,
            expiry_date=today + timedelta(days=15), # Hits the 15-day rule
            status="active"
        )
        
        doc3 = Document(
            id=uuid.uuid4(),
            title="Hợp đồng dịch vụ bảo vệ",
            document_number="789/HĐ-TVU",
            owner_id=u2.id,
            department_id=d2.id,
            expiry_date=today - timedelta(days=2), # Overdue
            status="expired"
        )
        
        doc4 = Document(
            id=uuid.uuid4(),
            title="Quyết định khen thưởng",
            document_number="101/QĐ-TVU",
            owner_id=u2.id,
            department_id=d2.id,
            expiry_date=today + timedelta(days=180), # Active
            status="active"
        )
        
        db.add_all([doc1, doc2, doc3, doc4])
        await db.commit()
        
        print("Successfully seeded Departments, Users, and Documents!")

if __name__ == "__main__":
    asyncio.run(seed())
