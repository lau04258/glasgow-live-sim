from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings with safe local defaults."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Glasgow Live Sim"
    environment: str = Field(default="local", validation_alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+psycopg://glasgow:glasgow@localhost:5432/glasgow_live_sim",
        validation_alias="DATABASE_URL",
    )
    analytics_enabled: bool = Field(default=False, validation_alias="ANALYTICS_ENABLED")


@lru_cache
def get_settings() -> Settings:
    return Settings()
