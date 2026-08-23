"""Worker settings loaded from the environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the worker process."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str
    environment: str = "development"
    log_level: str = "INFO"


settings = Settings()  # type: ignore[call-arg]
