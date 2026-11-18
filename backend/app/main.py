from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import admin, auth, health, me
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging

settings = get_settings()
configure_logging("DEBUG" if settings.app_env == "development" else "INFO")

app = FastAPI(title="BE CYBER SMART")
register_error_handlers(app)

# Only our own website may call the API with cookies.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-CSRF-Token", "Authorization"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(me.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
