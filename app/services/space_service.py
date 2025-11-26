from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.models import Space, SpaceMembership, SpaceRole
from app.repositories import SpaceRepository


class SpaceService:
    def __init__(self, session: Session):
        self.session = session
        self.spaces = SpaceRepository(session)

    def list_spaces(self) -> List[Space]:
        return self.spaces.list()

    def get_space(self, space_id: int) -> Space:
        space = self.spaces.get(space_id)
        if not space:
            raise ValueError("Space not found")
        return space

    def create_space(self, *, name: str, key: str, description: str | None, owner_id: int) -> Space:
        space = self.spaces.create(name=name, key=key, description=description, owner_id=owner_id)
        self.session.commit()
        self.session.refresh(space)
        return space

    def update_space(self, space_id: int, *, name: str | None, description: str | None) -> Space:
        space = self.get_space(space_id)
        updated = self.spaces.update(space, name=name, description=description)
        self.session.commit()
        self.session.refresh(updated)
        return updated

    def delete_space(self, space_id: int) -> None:
        space = self.get_space(space_id)
        self.spaces.delete(space)
        self.session.commit()

    def user_has_access(self, *, user_id: int, space: Space, allowed_roles: list[SpaceRole]) -> bool:
        for membership in space.memberships:
            if membership.user_id == user_id and membership.role in allowed_roles:
                return True
        return False
