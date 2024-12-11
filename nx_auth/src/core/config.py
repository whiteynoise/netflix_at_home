import os
from .settings import NXAuthSettings

settings = NXAuthSettings()

REDIS_CONFIG = {
    'host': settings.redis_host,
    'port': settings.redis_port,
}

ES_CONFIG = {
    'host': settings.elastic_host,
    'port': settings.elastic_port,
}

PROJECT_NAME = settings.project_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
