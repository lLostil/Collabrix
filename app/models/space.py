from __future__ import annotations

from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import CreatedAtMixin, TimestampMixin


class SpaceRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Space(TimestampMixin, Base):
    __tablename__ = "spaces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1024))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    owner: Mapped["User"] = relationship("User", back_populates="spaces")
    pages: Mapped[List["Page"]] = relationship("Page", back_populates="space", cascade="all, delete-orphan")
    memberships: Mapped[List["SpaceMembership"]] = relationship(
        "SpaceMembership", back_populates="space", cascade="all, delete-orphan"
    )


class SpaceMembership(CreatedAtMixin, Base):
    __tablename__ = "space_memberships"
    __table_args__ = (UniqueConstraint("user_id", "space_id", name="uq_space_member"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), nullable=False, index=True)
    role: Mapped[SpaceRole] = mapped_column(default=SpaceRole.VIEWER)

    user: Mapped["User"] = relationship("User", back_populates="space_memberships")
    space: Mapped["Space"] = relationship("Space", back_populates="memberships")


Index("ix_spaces_key", Space.key, unique=True)  # type: ignore[name-defined]
