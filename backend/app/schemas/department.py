"""
Pydantic schemas for Department API requests and responses.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# --- Request schemas ---

class DepartmentCreate(BaseModel):
    """Schema for creating a new department."""
    name: str
    code: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    manager_id: Optional[uuid.UUID] = None


class DepartmentUpdate(BaseModel):
    """Schema for updating a department."""
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    manager_id: Optional[uuid.UUID] = None


# --- Response schemas ---

class DepartmentResponse(BaseModel):
    """Schema for department in API responses."""
    id: uuid.UUID
    name: str
    code: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    manager_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DepartmentListResponse(BaseModel):
    """List of departments."""
    items: list[DepartmentResponse]
    total: int
