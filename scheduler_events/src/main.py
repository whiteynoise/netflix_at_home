from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI

import session
from models.response import CreateEventSchema
from sheduler import schedule_event, start_scheduler

app = FastAPI(docs_url="/api/openapi")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    start_scheduler()
    session.aiohttp_session = ClientSession()
    yield
    await session.aiohttp_session.close()
    session.aiohttp_session = None


@app.post("/create_deferred_event", status_code=201)
async def create_deferred_event(event: CreateEventSchema):
    """Создание события"""
    schedule_event(event)
    return {"detail": "Событие запланировано"}
