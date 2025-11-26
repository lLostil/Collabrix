from __future__ import annotations

from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import CreatedAtMixin, TimestampMixin


class Page(TimestampMixin, Base):
    __tablename__ = "pages"
    __table_args__ = (UniqueConstraint("space_id", "slug", name="uq_page_space_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    space_id: Mapped[int] = mapped_column(ForeignKey("spaces.id"), nullable=False, index=True)
    parent_page_id: Mapped[int | None] = mapped_column(ForeignKey("pages.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    updated_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    space: Mapped["Space"] = relationship("Space", back_populates="pages")
    created_by_user: Mapped["User"] = relationship(
        "User", foreign_keys=[created_by_id], back_populates="created_pages"
    )
    updated_by_user: Mapped["User"] = relationship("User", foreign_keys=[updated_by_id])
    parent: Mapped[Optional["Page"]] = relationship("Page", remote_side="Page.id")
    children: Mapped[List["Page"]] = relationship("Page", back_populates="parent")
    versions: Mapped[List["PageVersion"]] = relationship(
        "PageVersion", back_populates="page", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="page", cascade="all, delete-orphan")
    inline_comments: Mapped[List["InlineComment"]] = relationship(
        "InlineComment", back_populates="page", cascade="all, delete-orphan"
    )
    attachments: Mapped[List["Attachment"]] = relationship(
        "Attachment", back_populates="page", cascade="all, delete-orphan"
    )


class PageVersion(CreatedAtMixin, Base):
    __tablename__ = "page_versions"
    __table_args__ = (UniqueConstraint("page_id", "version_number", name="uq_page_version_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    page: Mapped["Page"] = relationship("Page", back_populates="versions")
    created_by_user: Mapped["User"] = relationship("User", back_populates="page_versions")
    inline_comments: Mapped[List["InlineComment"]] = relationship(
        "InlineComment", back_populates="page_version", cascade="all, delete-orphan"
    )


class Comment(CreatedAtMixin, Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False, index=True)
    parent_comment_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id"), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    page: Mapped["Page"] = relationship("Page", back_populates="inline_comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
    replies: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="parent_comment", remote_side="Comment.id"
    )
    parent_comment: Mapped[Optional["Comment"]] = relationship(
        "Comment", back_populates="replies", remote_side="Comment.id"
    )
    inline_comments: Mapped[List["InlineComment"]] = relationship(
        "InlineComment", back_populates="comment", cascade="all, delete-orphan"
    )


class InlineComment(CreatedAtMixin, Base):
    __tablename__ = "inline_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False, index=True)
    page_version_id: Mapped[int] = mapped_column(ForeignKey("page_versions.id"), nullable=False, index=True)
    selection_start: Mapped[int] = mapped_column(nullable=False)
    selection_end: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    comment_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id"), index=True)

    page: Mapped["Page"] = relationship("Page", back_populates="comments")
    page_version: Mapped["PageVersion"] = relationship("PageVersion", back_populates="inline_comments")
    author: Mapped["User"] = relationship("User", back_populates="inline_comments")
    comment: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="inline_comments")


class Attachment(CreatedAtMixin, Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    page: Mapped["Page"] = relationship("Page", back_populates="attachments")
    uploaded_by_user: Mapped["User"] = relationship("User", back_populates="attachments")


Index("ix_pages_slug_space", Page.space_id, Page.slug, unique=True)  # type: ignore[name-defined]
Index("ix_pages_created_at", Page.created_at)  # type: ignore[name-defined]
Index("ix_page_versions_created_at", PageVersion.created_at)  # type: ignore[name-defined]
Index("ix_comments_created_at", Comment.created_at)  # type: ignore[name-defined]
Index("ix_inline_comments_created_at", InlineComment.created_at)  # type: ignore[name-defined]
Index("ix_attachments_created_at", Attachment.created_at)  # type: ignore[name-defined]
