from contextlib import asynccontextmanager
from pathlib import Path

import core.session as session
from aiohttp import ClientSession
from api.v1 import bookmarks, likes, ratings, reviews, heartbeat
from beanie import init_beanie
from core.config import MONGODB_CONFIG, PROJECT_NAME
from commons.token_checker import get_user_from_auth_service
from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from models import beanie_models as bm
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server...")
    session.aiohttp_session = ClientSession()
    client = AsyncIOMotorClient(
        "mongodb://{user}:{password}@{host}:{port}".format(**MONGODB_CONFIG),
    )
    await init_beanie(
        database=client.db_name,
        document_models=[bm.Bookmark, bm.Rating, bm.Like, bm.Review],
    )
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None
    client.close()


BASE_DIR = Path(__file__).resolve().parent
logger.remove()
logger.add(
    BASE_DIR / "nx_ugc.log",
    level="INFO",
    format="{message}",
    serialize=True,
)

app = FastAPI(
    title=PROJECT_NAME,
    description="Сервис обработки запрос, связанных с контентом, созданным пользователями.",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# routing
api_router_main = APIRouter(
    prefix="/ugc-service", dependencies=[Depends(get_user_from_auth_service)]
)

api_router_v1 = APIRouter(prefix="/api/v1")

api_router_v1.include_router(ratings.router, prefix="/rating", tags=["rating"])
api_router_v1.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router_v1.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router_v1.include_router(reviews.router, prefix="/reviews", tags=["reviews"])

api_router_main.include_router(api_router_v1)

app.include_router(api_router_main)
app.include_router(heartbeat.router, prefix="/lifecheck")
