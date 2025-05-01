from typing import Annotated

from fastapi import APIRouter, Depends
from loguru import logger

from db.producer import get_rmq_producer
from models.constants import EventType
from models.response import EventCreate

from models.entity import Event
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from mq.producer import RabbitMqProducer

router = APIRouter(tags=["Нотификация"])


@router.post("/create_notification", summary="Создание события", status_code=201)
async def create_event(
    event: EventCreate,
    db: Annotated[AsyncSession, Depends(get_session)],
    rmq: Annotated[RabbitMqProducer, Depends(get_rmq_producer)],
) -> None:
    entity_event = Event(**event.dict())
    db.add(entity_event)
    await db.commit()
    logger.info({"message": f"Event {event.dict()} created"})
    match event.type:
        case EventType.INSTANCE.value:
            await rmq.publish({"template_id": event.template_id, "roles": event.roles})
            pass
        case EventType.REGULAR.value:
            pass
    return

