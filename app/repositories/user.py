from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.scalar(select(User).where(User.email == email))

    def get(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def create(self, *, email: str, full_name: str, password_hash: str) -> User:
        user = User(email=email, full_name=full_name, password_hash=password_hash)
        self.session.add(user)
        self.session.flush()
        return user
