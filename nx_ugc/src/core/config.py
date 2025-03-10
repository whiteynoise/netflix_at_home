import os

from models.settings_model import NXBackendEnvSettings

settings = NXBackendEnvSettings()

REDIS_CONFIG = {
    "host": settings.redis_host,
    "port": settings.redis_port,
}

MONGODB_CONFIG = {
    "user": settings.mongo_user,
    "password": settings.mongo_password,
    "host": settings.mongo_host,
    "port": settings.mongo_port,
}

AUTH_SERVICE_URL = settings.auth_service_url

PROJECT_NAME: str = "nx_ugc"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
