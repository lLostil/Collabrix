from __future__ import annotations

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title=settings.project_name)
app.include_router(api_router)
