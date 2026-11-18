from fastapi import Response

from app.core.config import Settings
from app.services.session_service import IssuedSession

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"
CSRF_COOKIE = "csrf_token"
CSRF_HEADER = "x-csrf-token"
AUTH_PATH = "/api/v1/auth"


def set_session_cookies(response: Response, issued: IssuedSession, settings: Settings) -> None:
    secure = settings.cookies_secure
    response.set_cookie(
        ACCESS_COOKIE,
        issued.access_token,
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )
    # The refresh token only travels to the auth routes, and never from another site.
    response.set_cookie(
        REFRESH_COOKIE,
        issued.refresh_token,
        max_age=settings.refresh_token_days * 86400,
        httponly=True,
        secure=secure,
        samesite="strict",
        path=AUTH_PATH,
    )
    # The page must be able to read this one to copy it into a header (double submit).
    response.set_cookie(
        CSRF_COOKIE,
        issued.csrf_token,
        max_age=settings.refresh_token_days * 86400,
        httponly=False,
        secure=secure,
        samesite="lax",
        path="/",
    )


def clear_session_cookies(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE, path="/")
    response.delete_cookie(REFRESH_COOKIE, path=AUTH_PATH)
    response.delete_cookie(CSRF_COOKIE, path="/")
