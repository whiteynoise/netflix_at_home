from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="POSTGRES_", extra="ignore")


pg_config = PostgresConfig()
