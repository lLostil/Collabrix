from __future__ import annotations

from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin


class PageRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class Page(TimestampMixin, Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    current_version_id: Mapped[int | None] = mapped_column(ForeignKey("page_versions.id"))

    space: Mapped["Space"] = relationship("Space", back_populates="pages")
    created_by_user: Mapped["User"] = relationship("User", back_populates="created_pages")
    versions: Mapped[List["PageVersion"]] = relationship(
        "PageVersion", back_populates="page", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="page")
    attachments: Mapped[List["Attachment"]] = relationship(
        "Attachment", back_populates="page", cascade="all, delete-orphan"
    )
    permissions: Mapped[List["PagePermission"]] = relationship(
        "PagePermission", back_populates="page", cascade="all, delete-orphan"
    )


class PageVersion(TimestampMixin, Base):
    __tablename__ = "page_versions"
    __table_args__ = (UniqueConstraint("page_id", "version_number", name="uq_page_version_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    page: Mapped["Page"] = relationship("Page", back_populates="versions")
    created_by_user: Mapped["User"] = relationship("User", back_populates="page_versions")
    inline_comments: Mapped[List["InlineComment"]] = relationship("InlineComment", back_populates="page_version")


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    parent_comment_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id"))

    page: Mapped["Page"] = relationship("Page", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
    replies: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="parent_comment", remote_side="Comment.id"
    )
    parent_comment: Mapped[Optional["Comment"]] = relationship(
        "Comment", back_populates="replies", remote_side="Comment.id"
    )
    inline_comment: Mapped[Optional["InlineComment"]] = relationship(
        "InlineComment", back_populates="comment", uselist=False
    )


class InlineComment(TimestampMixin, Base):
    __tablename__ = "inline_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_version_id: Mapped[int] = mapped_column(ForeignKey("page_versions.id"), nullable=False)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=False, unique=True)
    anchor: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    page_version: Mapped["PageVersion"] = relationship("PageVersion", back_populates="inline_comments")
    comment: Mapped["Comment"] = relationship("Comment", back_populates="inline_comment")
    author: Mapped["User"] = relationship("User", back_populates="inline_comments")


class Attachment(TimestampMixin, Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    page: Mapped["Page"] = relationship("Page", back_populates="attachments")
    uploaded_by_user: Mapped["User"] = relationship("User", back_populates="attachments")


class PagePermission(TimestampMixin, Base):
    __tablename__ = "page_permissions"
    __table_args__ = (UniqueConstraint("page_id", "user_id", name="uq_page_permission"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[PageRole] = mapped_column(default=PageRole.VIEWER)

    page: Mapped["Page"] = relationship("Page", back_populates="permissions")
    user: Mapped["User"] = relationship("User", back_populates="page_permissions")