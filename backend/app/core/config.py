from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

# In these environments cookies may travel over plain http (local work and tests).
PLAIN_HTTP_ENVS = {"development", "test"}


class Settings(BaseSettings):
    app_env: str = "development"
    frontend_origin: str = "http://localhost:3000"
    ollama_url: str = "http://localhost:11434"
    access_token_minutes: int = 15
    refresh_token_days: int = 14

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

    @property
    def cookies_secure(self) -> bool:
        return self.app_env not in PLAIN_HTTP_ENVS


@lru_cache
def get_settings() -> Settings:
    return Settings()
