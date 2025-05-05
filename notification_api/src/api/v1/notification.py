from http import HTTPStatus
from typing import Annotated
from queries import notification as sql

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from db.producer import get_rmq_producer
from models.response import EventCreate

from models.entity import Event
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from mq.producer import RabbitMqProducer
from service.notification import msg_generation

router = APIRouter(tags=["Нотификация"])


@router.post("/create_notification", summary="Создание события", status_code=201)
async def create_event(
        event: EventCreate,
        db: Annotated[AsyncSession, Depends(get_session)],
        rmq: Annotated[RabbitMqProducer, Depends(get_rmq_producer)],
) -> None:
    """Создание события и отправка в очередь"""
    template_name = None

    if event.template_id:
        template_path = (
            await db.execute(
                sql.get_template_by_id(),
                {"template_id": event.template_id},
            )
        ).scalar_one_or_none()

        if not template_path:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Шаблон не найден!",
            )
        
        template_name = template_path.split('/')[-1]

    entity_event = Event(**event.model_dump())
    db.add(entity_event)
    await db.commit()

    await msg_generation(
        db=db,
        rmq=rmq,
        event=event,
        template_name=template_name,
    )

    logger.info({"message": f"Event {event.model_dump()} created"})

    return None
