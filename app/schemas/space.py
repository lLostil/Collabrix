from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.space import SpaceRole
from app.schemas.user import UserRead


class SpaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    key: str
    description: Optional[str] = None


class SpaceCreate(SpaceBase):
    owner_id: int


class SpaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SpaceRead(SpaceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class SpaceMembershipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    space_id: int
    role: SpaceRole
    created_at: datetime


class SpaceWithOwner(SpaceRead):
    owner: UserRead
