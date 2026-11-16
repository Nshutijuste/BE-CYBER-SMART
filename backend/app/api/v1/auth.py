from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterResponse:
    return RegisterResponse(id=service.register(data))