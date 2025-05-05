from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLAlchemyConfig(BaseSettings):
    echo: bool = False
    model_config = SettingsConfigDict(env_prefix="SQLALCHEMY_", extra="ignore")


sqlalchemy_config = SQLAlchemyConfig().model_dump()
