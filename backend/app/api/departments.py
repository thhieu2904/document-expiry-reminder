"""
Departments API routes: CRUD operations.
Admin only.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate, DepartmentUpdate,
    DepartmentResponse, DepartmentListResponse,
)

router = APIRouter(
    prefix="/departments", tags=["Departments"],
    dependencies=[Depends(require_admin)],
)


@router.get("", response_model=DepartmentListResponse)
async def list_departments(
    db: AsyncSession = Depends(get_db),
):
    """List all departments."""
    result = await db.execute(select(Department).order_by(Department.name))
    departments = result.scalars().all()
    return DepartmentListResponse(
        items=[DepartmentResponse.model_validate(d) for d in departments],
        total=len(departments),
    )


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new department."""
    # Check duplicate code
    if data.code:
        existing = await db.execute(
            select(Department).where(Department.code == data.code)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Department with code '{data.code}' already exists",
            )

    department = Department(
        name=data.name,
        code=data.code,
        parent_id=data.parent_id,
        manager_id=data.manager_id,
    )
    db.add(department)
    await db.flush()
    await db.refresh(department)
    return DepartmentResponse.model_validate(department)


@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(
    dept_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a department by ID."""
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return DepartmentResponse.model_validate(dept)


@router.put("/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: uuid.UUID,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a department."""
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dept, field, value)

    await db.flush()
    await db.refresh(dept)
    return DepartmentResponse.model_validate(dept)


@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    dept_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a department."""
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    await db.delete(dept)
    await db.flush()
