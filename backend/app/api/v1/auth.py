from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.auth_deps import CurrentUser, csrf_protect, get_current_user
from app.api.cookies import REFRESH_COOKIE, clear_session_cookies, set_session_cookies
from app.api.deps import (
    get_app_settings,
    get_auth_service,
    get_login_service,
    get_mfa_service,
    get_session_service,
    get_token_service,
)
from app.core.config import Settings
from app.core.errors import AuthenticationError, InvalidSessionError
from app.core.tokens import InvalidTokenError, TokenService
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MfaCodeRequest,
    MfaLoginRequest,
    MfaSetupResponse,
    RegisterRequest,
    RegisterResponse,
    StatusResponse,
)
from app.services.auth_service import AuthService
from app.services.login_service import LoginService
from app.services.mfa_service import MfaService
from app.services.session_service import SessionService

router = APIRouter(prefix="/auth", tags=["auth"])


def _client(request: Request) -> tuple[str, str | None]:
    source_ip = request.client.host if request.client else "unknown"
    device = request.headers.get("user-agent", "")[:200] or None
    return source_ip, device


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
    response: Response,
    logins: Annotated[LoginService, Depends(get_login_service)],
    sessions: Annotated[SessionService, Depends(get_session_service)],
    tokens: Annotated[TokenService, Depends(get_token_service)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> LoginResponse:
    source_ip, device = _client(request)
    outcome = logins.login(data, source_ip=source_ip, device_summary=device)
    if outcome.needs_mfa:
        # Right password, but a second step is on: no session yet, only a short pass.
        return LoginResponse(
            status="mfa_required", mfa_token=tokens.issue_mfa_challenge(outcome.user_id)
        )
    issued = sessions.start(
        outcome.user_id, mfa_passed=False, source_ip=source_ip, device_summary=device
    )
    set_session_cookies(response, issued, settings)
    return LoginResponse(status="ok")


@router.post("/login/mfa")
def login_with_code(
    data: MfaLoginRequest,
    request: Request,
    response: Response,
    mfa: Annotated[MfaService, Depends(get_mfa_service)],
    sessions: Annotated[SessionService, Depends(get_session_service)],
    tokens: Annotated[TokenService, Depends(get_token_service)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> LoginResponse:
    source_ip, device = _client(request)
    try:
        user_id = tokens.decode_mfa_challenge(data.mfa_token)
    except InvalidTokenError:
        raise AuthenticationError() from None
    mfa.verify_login_code(user_id, data.code, source_ip=source_ip)
    issued = sessions.start(user_id, mfa_passed=True, source_ip=source_ip, device_summary=device)
    set_session_cookies(response, issued, settings)
    return LoginResponse(status="ok")


@router.post("/refresh", dependencies=[Depends(csrf_protect)])
def refresh(
    request: Request,
    response: Response,
    sessions: Annotated[SessionService, Depends(get_session_service)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> StatusResponse:
    raw = request.cookies.get(REFRESH_COOKIE)
    if not raw:
        raise InvalidSessionError()
    set_session_cookies(response, sessions.rotate(raw), settings)
    return StatusResponse()


@router.post("/logout", dependencies=[Depends(csrf_protect)])
def logout(
    request: Request,
    response: Response,
    sessions: Annotated[SessionService, Depends(get_session_service)],
) -> StatusResponse:
    raw = request.cookies.get(REFRESH_COOKIE)
    if raw:
        sessions.end(raw)
    clear_session_cookies(response)
    return StatusResponse()


@router.post("/mfa/setup", dependencies=[Depends(csrf_protect)])
def mfa_setup(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    mfa: Annotated[MfaService, Depends(get_mfa_service)],
) -> MfaSetupResponse:
    setup = mfa.begin_setup(user.id, account_label=str(user.id))
    return MfaSetupResponse(secret=setup.secret, otpauth_uri=setup.otpauth_uri)


@router.post("/mfa/confirm", dependencies=[Depends(csrf_protect)])
def mfa_confirm(
    data: MfaCodeRequest,
    request: Request,
    response: Response,
    user: Annotated[CurrentUser, Depends(get_current_user)],
    mfa: Annotated[MfaService, Depends(get_mfa_service)],
    sessions: Annotated[SessionService, Depends(get_session_service)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> StatusResponse:
    source_ip, device = _client(request)
    mfa.confirm_setup(user.id, data.code, source_ip=source_ip)
    # From now on this session counts as having passed the second step.
    issued = sessions.start(user.id, mfa_passed=True, source_ip=source_ip, device_summary=device)
    set_session_cookies(response, issued, settings)
    return StatusResponse()
