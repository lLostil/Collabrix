from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_db_session
from app.models import Page, User
from app.schemas import PageCreate, PageRead, PageUpdate
from app.services import PageService

router = APIRouter(prefix="/pages", tags=["pages"])


def get_page_service(db=Depends(get_db_session)) -> PageService:
    return PageService(db)


@router.get("/spaces/{space_id}", response_model=list[PageRead])
def list_pages(space_id: int, page_service: PageService = Depends(get_page_service)) -> list[Page]:
    return page_service.list_pages(space_id=space_id)


@router.post("/", response_model=PageRead, status_code=status.HTTP_201_CREATED)
def create_page(
    payload: PageCreate,
    current_user: User = Depends(get_current_user),
    page_service: PageService = Depends(get_page_service),
) -> Page:
    return page_service.create_page(
        space_id=payload.space_id,
        title=payload.title,
        slug=payload.slug,
        content=payload.content,
        created_by_id=current_user.id,
        parent_page_id=payload.parent_page_id,
    )


@router.get("/{page_id}", response_model=PageRead)
def get_page(page_id: int, page_service: PageService = Depends(get_page_service)) -> Page:
    try:
        return page_service.get_page(page_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{page_id}", response_model=PageRead)
def update_page(
    page_id: int,
    payload: PageUpdate,
    current_user: User = Depends(get_current_user),
    page_service: PageService = Depends(get_page_service),
) -> Page:
    page = page_service.get_page(page_id)
    if not page_service.user_can_edit(user_id=current_user.id, page=page):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return page_service.update_page(
        page_id,
        title=payload.title,
        slug=payload.slug,
        parent_page_id=payload.parent_page_id,
        content=payload.content,
        updated_by_id=current_user.id,
    )


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_page(
    page_id: int,
    current_user: User = Depends(get_current_user),
    page_service: PageService = Depends(get_page_service),
) -> None:
    page = page_service.get_page(page_id)
    if not page_service.user_can_edit(user_id=current_user.id, page=page):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    page_service.delete_page(page_id)
