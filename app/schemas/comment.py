from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    page_id: int
    content: str
    created_by_id: int
    parent_comment_id: Optional[int] = None
    resolved: bool = False


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    parent_comment_id: Optional[int]
    content: str
    created_by_id: int
    resolved: bool
    created_at: datetime


class InlineCommentCreate(BaseModel):
    page_id: int
    page_version_id: int
    selection_start: int
    selection_end: int
    content: str
    created_by_id: int
    resolved: bool = False
    comment_id: Optional[int] = None


class InlineCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    page_version_id: int
    selection_start: int
    selection_end: int
    content: str
    created_by_id: int
    resolved: bool
    comment_id: Optional[int]
    created_at: datetime
