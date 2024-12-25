import os
from .settings import NXAuthSettings

settings = NXAuthSettings()

PROJECT_NAME: str = 'nx_auth'

PG_CONFIG = {
    "db": settings.postgres_db,
    "user": settings.postgres_user,
    "password": settings.postgres_password,
    "host": settings.postgres_host,
    "port": settings.postgres_port,
}

REDIS_CONFIG = {
    'host': settings.redis_host,
    'port': settings.redis_port,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
