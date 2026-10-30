from fastapi import FastAPI

from app.api.v1 import health

app = FastAPI(title="BE CYBER SMART")
app.include_router(health.router, prefix="/api/v1")
