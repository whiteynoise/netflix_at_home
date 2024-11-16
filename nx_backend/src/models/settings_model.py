from pydantic_settings import BaseSettings, SettingsConfigDict


class NXBackendEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    project_name: str = 'movies'

    redis_host: str = 'redis'
    redis_port: int = 6379

    elastic_host: str = 'http://elasticsearch'
    elastic_port: int = 9200