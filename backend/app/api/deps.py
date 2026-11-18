from datetime import timedelta
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.crypto import FieldCipher, KeyedHasher
from app.core.security import Argon2PasswordHasher
from app.core.tokens import TokenService
from app.db.session import get_db
from app.domain.interfaces import (
    BreachChecker,
    DeviceRepository,
    LoginAttemptRepository,
    MfaRepository,
    Notifier,
    PasswordHasher,
    RefreshTokenRepository,
    UserRepository,
)
from app.repositories.device_repository import SqlDeviceRepository
from app.repositories.login_attempt_repository import SqlLoginAttemptRepository
from app.repositories.mfa_repository import SqlMfaRepository
from app.repositories.refresh_token_repository import SqlRefreshTokenRepository
from app.repositories.user_repository import SqlUserRepository
from app.services.auth_service import AuthService
from app.services.breach_check import PwnedPasswordsChecker
from app.services.login_service import LoginService
from app.services.mfa_service import MfaService
from app.services.notifier import LoggingNotifier
from app.services.session_service import SessionService

DbSession = Annotated[Session, Depends(get_db)]


# ---- single shared tools (built once) ----
@lru_cache
def _tokens() -> TokenService:
    settings = get_settings()
    return TokenService(
        settings.jwt_signing_key.get_secret_value(),
        access_lifetime=timedelta(minutes=settings.access_token_minutes),
    )


@lru_cache
def _keyed_hasher() -> KeyedHasher:
    return KeyedHasher(get_settings().hmac_secret.get_secret_value())


@lru_cache
def _cipher() -> FieldCipher:
    return FieldCipher(get_settings().field_encryption_key.get_secret_value())


def get_app_settings() -> Settings:
    return get_settings()


def get_token_service() -> TokenService:
    return _tokens()


def get_keyed_hasher() -> KeyedHasher:
    return _keyed_hasher()


def get_field_cipher() -> FieldCipher:
    return _cipher()


def get_password_hasher() -> PasswordHasher:
    return Argon2PasswordHasher()


def get_breach_checker() -> BreachChecker:
    return PwnedPasswordsChecker()


def get_notifier() -> Notifier:
    return LoggingNotifier()


# ---- storage (tests replace these with in-memory fakes) ----
def get_user_repository(db: DbSession) -> UserRepository:
    return SqlUserRepository(db)


def get_attempt_repository(db: DbSession) -> LoginAttemptRepository:
    return SqlLoginAttemptRepository(db)


def get_refresh_repository(db: DbSession) -> RefreshTokenRepository:
    return SqlRefreshTokenRepository(db)


def get_mfa_repository(db: DbSession) -> MfaRepository:
    return SqlMfaRepository(db)


def get_device_repository(db: DbSession) -> DeviceRepository:
    return SqlDeviceRepository(db)


# ---- services ----
def get_auth_service(
    users: Annotated[UserRepository, Depends(get_user_repository)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    breach: Annotated[BreachChecker, Depends(get_breach_checker)],
) -> AuthService:
    return AuthService(users, hasher, breach)


def get_login_service(
    users: Annotated[UserRepository, Depends(get_user_repository)],
    attempts: Annotated[LoginAttemptRepository, Depends(get_attempt_repository)],
    mfa: Annotated[MfaRepository, Depends(get_mfa_repository)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    keyed: Annotated[KeyedHasher, Depends(get_keyed_hasher)],
) -> LoginService:
    return LoginService(users, attempts, mfa, hasher, keyed)


def get_session_service(
    tokens: Annotated[TokenService, Depends(get_token_service)],
    refresh: Annotated[RefreshTokenRepository, Depends(get_refresh_repository)],
    users: Annotated[UserRepository, Depends(get_user_repository)],
    devices: Annotated[DeviceRepository, Depends(get_device_repository)],
    notifier: Annotated[Notifier, Depends(get_notifier)],
    keyed: Annotated[KeyedHasher, Depends(get_keyed_hasher)],
    settings: Annotated[Settings, Depends(get_app_settings)],
) -> SessionService:
    return SessionService(
        tokens, refresh, users, devices, notifier, keyed, refresh_days=settings.refresh_token_days
    )


def get_mfa_service(
    mfa: Annotated[MfaRepository, Depends(get_mfa_repository)],
    attempts: Annotated[LoginAttemptRepository, Depends(get_attempt_repository)],
    cipher: Annotated[FieldCipher, Depends(get_field_cipher)],
    keyed: Annotated[KeyedHasher, Depends(get_keyed_hasher)],
) -> MfaService:
    return MfaService(mfa, attempts, cipher, keyed)
