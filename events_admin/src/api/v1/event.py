from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException
from loguru import logger

from config import session

from api.v1.constants import (
    SINGLE_NOTIFICATION_SERVICE_API,
    MASSIVE_NOTIFICATION_SERVICE_API,
    VolumeEventType,
    TimeEventType
)

from models.response import CreateEventSchema

router = APIRouter(tags=["События"])

@router.post("/create_event", summary="Отправить событие", status_code=201)
async def create_event(event: Annotated[CreateEventSchema, Body(...)]) -> None:
    logger.info({"message": f"Направлено событие {event.model_dump()}"})

    # смотрим в какой сервис отправить
    match event.volume_type:
        case VolumeEventType.SINGLE.value:
            url = SINGLE_NOTIFICATION_SERVICE_API
        case VolumeEventType.MASSIVE.value:
            url = MASSIVE_NOTIFICATION_SERVICE_API
        case _:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Невалидный тип",
            )

    # смотрим отправить ли сразу на апи или в шедулер
    match event.time_type:
        case TimeEventType.INSTANT.value:
            async with session.aiohttp_session.post(url, json=event.model_dump()) as response:
                if response.status not in (200, 201):
                    raise HTTPException(
                        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                        detail="Ошибка отправки!",
                    )
        case TimeEventType.DEFERRED.value:
            pass # отправить в шелудер
