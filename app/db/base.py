from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for declarative models."""

    pass
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[misc]
        return cls.__name__.lower()