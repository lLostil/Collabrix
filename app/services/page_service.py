from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.models import Page, SpaceRole
from app.repositories import PageRepository
from app.services.space_service import SpaceService


class PageService:
    def __init__(self, session: Session):
        self.session = session
        self.pages = PageRepository(session)
        self.space_service = SpaceService(session)

    def list_pages(self, *, space_id: int) -> List[Page]:
        return self.pages.list_by_space(space_id)

    def get_page(self, page_id: int) -> Page:
        page = self.pages.get(page_id)
        if not page:
            raise ValueError("Page not found")
        return page

    def create_page(
        self, *, space_id: int, title: str, slug: str, content: str, created_by_id: int, parent_page_id: int | None
    ) -> Page:
        space = self.space_service.get_space(space_id)
        page = self.pages.create(
            space_id=space.id,
            title=title,
            slug=slug,
            content=content,
            created_by_id=created_by_id,
            parent_page_id=parent_page_id,
        )
        self.session.commit()
        self.session.refresh(page)
        return page

    def update_page(
        self,
        page_id: int,
        *,
        title: str | None,
        slug: str | None,
        parent_page_id: int | None,
        content: str | None,
        updated_by_id: int,
    ) -> Page:
        page = self.get_page(page_id)
        updated = self.pages.update(
            page,
            title=title,
            slug=slug,
            parent_page_id=parent_page_id,
            content=content,
            updated_by_id=updated_by_id,
        )
        self.session.commit()
        self.session.refresh(updated)
        return updated

    def delete_page(self, page_id: int) -> None:
        page = self.get_page(page_id)
        self.pages.delete(page)
        self.session.commit()

    def user_can_edit(self, *, user_id: int, page: Page) -> bool:
        space = page.space
        return self.space_service.user_has_access(
            user_id=user_id, space=space, allowed_roles=[SpaceRole.OWNER, SpaceRole.ADMIN, SpaceRole.EDITOR]
        )

    def user_can_view(self, *, user_id: int, page: Page) -> bool:
        space = page.space
        return self.space_service.user_has_access(
            user_id=user_id, space=space, allowed_roles=[SpaceRole.OWNER, SpaceRole.ADMIN, SpaceRole.EDITOR, SpaceRole.VIEWER]
        )
