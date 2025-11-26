from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Space, SpaceMembership, SpaceRole


class SpaceRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> List[Space]:
        return list(self.session.scalars(select(Space)))

    def get(self, space_id: int) -> Optional[Space]:
        return self.session.get(Space, space_id)

    def create(self, *, name: str, key: str, description: str | None, owner_id: int) -> Space:
        space = Space(name=name, key=key, description=description, owner_id=owner_id)
        self.session.add(space)
        self.session.flush()
        membership = SpaceMembership(user_id=owner_id, space_id=space.id, role=SpaceRole.OWNER)
        self.session.add(membership)
        return space

    def update(self, space: Space, *, name: str | None, description: str | None) -> Space:
        if name is not None:
            space.name = name
        if description is not None:
            space.description = description
        self.session.add(space)
        return space

    def delete(self, space: Space) -> None:
        self.session.delete(space)
