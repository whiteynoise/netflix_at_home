from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.v1 import auth, managment, token
from core.config import PROJECT_NAME

logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue=True)


app = FastAPI(
    version='0.0.1',
    title=PROJECT_NAME,
    description='Сервис авторизации',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(managment.router, prefix='/api/v1/managment', tags=['managment'])
app.include_router(token.router, prefix='/api/v1/token', tags=['token'])