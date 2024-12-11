from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from core.config import PROJECT_NAME

logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue=True)


app = FastAPI(
    title=PROJECT_NAME,
    description='Сервис авторизации',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app = FastAPI(version='0.0.1')