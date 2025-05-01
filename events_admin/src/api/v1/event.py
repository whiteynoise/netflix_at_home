from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException
from loguru import logger

from config import session

from api.v1.constants import (
    REGULAR_NOTIFICATION_SERVICE_API,
    INSTANCE_NOTIFICATION_SERVICE_API,
    EventType,
)

from models.response import CreateEventSchema

router = APIRouter(tags=["События"])

@router.post("/create_event", summary="Отправить событие", status_code=201)
async def create_event(event: Annotated[CreateEventSchema, Body(...)]) -> None:
    logger.info({"message": f"Направлено событие {event.model_dump()}"})

    match event.type:
        case EventType.INSTANCE.value:
            url = INSTANCE_NOTIFICATION_SERVICE_API
        case EventType.REGULAR.value:
            url = REGULAR_NOTIFICATION_SERVICE_API
        case _:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Невалидный тип",
            )

    async with session.aiohttp_session.post(url, json=event.model_dump(mode='json')) as response:
        if response.status not in (200, 201):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Create event: error",
            )
