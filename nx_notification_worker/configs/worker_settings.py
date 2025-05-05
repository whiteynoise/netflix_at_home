from pydantic_settings import BaseSettings, SettingsConfigDict


class StartSettings(BaseSettings):
    consumer_type: str = 'rmq'
    worker_type: str = 'mail'

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RabbitMQConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    exchange: str
    routing_key: str
    queue_name: str

    model_config = SettingsConfigDict(env_prefix="RMQ_", extra="ignore")


rabbit_mq_config = RabbitMQConfig()
start_settings = StartSettings()
