from elasticsearch import AsyncElasticsearch
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films
from core import config
from db import elastic, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup connections to es and redis on startup
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])

    yield

    # close connections to es and redis on shutdown
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
