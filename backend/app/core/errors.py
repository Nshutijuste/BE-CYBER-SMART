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

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    message = "Not found."


def _body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=_body(exc.code, exc.message))


async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Never echo the user's input back: it may contain a password.
    return JSONResponse(status_code=422, content=_body("invalid_input", "Some input is invalid."))


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    # Full detail goes to the log only, never to the user.
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=_body("server_error", "Something went wrong. Please try again."),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, handle_app_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(Exception, handle_unexpected_error)
    