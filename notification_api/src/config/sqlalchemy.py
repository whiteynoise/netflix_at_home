from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLAlchemyConfig(BaseSettings):
    echo: str = False
    model_config = SettingsConfigDict(env_prefix="SQLALCHEMY_", extra="ignore")


sqlalchemy_config = SQLAlchemyConfig()
