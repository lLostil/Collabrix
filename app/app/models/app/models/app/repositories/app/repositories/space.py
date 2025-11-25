import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceUpdate


class SpaceRepository:
    """Persistence layer for space entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list_spaces(self) -> list[Space]:
        statement = select(Space).order_by(Space.created_at)
        return list(self.session.scalars(statement))

    def get_space(self, space_id: uuid.UUID) -> Space | None:
        return self.session.get(Space, space_id)

    def create_space(self, payload: SpaceCreate) -> Space:
        space = Space(name=payload.name, description=payload.description)
        self.session.add(space)
        self.session.flush()
        return space

    def update_space(self, space: Space, payload: SpaceUpdate) -> Space:
        if payload.name is not None:
            space.name = payload.name
        if payload.description is not None:
            space.description = payload.description
        self.session.add(space)
        self.session.flush()
        return space

    def delete_space(self, space: Space) -> None:
        self.session.delete(space)