import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.core.storage import upload_file_async, get_file_url, delete_file_async

router = APIRouter(prefix="/documents", tags=["documents"])

def inject_file_url(doc: Document) -> DocumentResponse:
    doc_dict = {
        "id": doc.id,
        "title": doc.title,
        "document_number": doc.document_number,
        "description": doc.description,
        "department_id": doc.department_id,
        "expiry_date": doc.expiry_date,
        "status": doc.status,
        "owner_id": doc.owner_id,
        "file_path": doc.file_path,
        "file_name": doc.file_name,
        "file_size": doc.file_size,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
    }
    if doc.file_path:
        # Dynamically inject public URL
        doc_dict["file_url"] = get_file_url(doc.file_path)
    return DocumentResponse(**doc_dict)

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    department_id: Optional[uuid.UUID] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Document)
    if status_filter:
        query = query.where(Document.status == status_filter)
    if department_id:
        query = query.where(Document.department_id == department_id)
    if search:
        search_pattern = f"%{search}%"
        from sqlalchemy import or_
        query = query.where(or_(
            Document.title.ilike(search_pattern),
            Document.document_number.ilike(search_pattern)
        ))
        
    query = query.order_by(Document.expiry_date.asc()) # Default sort by expiry date
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    docs = result.scalars().all()
    
    return [inject_file_url(d) for d in docs]

@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    data: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_doc = Document(
        **data.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return inject_file_url(new_doc)

@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return inject_file_url(doc)

@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(
    doc_id: uuid.UUID,
    data: DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(doc, key, value)
        
    await db.commit()
    await db.refresh(doc)
    return inject_file_url(doc)

@router.post("/{doc_id}/upload", response_model=DocumentResponse)
async def upload_document_file(
    doc_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_bytes = await file.read()
    # Format path: {doc_id}/{filename}
    file_path = f"{doc_id}/{file.filename}"
    
    # Upload to Supabase Storage
    try:
        await upload_file_async(file_bytes, file_path, file.content_type or "application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to storage: {str(e)}")

    # Delete old file if exists
    if doc.file_path and doc.file_path != file_path:
        try:
            await delete_file_async(doc.file_path)
        except:
            pass # Ignore deletion errors for old files

    doc.file_path = file_path
    doc.file_name = file.filename
    doc.file_size = len(file_bytes)
    await db.commit()
    await db.refresh(doc)
    
    return inject_file_url(doc)

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if doc.file_path:
        try:
            await delete_file_async(doc.file_path)
        except:
            pass
            
    await db.delete(doc)
    await db.commit()
