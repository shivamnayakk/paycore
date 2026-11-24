from functools import lru_cache
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration loaded from environment variables and .env file.
    Follows 12-factor app principles for cloud-native deployment.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application Info
    PROJECT_NAME: str = "PayCore"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Server Binding
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database URL
    # Defaults to async SQLite for local testing without external setup.
    # In Docker/Production, set to postgresql+asyncpg://user:pass@host:5432/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./paycore.db"

    # Security
    SECRET_KEY: str = "default-insecure-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Mock Gateway Settings
    MOCK_GATEWAY_SUCCESS_RATE: float = 0.90
    MOCK_GATEWAY_LATENCY_MS: int = 200

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    Using lru_cache prevents reading the disk/.env file repeatedly on every request.
    """
    return Settings()


settings = get_settings()
