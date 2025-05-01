from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from db.producer import get_rmq_producer
from models.response import EventCreate
from sqlalchemy import text

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
    """Создание события и отправка в очередь"""

    result = await db.execute(
        text("SELECT path FROM events_admin.template WHERE id = :template_id"),
        {"template_id": event.template_id},
    )
    row = result.fetchone()
    template_path = row[0] if row else None

    if not template_path:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Шаблон не найден!",
        )

    entity_event = Event(**event.dict())
    db.add(entity_event)
    await db.commit()

    logger.info({"message": f"Event {event.dict()} created"})
    await rmq.publish(
        {
            "template_path": template_path,
            "roles": event.roles,
            "user_id": event.user_id,
            "volume_type": event.volume_type,
        }
    )
    return
