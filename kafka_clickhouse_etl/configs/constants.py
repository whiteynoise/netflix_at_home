from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOPIC: str
    BOOTSTRAP_SERVERS: List[str]
    GROUP_ID: str
    CLICKHOUSE_NODE_MAIN: str

    @classmethod
    def create(cls):
        settings = cls()
        settings.BOOTSTRAP_SERVERS = [server.strip() for server in settings.BOOTSTRAP_SERVERS]
        return settings


settings = Settings.create()
