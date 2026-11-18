from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth_deps import CurrentUser, require_permission
from app.core.permissions import Permission
from app.schemas.auth import StatusResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
def ping(
    _user: Annotated[CurrentUser, Depends(require_permission(Permission.MANAGE_USERS))],
) -> StatusResponse:
    """A stand-in that proves roles and the second step are enforced."""
    return StatusResponse()
