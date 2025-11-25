import uuid

from sqlalchemy.orm import Session

from app.repositories.space import SpaceRepository
from app.schemas.space import SpaceCreate, SpaceRead, SpaceUpdate


class SpaceService:
    """Domain logic for space operations."""

    def __init__(self, session: Session):
        self.repository = SpaceRepository(session)

    def list_spaces(self) -> list[SpaceRead]:
        spaces = self.repository.list_spaces()
        return [SpaceRead.model_validate(space) for space in spaces]

    def get_space(self, space_id: uuid.UUID) -> SpaceRead | None:
        space = self.repository.get_space(space_id)
        return None if space is None else SpaceRead.model_validate(space)

    def create_space(self, payload: SpaceCreate) -> SpaceRead:
        space = self.repository.create_space(payload)
        return SpaceRead.model_validate(space)

    def update_space(self, space_id: uuid.UUID, payload: SpaceUpdate) -> SpaceRead | None:
        space = self.repository.get_space(space_id)
        if space is None:
            return None
        updated = self.repository.update_space(space, payload)
        return SpaceRead.model_validate(updated)

    def delete_space(self, space_id: uuid.UUID) -> bool:
        space = self.repository.get_space(space_id)
        if space is None:
            return False
        self.repository.delete_space(space)
        return True