import uuid
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, model_validator

CODE_PATTERN = r"^\d{6}$"


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\+[1-9]\d{7,14}$")
    password: SecretStr = Field(min_length=12, max_length=128)

    @model_validator(mode="after")
    def need_email_or_phone(self) -> Self:
        if self.email is None and self.phone is None:
            raise ValueError("email or phone is required")
        return self


class RegisterResponse(BaseModel):
    id: uuid.UUID


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\+[1-9]\d{7,14}$")
    password: SecretStr = Field(min_length=1, max_length=128)

    @model_validator(mode="after")
    def need_exactly_one_identifier(self) -> Self:
        if (self.email is None) == (self.phone is None):
            raise ValueError("send either email or phone")
        return self


class LoginResponse(BaseModel):
    status: Literal["ok", "mfa_required"]
    mfa_token: str | None = None


class MfaLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mfa_token: str = Field(min_length=1, max_length=2000)
    code: str = Field(pattern=CODE_PATTERN)


class MfaCodeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str = Field(pattern=CODE_PATTERN)


class MfaSetupResponse(BaseModel):
    secret: str
    otpauth_uri: str


class StatusResponse(BaseModel):
    status: Literal["ok"] = "ok"


class MeResponse(BaseModel):
    id: uuid.UUID
    role: str
    permissions: list[str]
    mfa_verified: bool
