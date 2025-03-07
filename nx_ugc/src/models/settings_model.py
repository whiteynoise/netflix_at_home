from pydantic_settings import BaseSettings, SettingsConfigDict


class NXBackendEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    redis_host: str
    redis_port: int

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int

    auth_service_url: str
    