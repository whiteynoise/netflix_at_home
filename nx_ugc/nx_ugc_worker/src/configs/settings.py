from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOPIC: str
    BOOTSTRAP_SERVERS: str | List[str]
    GROUP_ID: str

    @field_validator("BOOTSTRAP_SERVERS", mode="before")
    @classmethod
    def convert_bootstrap_servers(cls, value: str):
        return value.split(",")


settings = Settings()
