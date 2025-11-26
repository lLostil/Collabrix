from __future__ import annotations

from typing import List

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    spaces: Mapped[List["Space"]] = relationship("Space", back_populates="owner")
    created_pages: Mapped[List["Page"]] = relationship(
        "Page", back_populates="created_by_user", foreign_keys="Page.created_by_id"
    )
    page_versions: Mapped[List["PageVersion"]] = relationship("PageVersion", back_populates="created_by_user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
    inline_comments: Mapped[List["InlineComment"]] = relationship("InlineComment", back_populates="author")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="uploaded_by_user")
    space_memberships: Mapped[List["SpaceMembership"]] = relationship("SpaceMembership", back_populates="user")
