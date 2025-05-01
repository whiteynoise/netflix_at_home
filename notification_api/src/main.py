from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.v1 import notification
from config.rabbit import rmq_config
from db import producer
from mq.producer import RabbitMqProducer

BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "notification_api.log",
    level="INFO",
    format="{message}",
    serialize=True,
)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    producer.rmq_producer = RabbitMqProducer(config=rmq_config)
    await producer.rmq_producer.connect()
    yield
    await producer.rmq_producer.close()


app = FastAPI(
    title="Апи нотификации",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(notification.router)

app.include_router(api_router_v1)
