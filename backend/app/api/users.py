"""
Users API routes: CRUD operations for managing users/contacts.
Admin only - all endpoints require admin role.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_admin
from app.core.security import create_auth_user, update_auth_password
from app.models.user import User
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
)

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(require_admin)])


@router.get("", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    department_id: uuid.UUID | None = None,
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
):
    """List all users with optional search and filters."""
    query = select(User)

    # Apply filters
    if search:
        query = query.where(
            User.full_name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
        )
    if department_id:
        query = query.where(User.department_id == department_id)
    if status_filter:
        query = query.where(User.status == status_filter)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.order_by(User.full_name).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user. If can_login=True, also creates Supabase Auth account."""
    # Check duplicate email
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {data.email} already exists",
        )

    # If user needs login access, create Supabase Auth account
    auth_id = None
    if data.can_login:
        if not data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required for users with login access",
            )
        try:
            auth_result = await create_auth_user(data.email, data.password)
            auth_id = auth_result["id"]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create auth account: {str(e)}",
            )

    # Create user in our database
    user = User(
        id=uuid.UUID(auth_id) if auth_id else uuid.uuid4(),
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        department_id=data.department_id,
        position=data.position,
        role=data.role,
        can_login=data.can_login,
        manager_id=data.manager_id,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update user information."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update fields that were provided
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Soft delete a user (set status to inactive)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.status = "inactive"
    await db.flush()
