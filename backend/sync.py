import asyncio
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import async_session
from app.core.security import supabase_admin
from app.models.user import User

async def sync():
    async with async_session() as db:
        res = supabase_admin.auth.admin.list_users()
        ulist = getattr(res, 'users', res)
        uid = next((u.id for u in ulist if u.email == 'thhieu2904@gmail.com'), None)
        if uid:
            user = User(
                id=uuid.UUID(uid),
                full_name='Nguyễn Thanh Hiếu',
                email='thhieu2904@gmail.com',
                role='admin',
                can_login=True,
                status='active'
            )
            db.add(user)
            await db.commit()
            print('Đã đồng bộ xong admin vào database!')
        else:
            print('Không tìm thấy user trên Supabase')

asyncio.run(sync())
