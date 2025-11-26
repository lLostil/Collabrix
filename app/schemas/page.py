from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    parent_page_id: Optional[int] = None


class PageCreate(PageBase):
    space_id: int
    content: str
    created_by_id: int
    updated_by_id: int


class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    parent_page_id: Optional[int] = None
    content: Optional[str] = None
    updated_by_id: Optional[int] = None


class PageRead(PageBase):
    id: int
    space_id: int
    created_by_id: int
    updated_by_id: int
    created_at: datetime
    updated_at: datetime


class PageVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    version_number: int
    content: str
    created_at: datetime
    created_by_id: int
