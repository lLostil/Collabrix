from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentCreate(BaseModel):
    page_id: int
    file_name: str
    file_path: str
    mime_type: str
    file_size: int
    created_by_id: int


class AttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    file_name: str
    file_path: str
    mime_type: str
    file_size: int
    created_by_id: int
    created_at: datetime
