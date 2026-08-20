from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import API_V1_PREFIX, SERVICE_NAME


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = SERVICE_NAME
    app_description: str = (
        "AI-powered incident root-cause-analysis (RCA) service"
    )
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    api_v1_prefix: str = API_V1_PREFIX
    log_level: str = "INFO"
    cors_origins: list[str] = ["*"]
    anthropic_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
