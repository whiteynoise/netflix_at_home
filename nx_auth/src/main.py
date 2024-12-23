from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.v1 import auth, managment, token
from core.config import PROJECT_NAME
from db.const import constants

logger.add("info.log", format="Log: [{time} - {level} - {message}]", level="INFO", enqueue=True)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Loading constants...")
    await constants.initialize()
    yield


app = FastAPI(
    version='0.0.1',
    title=PROJECT_NAME,
    description='Сервис авторизации',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(managment.router, prefix='/api/v1/managment', tags=['managment'])
app.include_router(token.router, prefix='/api/v1/token', tags=['token'])
