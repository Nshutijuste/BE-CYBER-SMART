from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    """Application settings."""
    app_env: str = "development"
    frontend_origin: str = "http://localhost:3000"
    ollama_url: str = "http://localhost:11434"


    database_url: SecretStr
    jwt_signing_key: SecretStr
    hmac_secret: SecretStr
    field_encryption_key: SecretStr

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url.get_secret_value()
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

@lru_cache
def get_settings() -> Settings:
    return Settings()
