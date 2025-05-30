from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import ORJSONResponse

from config import session
from dependency.user import get_user_from_auth_service
from api.v1 import film_window


@asynccontextmanager
async def lifespan(app: FastAPI):
    session.aiohttp_session = ClientSession()
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/openapi",
    docs_url="/api/docs",
    default_response_class=ORJSONResponse,
)


# routing
api_router_main = APIRouter(
    prefix="/nup", dependencies=[Depends(get_user_from_auth_service)]
)

api_router_main.include_router(film_window.router, prefix="/film_window")


app.include_router(api_router_main)
