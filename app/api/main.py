from fastapi import APIRouter

from app.api.routes.space_routes import router as space_router

api_router = APIRouter()
api_router.include_router(space_router)
from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import auth_router, health_router, pages_router, spaces_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(spaces_router, prefix="/api/v1")
api_router.include_router(pages_router, prefix="/api/v1")