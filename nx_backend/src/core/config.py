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

PROJECT_NAME = settings.project_name

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
