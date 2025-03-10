import logging

import logstash

import core.session as session
from aiohttp import ClientSession
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from loguru import logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from api.v1 import auth, managment, token
from core.config import PROJECT_NAME, REDIS_CONFIG, JAEGER_CONFIG, ENABLE_TRACER
from core.tracer import configure_tracer
from db.const import constants
from redis.asyncio import Redis
from db import redis
from services.middleware import RateLimitMiddleware, RequestIdMiddleware

logger.remove()
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
