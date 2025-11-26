from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.pages import router as pages_router
from app.api.routes.spaces import router as spaces_router

__all__ = ["auth_router", "health_router", "pages_router", "spaces_router"]
