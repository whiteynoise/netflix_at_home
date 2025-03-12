from contextlib import asynccontextmanager

import core.session as session
import logstash
from aiohttp import ClientSession
from api.v1 import auth, managment, token
from core.config import (ENABLE_TRACER, JAEGER_CONFIG, PROJECT_NAME,
                         REDIS_CONFIG)
from core.tracer import configure_tracer
from db import redis
from db.const import constants
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from services.middleware import RateLimitMiddleware, RequestIdMiddleware


DEFAULT_TAG = 'nx_auth'


def add_tag(record):
    """Добавляет tag в каждый логт"""
    record['extra'].setdefault('tag', DEFAULT_TAG)


logger.remove()

logger = logger.patch(add_tag)
logger.add(
    logstash.TCPLogstashHandler("logstash", 5044, version=1),
    serialize=True,
    level="INFO",
)

logger.add(
    "info.log", format="Log: [{time} - {level} - {message}]", level="INFO", enqueue=True
)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    session.aiohttp_session = ClientSession()
    logger.info("Loading constants...")
    redis.redis = Redis(**REDIS_CONFIG)
    await constants.initialize()
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None


app = FastAPI(
    version="0.0.1",
    title=PROJECT_NAME,
    description="Сервис авторизации",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# routing
api_router_main = APIRouter(prefix="/auth-service")

api_router_v1 = APIRouter(prefix="/api/v1")

api_router_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router_v1.include_router(managment.router, prefix="/managment", tags=["managment"])
api_router_v1.include_router(token.router, prefix="/token", tags=["token"])

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)


# middlewares
app.add_middleware(RateLimitMiddleware, redis_=Redis(**REDIS_CONFIG))

if ENABLE_TRACER:
    configure_tracer(config=JAEGER_CONFIG)
    FastAPIInstrumentor.instrument_app(app)

    app.add_middleware(RequestIdMiddleware)
