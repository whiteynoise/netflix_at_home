from pydantic_settings import BaseSettings, SettingsConfigDict


class NXBackendEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    project_name: str = 'movies'

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    elastic_host: str = 'http://127.0.0.1'
    elastic_port: int = 9200
    