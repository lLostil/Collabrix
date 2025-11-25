from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.page import PageRole


class PageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str


class PageCreate(PageBase):
    space_id: int
    content: str


class PageUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PageVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    version_number: int
    content: str
    created_at: datetime
    created_by_id: int


class PageRead(PageBase):
    id: int
    space_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    current_version_id: Optional[int]


class PagePermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    user_id: int
    role: PageRole
    created_at: datetime