import datetime
import uuid

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Space(Base):
    """Workspace grouping pages and discussions."""

    __tablename__ = "spaces"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = mapped_column(String(length=200), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
from __future__ import annotations

from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class SpaceRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Space(TimestampMixin, Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(1024))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="spaces")
    pages: Mapped[List["Page"]] = relationship("Page", back_populates="space")
    memberships: Mapped[List["SpaceMembership"]] = relationship(
        "SpaceMembership", back_populates="space", cascade="all, delete-orphan"
    )


class SpaceMembership(TimestampMixin, Base):
    __tablename__ = "space_memberships"
    __table_args__ = (UniqueConstraint("user_id", "space_id", name="uq_space_member"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), nullable=False)
    role: Mapped[SpaceRole] = mapped_column(default=SpaceRole.VIEWER)

    user: Mapped["User"] = relationship("User", back_populates="space_memberships")
    space: Mapped["Space"] = relationship("Space", back_populates="memberships")