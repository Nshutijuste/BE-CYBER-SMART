from fastapi import FastAPI

from app.api.v1 import health
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging

settings = get_settings()
configure_logging("DEBUG" if settings.app_env == "development" else "INFO")

app = FastAPI (title="BE CYBER SMART")
register_error_handlers(app)

app.include_router(health.router, prefix="/api/v1")

