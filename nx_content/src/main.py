from contextlib import asynccontextmanager
from pathlib import Path

from loguru import logger

import core.session as session
from aiohttp import ClientSession
from api.v1 import films, genres, persons, heartbeat
from core.config import ES_CONFIG, PROJECT_NAME, REDIS_CONFIG
from core.token import get_user_from_auth_service
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup connections to es and redis on startup
    logger.info("Start content service!")
    session.aiohttp_session = ClientSession()
    redis.redis = Redis(**REDIS_CONFIG)
    elastic.es = AsyncElasticsearch(hosts=["{host}:{port}".format(**ES_CONFIG)])
    yield
    # close connections to es and redis on shutdown
    await session.aiohttp_session.close()
    session.aiohttp_session = None
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=PROJECT_NAME,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# logger
BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "nx_content.log",
    level="INFO",
    format="{message}",
    serialize=True,
)


# routing
api_router_main = APIRouter(
    prefix="/content-service", dependencies=[Depends(get_user_from_auth_service)]
)

api_router_v1 = APIRouter(prefix="/api/v1")

api_router_v1.include_router(films.router, prefix="/films", tags=["films"])
api_router_v1.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router_v1.include_router(persons.router, prefix="/persons", tags=["persons"])

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)
app.include_router(heartbeat.router)
