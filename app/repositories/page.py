from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Page, PageVersion


class PageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, page_id: int) -> Optional[Page]:
        return self.session.get(Page, page_id)

    def list_by_space(self, space_id: int) -> List[Page]:
        return list(self.session.scalars(select(Page).where(Page.space_id == space_id)))

    def create(
        self,
        *,
        space_id: int,
        title: str,
        slug: str,
        content: str,
        created_by_id: int,
        parent_page_id: int | None,
    ) -> Page:
        page = Page(
            space_id=space_id,
            title=title,
            slug=slug,
            parent_page_id=parent_page_id,
            created_by_id=created_by_id,
            updated_by_id=created_by_id,
        )
        self.session.add(page)
        self.session.flush()

        version = PageVersion(page_id=page.id, version_number=1, content=content, created_by_id=created_by_id)
        self.session.add(version)
        self.session.flush()
        return page

    def update(
        self,
        page: Page,
        *,
        title: str | None,
        slug: str | None,
        parent_page_id: int | None,
        content: str | None,
        updated_by_id: int,
    ) -> Page:
        if title is not None:
            page.title = title
        if slug is not None:
            page.slug = slug
        if parent_page_id is not None:
            page.parent_page_id = parent_page_id
        if content is not None:
            new_version_number = len(page.versions) + 1
            version = PageVersion(
                page_id=page.id, version_number=new_version_number, content=content, created_by_id=updated_by_id
            )
            self.session.add(version)
            self.session.flush()
        page.updated_by_id = updated_by_id
        self.session.add(page)
        return page

    def delete(self, page: Page) -> None:
        self.session.delete(page)
