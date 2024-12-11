from pydantic_settings import BaseSettings


class NXAuthSettings(BaseSettings):

    project_name: str

    user: str
    password: str

    host: str
    port: str
    db: str
