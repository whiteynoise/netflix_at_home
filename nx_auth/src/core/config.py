import os

from .settings import NXAuthSettings

settings = NXAuthSettings()

PROJECT_NAME: str = "nx_auth"

PG_CONFIG = {
    "db": settings.postgres_db,
    "user": settings.postgres_user,
    "password": settings.postgres_password,
    "host": settings.postgres_host,
    "port": settings.postgres_port,
}

REDIS_CONFIG = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

JAEGER_CONFIG = {"host": settings.jaeger_host, "port": settings.jaeger_port}

ENABLE_TRACER = settings.enable_tracer

PROVIDERS_URL: dict[str, str] = {
    "yandex": "https://login.yandex.ru/info?format=json",
}

YNDX_AUTH_URL: str = "https://login.yandex.ru/info?format=json"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
