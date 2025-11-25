from __future__ import annotations

from datetime import timedelta
from typing import Optional

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from app.models import User
from app.repositories import UserRepository


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.users = UserRepository(session)

    def register_user(self, *, email: str, full_name: str, password: str) -> User:
        existing = self.users.get_by_email(email)
        if existing:
            raise ValueError("User already exists")
        hashed_password = get_password_hash(password)
        user = self.users.create(email=email, full_name=full_name, hashed_password=hashed_password)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, *, email: str, password: str) -> Optional[User]:
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token_for_user(self, *, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        return create_access_token(subject=user_id, expires_delta=expires_delta)

    def decode_token(self, token: str) -> Optional[int]:
        try:
            payload = decode_access_token(token)
            user_id = int(payload.get("sub"))
        except (JWTError, ValueError, TypeError):
            return None
        return user_id