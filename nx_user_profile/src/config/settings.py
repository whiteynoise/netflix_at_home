from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class PGSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="nup_postgres_")

    db: str
    user: str
    password: str
    host: str
    port: int


class AuthServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    auth_service_url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="nup_", extra="ignore")

    auth_service_settings: AuthServiceSettings = AuthServiceSettings()
    pg_settings: PGSettings = PGSettings()

    content_url: str


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.model_validate({})
