from pydantic_settings import BaseSettings


class NXAuthSettings(BaseSettings):

    project_name: str

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int