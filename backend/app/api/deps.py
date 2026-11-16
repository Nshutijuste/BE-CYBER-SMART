from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import Argon2PasswordHasher
from app.db.session import get_db
from app.domain.interfaces import PasswordHasher
from app.repositories.login_attempt_repository import SqlLoginAttemptRepository
from app.repositories.user_repository import SqlUserRepository
from app.services.auth_service import AuthService
from app.services.login_service import LoginService


def get_password_hasher() -> PasswordHasher:
    return Argon2PasswordHasher()


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> AuthService:
    return AuthService(SqlUserRepository(db), hasher)


def get_login_service(
    db: Annotated[Session, Depends(get_db)],
    hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> LoginService:
    return LoginService(SqlUserRepository(db), SqlLoginAttemptRepository(db), hasher)