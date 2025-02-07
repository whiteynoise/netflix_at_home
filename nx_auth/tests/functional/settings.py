from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    redis_host: str
    redis_port: int
    url_app: str

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int


test_settings = TestSettings()

REDIS_CONFIG = {
    'host': test_settings.redis_host,
    'port': test_settings.redis_port,
}

PG_CONFIG = {
    "db": test_settings.postgres_db,
    "user": test_settings.postgres_user,
    "password": test_settings.postgres_password,
    "host": test_settings.postgres_host,
    "port": test_settings.postgres_port,
}

dsn = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(**PG_CONFIG)

URL_APP = test_settings.url_app
