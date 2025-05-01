from contextlib import asynccontextmanager
from pathlib import Path

from aiohttp import ClientSession
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from loguru import logger

from api.v1 import template
from config import session

BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "event_admin.log",
    level="INFO",
    format="{message}",
    serialize=True,
)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    session.aiohttp_session = ClientSession()
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None


app = FastAPI(
    title="Административная панель событий",
    description="Административный сервис взаимодействия с событиями для отправки на почту юзеров.",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(template.router)

app.include_router(api_router_v1)
