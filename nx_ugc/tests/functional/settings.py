from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    auth_service_url: str

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int


test_settings = TestSettings()

PG_CONFIG = {
    "db": test_settings.postgres_db,
    "user": test_settings.postgres_user,
    "password": test_settings.postgres_password,
    "host": test_settings.postgres_host,
    "port": test_settings.postgres_port,
}

MONGODB_CONFIG = {
    "user": test_settings.mongo_user,
    "password": test_settings.mongo_password,
    "host": test_settings.mongo_host,
    "port": test_settings.mongo_port,
}

dsn = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(**PG_CONFIG)

URL_APP = 'http://app:8005/ugc-service/'
