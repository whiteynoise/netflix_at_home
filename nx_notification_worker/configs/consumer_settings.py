from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    exchange: str
    routing_key: str
    queue_name: str

    model_config = SettingsConfigDict(env_prefix="RMQ_", extra="ignore")


broker_config = RabbitMQConfig()
