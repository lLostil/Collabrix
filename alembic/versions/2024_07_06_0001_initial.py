"""initial schema

Revision ID: 2024_07_06_0001
Revises: 
Create Date: 2024-07-06 00:01:00.000000
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2024_07_06_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "spaces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_spaces_key", "spaces", ["key"], unique=True)
    op.create_index("ix_spaces_owner_id", "spaces", ["owner_id"], unique=False)

    op.create_table(
        "space_memberships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("space_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.Enum("owner", "admin", "editor", "viewer", name="spacerole"), nullable=False, server_default="viewer"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "space_id", name="uq_space_member"),
    )
    op.create_index("ix_space_memberships_user_id", "space_memberships", ["user_id"], unique=False)
    op.create_index("ix_space_memberships_space_id", "space_memberships", ["space_id"], unique=False)

    op.create_table(
        "pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("space_id", sa.Integer(), nullable=False),
        sa.Column("parent_page_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("updated_by_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_page_id"], ["pages.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["space_id"], ["spaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("space_id", "slug", name="uq_page_space_slug"),
    )
    op.create_index("ix_pages_slug_space", "pages", ["space_id", "slug"], unique=True)
    op.create_index("ix_pages_created_at", "pages", ["created_at"], unique=False)
    op.create_index("ix_pages_space_id", "pages", ["space_id"], unique=False)

    op.create_table(
        "page_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("page_id", "version_number", name="uq_page_version_number"),
    )
    op.create_index("ix_page_versions_created_at", "page_versions", ["created_at"], unique=False)
    op.create_index("ix_page_versions_page_id", "page_versions", ["page_id"], unique=False)

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("parent_comment_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_comment_id"], ["comments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_comments_created_at", "comments", ["created_at"], unique=False)
    op.create_index("ix_comments_page_id", "comments", ["page_id"], unique=False)

    op.create_table(
        "inline_comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("page_version_id", sa.Integer(), nullable=False),
        sa.Column("selection_start", sa.Integer(), nullable=False),
        sa.Column("selection_end", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
        sa.Column("comment_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["comment_id"], ["comments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_version_id"], ["page_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_inline_comments_created_at", "inline_comments", ["created_at"], unique=False)
    op.create_index("ix_inline_comments_page_id", "inline_comments", ["page_id"], unique=False)
    op.create_index("ix_inline_comments_page_version_id", "inline_comments", ["page_version_id"], unique=False)

    op.create_table(
        "attachments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("mime_type", sa.String(length=255), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_attachments_created_at", "attachments", ["created_at"], unique=False)
    op.create_index("ix_attachments_page_id", "attachments", ["page_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_attachments_page_id", table_name="attachments")
    op.drop_index("ix_attachments_created_at", table_name="attachments")
    op.drop_table("attachments")

    op.drop_index("ix_inline_comments_page_version_id", table_name="inline_comments")
    op.drop_index("ix_inline_comments_page_id", table_name="inline_comments")
    op.drop_index("ix_inline_comments_created_at", table_name="inline_comments")
    op.drop_table("inline_comments")

    op.drop_index("ix_comments_page_id", table_name="comments")
    op.drop_index("ix_comments_created_at", table_name="comments")
    op.drop_table("comments")

    op.drop_index("ix_page_versions_page_id", table_name="page_versions")
    op.drop_index("ix_page_versions_created_at", table_name="page_versions")
    op.drop_table("page_versions")

    op.drop_index("ix_pages_space_id", table_name="pages")
    op.drop_index("ix_pages_created_at", table_name="pages")
    op.drop_index("ix_pages_slug_space", table_name="pages")
    op.drop_table("pages")

    op.drop_index("ix_space_memberships_space_id", table_name="space_memberships")
    op.drop_index("ix_space_memberships_user_id", table_name="space_memberships")
    op.drop_table("space_memberships")
    op.execute("DROP TYPE spacerole")

    op.drop_index("ix_spaces_owner_id", table_name="spaces")
    op.drop_index("ix_spaces_key", table_name="spaces")
    op.drop_table("spaces")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
