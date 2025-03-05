import core.session as session
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films, genres, persons
from db import elastic, redis

from core.config import REDIS_CONFIG, ES_CONFIG, PROJECT_NAME
from core.token import get_user_from_auth_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup connections to es and redis on startup
    session.aiohttp_session = ClientSession()
    redis.redis = Redis(**REDIS_CONFIG)
    elastic.es = AsyncElasticsearch(hosts=['{host}:{port}'.format(**ES_CONFIG)])
    yield
    # close connections to es and redis on shutdown
    await session.aiohttp_session.close()
    session.aiohttp_session = None
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=PROJECT_NAME,
    description='Информация о фильмах, жанрах и людях, участвовавших в создании произведения',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


# routing
api_router_main = APIRouter(
    prefix='/content-service',
    dependencies=[Depends(get_user_from_auth_service)]
)

api_router_v1 = APIRouter(prefix='/api/v1')

api_router_v1.include_router(films.router, prefix='/films', tags=['films'])
api_router_v1.include_router(genres.router, prefix='/genres', tags=['genres'])
api_router_v1.include_router(persons.router, prefix='/persons', tags=['persons'])

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)
