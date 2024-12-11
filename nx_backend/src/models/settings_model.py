from pydantic_settings import BaseSettings, SettingsConfigDict


class NXBackendEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int