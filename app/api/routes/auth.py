from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.schemas import AuthenticatedUser, LoginRequest, RegisterRequest, Token
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthenticatedUser, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> AuthenticatedUser:
    try:
        user = auth_service.register_user(email=payload.email, full_name=payload.full_name, password=payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    token = auth_service.create_token_for_user(user_id=user.id)
    return AuthenticatedUser(user=user, token=Token(access_token=token))


@router.post("/login", response_model=AuthenticatedUser)
def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> AuthenticatedUser:
    user = auth_service.authenticate_user(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_service.create_token_for_user(user_id=user.id)
    return AuthenticatedUser(user=user, token=Token(access_token=token))
