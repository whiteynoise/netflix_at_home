import os
from .settings import NXAuthSettings

settings = NXAuthSettings()

PROJECT_NAME = settings.project_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
