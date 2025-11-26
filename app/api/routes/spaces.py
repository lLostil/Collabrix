from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_db_session
from app.models import Space, SpaceRole, User
from app.schemas import SpaceCreate, SpaceRead, SpaceUpdate
from app.services import SpaceService
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_db_session
from app.models import Space, SpaceRole, User
from app.schemas import SpaceCreate, SpaceRead, SpaceUpdate
from app.services import SpaceService

router = APIRouter(prefix="/spaces", tags=["spaces"])


def get_space_service(db=Depends(get_db_session)) -> SpaceService:
    return SpaceService(db)


@router.get("/", response_model=list[SpaceRead])
def list_spaces(space_service: SpaceService = Depends(get_space_service)) -> list[Space]:
    return space_service.list_spaces()


@router.post("/", response_model=SpaceRead, status_code=status.HTTP_201_CREATED)
def create_space(
    payload: SpaceCreate,
    current_user: User = Depends(get_current_user),
    space_service: SpaceService = Depends(get_space_service),
) -> Space:
    return space_service.create_space(
        name=payload.name, key=payload.key, description=payload.description, owner_id=current_user.id
    )


@router.get("/{space_id}", response_model=SpaceRead)
def get_space(space_id: int, space_service: SpaceService = Depends(get_space_service)) -> Space:
    try:
        return space_service.get_space(space_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{space_id}", response_model=SpaceRead)
def update_space(
    space_id: int,
    payload: SpaceUpdate,
    current_user: User = Depends(get_current_user),
    space_service: SpaceService = Depends(get_space_service),
) -> Space:
    space = space_service.get_space(space_id)
    if not space_service.user_has_access(
        user_id=current_user.id, space=space, allowed_roles=[SpaceRole.ADMIN, SpaceRole.EDITOR]
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return space_service.update_space(space_id, name=payload.name, description=payload.description)


@router.delete("/{space_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_space(
    space_id: int,
    current_user: User = Depends(get_current_user),
    space_service: SpaceService = Depends(get_space_service),
) -> None:
    space = space_service.get_space(space_id)
    if not space_service.user_has_access(user_id=current_user.id, space=space, allowed_roles=[SpaceRole.ADMIN]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    space_service.delete_space(space_id)
