import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class SpaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class SpaceCreate(SpaceBase):
    pass


class SpaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class SpaceRead(SpaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
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
    pass


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