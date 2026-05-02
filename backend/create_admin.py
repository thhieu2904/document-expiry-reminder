import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import async_session
from app.core.security import create_auth_user, supabase_admin
from app.models.user import User

async def create_first_admin():
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    full_name = input("Enter admin full name: ")

    async with async_session() as db:
        # Kiểm tra xem user có trong DB chưa
        res = await db.execute(select(User).where(User.email == email))
        if res.scalar_one_or_none():
            print("Tài khoản này đã tồn tại trong Database!")
            return

        print("Đang tạo/kiểm tra tài khoản trên Supabase Auth...")
        auth_id = None
        try:
            auth_result = await create_auth_user(email, password)
            auth_id = auth_result["id"]
        except Exception as e:
            error_msg = str(e).lower()
            if "already" in error_msg and ("registered" in error_msg or "exists" in error_msg):
                print("Tài khoản đã có trên Supabase Auth (từ lần chạy trước). Đang đồng bộ xuống Database...")
                # Lấy ID từ Supabase Auth
                users_resp = supabase_admin.auth.admin.list_users()
                # Tùy phiên bản supabase-py, list_users() trả về list hoặc object có thuộc tính users
                users_list = getattr(users_resp, 'users', users_resp) 
                for u in users_list:
                    if u.email == email:
                        auth_id = u.id
                        break
            else:
                print(f"Lỗi Supabase Auth: {e}")
                return

        if not auth_id:
            print("Không thể lấy ID từ Supabase Auth.")
            return

        print("Đang lưu vào Database PostgreSQL...")
        user = User(
            id=uuid.UUID(auth_id),
            full_name=full_name,
            email=email,
            role="admin",
            can_login=True,
            status="active"
        )
        db.add(user)
        await db.commit()  # Lỗi lần trước là do thiếu lệnh commit này!
        print(f"Thành công! Admin đã được đồng bộ với Database. (ID: {user.id})")

if __name__ == "__main__":
    asyncio.run(create_first_admin())
