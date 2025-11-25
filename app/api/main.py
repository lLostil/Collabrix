from fastapi import APIRouter

from app.api.routes.space_routes import router as space_router

api_router = APIRouter()
api_router.include_router(space_router)