from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth_deps import CurrentUser, get_current_user
from app.schemas.auth import MeResponse

router = APIRouter(tags=["me"])


@router.get("/me")
def me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(
        id=user.id,
        role=user.role,
        permissions=sorted(p.value for p in user.permissions),
        mfa_verified=user.mfa_verified,
    )
