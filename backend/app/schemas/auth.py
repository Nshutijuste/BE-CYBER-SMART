from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, model_validator


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