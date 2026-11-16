from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.deps import get_auth_service, get_login_service
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import AuthService
from app.services.login_service import LoginService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterResponse:
    return RegisterResponse(id=service.register(data))


@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    service: Annotated[LoginService, Depends(get_login_service)],
) -> LoginResponse:
    source_ip = request.client.host if request.client else "unknown"
    device = request.headers.get("user-agent", "")[:200] or None
    return LoginResponse(
        id=service.login(data, source_ip=source_ip, device_summary=device)
    )