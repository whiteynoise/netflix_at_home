from pydantic_settings import BaseSettings, SettingsConfigDict


class PGSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="nup_postgres_")

    db: str
    user: str
    password: str
    host: str
    port: int


pg_settings = PGSettings()

