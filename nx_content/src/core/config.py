import os
from logging import config as logging_config

from core.logger import LOGGING
from models.settings_model import NXBackendEnvSettings


settings = NXBackendEnvSettings()

REDIS_CONFIG = {
    'host': settings.redis_host,
    'port': settings.redis_port,
}

ES_CONFIG = {
    'host': settings.elastic_host,
    'port': settings.elastic_port,
}

AUTH_SERVICE_URL = settings.auth_service_url

PROJECT_NAME: str = 'nx_backend'

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
