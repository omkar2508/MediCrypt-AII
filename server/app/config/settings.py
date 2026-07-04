from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Medicrypt AI Server"
    environment: str = "development"
    database_url: str = "sqlite:///./medicrypt.db"
    enable_audit_logging: bool = True
    allowed_origins: str = "http://localhost:8000"
    cors_max_age: int = 600
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    jwt_secret_key: str = "development-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 43200

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
