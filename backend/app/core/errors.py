import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for errors we raise on purpose."""

    status_code = 400
    code = "app_error"
    message = "The request could not be completed."
    headers: dict[str, str] | None = None

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    message = "Not found."


class ConflictError(AppError):
    status_code = 409
    code = "account_unavailable"
    message = "These details cannot be used to register."


class MfaAlreadyEnabledError(ConflictError):
    code = "mfa_already_enabled"
    message = "Two-step login is already on."


class WeakPasswordError(AppError):
    status_code = 422
    code = "weak_password"
    message = "This password appears in known data leaks. Please choose another."


class AuthenticationError(AppError):
    status_code = 401
    code = "invalid_credentials"
    message = "Incorrect details. Please try again."


class NotAuthenticatedError(AppError):
    status_code = 401
    code = "not_authenticated"
    message = "Please log in."


class InvalidSessionError(AppError):
    status_code = 401
    code = "session_invalid"
    message = "Your session has ended. Please log in again."


class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"
    message = "You do not have permission to do that."


class MfaRequiredError(ForbiddenError):
    code = "mfa_required"
    message = "A second step is required for this account."


class InvalidCsrfError(ForbiddenError):
    code = "csrf_failed"
    message = "The request could not be verified."


class TooManyAttemptsError(AppError):
    status_code = 429
    code = "too_many_attempts"
    message = "Too many attempts. Please wait and try again."

    def __init__(self, retry_after: int) -> None:
        super().__init__()
        self.retry_after = retry_after
        self.headers = {"Retry-After": str(retry_after)}


def _body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_body(exc.code, exc.message),
        headers=exc.headers,
    )


async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content=_body("invalid_input", "Some input is invalid."))


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=_body("server_error", "Something went wrong. Please try again."),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, handle_app_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(Exception, handle_unexpected_error)
