from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.user import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class AuthenticatedUser(BaseModel):
    user: UserRead
    token: Token