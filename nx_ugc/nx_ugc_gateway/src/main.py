from contextlib import asynccontextmanager
from pathlib import Path

import core.session as session
from aiohttp import ClientSession
from commons.token_checker import get_user_from_auth_service
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.v1 import gateway
from producer import kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server...")
    session.aiohttp_session = ClientSession()
    await kafka_producer.start()
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None
    await kafka_producer.stop()


BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "nx_ugc.log",
    level="INFO",
    format="{message}",
    serialize=True,
)

app = FastAPI(
    title="ugc_gateway",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# routing
api_router_main = APIRouter(
    prefix="/ugc-gateway", dependencies=[Depends(get_user_from_auth_service)]
)

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(gateway.router)

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)
