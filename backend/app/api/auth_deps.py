"""Who is calling, and may they? Checked on the server for every request."""

import secrets
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request

from app.api.cookies import ACCESS_COOKIE, CSRF_COOKIE, CSRF_HEADER
from app.api.deps import get_token_service, get_user_repository
from app.core.errors import (
    ForbiddenError,
    InvalidCsrfError,
    MfaRequiredError,
    NotAuthenticatedError,
)
from app.core.permissions import MFA_REQUIRED_ROLES, Permission, permissions_for
from app.core.tokens import InvalidTokenError, TokenService
from app.domain.interfaces import UserRepository


@dataclass(frozen=True)
class CurrentUser:
    id: uuid.UUID
    role: str
    permissions: frozenset[Permission]
    mfa_verified: bool


def _raw_token(request: Request) -> str | None:
    header = request.headers.get("authorization", "")
    scheme, _, value = header.partition(" ")
    if scheme.lower() == "bearer" and value:
        return value.strip()
    return request.cookies.get(ACCESS_COOKIE)


def get_current_user(
    request: Request,
    tokens: Annotated[TokenService, Depends(get_token_service)],
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> CurrentUser:
    raw = _raw_token(request)
    if not raw:
        raise NotAuthenticatedError()
    try:
        claims = tokens.decode_access(raw)
    except InvalidTokenError:
        raise NotAuthenticatedError() from None
    # The role and the active flag are read fresh, so removing access takes effect now.
    profile = users.find_by_id(claims.user_id)
    if profile is None or not profile.is_active:
        raise NotAuthenticatedError()
    return CurrentUser(
        id=profile.id,
        role=profile.role,
        permissions=permissions_for(profile.role),
        mfa_verified=claims.mfa,
    )


def require_permission(permission: Permission) -> Callable[..., CurrentUser]:
    def check(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if user.role in MFA_REQUIRED_ROLES and not user.mfa_verified:
            raise MfaRequiredError()
        if permission not in user.permissions:
            raise ForbiddenError()
        return user

    return check


def csrf_protect(request: Request) -> None:
    """Double-submit check: the header must repeat the cookie. A page on another site
    cannot read our cookie, so it cannot fill in the header."""
    if request.headers.get("authorization"):
        return  # a header token is not sent automatically by browsers
    cookie = request.cookies.get(CSRF_COOKIE)
    header = request.headers.get(CSRF_HEADER)
    if not cookie or not header or not secrets.compare_digest(cookie, header):
        raise InvalidCsrfError()
