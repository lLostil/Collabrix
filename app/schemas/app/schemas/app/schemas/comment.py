from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    page_id: int
    body: str
    parent_comment_id: Optional[int] = None


class InlineCommentCreate(BaseModel):
    page_version_id: int
    anchor: str
    body: str


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    author_id: int
    body: str
    parent_comment_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class InlineCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comment_id: int
    page_version_id: int
    anchor: str
    author_id: int
    created_at: datetime
    updated_at: datetime