"""
Pydantic schemas for User API requests and responses.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# --- Request schemas ---

class UserCreate(BaseModel):
    """Schema for creating a new user (email recipient or admin)."""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    position: Optional[str] = None
    role: str = "staff"
    can_login: bool = False
    manager_id: Optional[uuid.UUID] = None

    # Only needed if can_login=True (will create Supabase Auth account)
    password: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    position: Optional[str] = None
    role: Optional[str] = None
    can_login: Optional[bool] = None
    manager_id: Optional[uuid.UUID] = None
    status: Optional[str] = None


# --- Response schemas ---

class UserResponse(BaseModel):
    """Schema for user in API responses."""
    id: uuid.UUID
    full_name: str
    email: str
    phone: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    position: Optional[str] = None
    role: str
    can_login: bool
    manager_id: Optional[uuid.UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    """Paginated list of users."""
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
