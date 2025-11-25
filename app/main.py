from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title=settings.project_name)
app.include_router(api_router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    """Lightweight health endpoint."""

    return {"status": "ok"}