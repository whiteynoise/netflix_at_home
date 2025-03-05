from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    project_name: str

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int

    url_app: str
 

test_settings = TestSettings()

REDIS_CONFIG = {
    'host': test_settings.redis_host,
    'port': test_settings.redis_port,
}

ES_CONFIG = {
    'host': test_settings.elastic_host,
    'port': test_settings.elastic_port,
}

URL_APP = test_settings.url_app
