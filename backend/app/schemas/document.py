from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
import uuid
from typing import Optional

class DocumentBase(BaseModel):
    title: str
    document_number: Optional[str] = None
    description: Optional[str] = None
    department_id: uuid.UUID
    expiry_date: date
    status: Optional[str] = "active"

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    document_number: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_url: Optional[str] = None # Dynamically injected
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
