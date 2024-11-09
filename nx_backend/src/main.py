from elasticsearch import AsyncElasticsearch
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films
from db import elastic, redis

from core.config import REDIS_CONFIG, ES_CONFIG, PROJECT_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup connections to es and redis on startup
    redis.redis = Redis(**REDIS_CONFIG)
    elastic.es = AsyncElasticsearch(hosts=['{host}:{port}'.format(**ES_CONFIG)])
    yield
    # close connections to es and redis on shutdown
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

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
