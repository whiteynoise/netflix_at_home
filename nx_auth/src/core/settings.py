from pydantic_settings import BaseSettings, SettingsConfigDict


class NXAuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    redis_port: str
    redis_host: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    jaeger_host: str
    jaeger_port: int

    dev_auth_mode: bool
    