import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import Session, get_db
from app.schemas.space import SpaceCreate, SpaceRead, SpaceUpdate
from app.services.space_service import SpaceService

router = APIRouter(prefix="/api/v1/spaces", tags=["spaces"])


@router.get("/", response_model=list[SpaceRead])
def list_spaces(session: Session = Depends(get_db)) -> list[SpaceRead]:
    service = SpaceService(session)
    return service.list_spaces()


@router.get("/{space_id}", response_model=SpaceRead)
def get_space(space_id: uuid.UUID, session: Session = Depends(get_db)) -> SpaceRead:
    service = SpaceService(session)
    space = service.get_space(space_id)
    if space is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
    return space


@router.post("/", response_model=SpaceRead, status_code=status.HTTP_201_CREATED)
def create_space(payload: SpaceCreate, session: Session = Depends(get_db)) -> SpaceRead:
    service = SpaceService(session)
    return service.create_space(payload)


@router.put("/{space_id}", response_model=SpaceRead)
def update_space(
    space_id: uuid.UUID, payload: SpaceUpdate, session: Session = Depends(get_db)
) -> SpaceRead:
    service = SpaceService(session)
    space = service.update_space(space_id, payload)
    if space is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")
    return space


@router.delete("/{space_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_space(space_id: uuid.UUID, session: Session = Depends(get_db)) -> None:
    service = SpaceService(session)
    deleted = service.delete_space(space_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Space not found")