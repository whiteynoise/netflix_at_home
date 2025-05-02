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

router = APIRouter(tags=["Нотификация"])


@router.post("/create_notification", summary="Создание события", status_code=201)
async def create_event(
        event: EventCreate,
        db: Annotated[AsyncSession, Depends(get_session)],
        rmq: Annotated[RabbitMqProducer, Depends(get_rmq_producer)],
) -> None:
    """Создание события и отправка в очередь"""

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

    entity_event = Event(**event.model_dump())
    db.add(entity_event)
    await db.commit()

    await msg_generation(
        db=db,
        rmq=rmq,
        event=event,
        template_name=template_path.split('/')[-1],
    )

    logger.info({"message": f"Event {event.model_dump()} created"})

    return None


async def msg_generation(
        db: AsyncSession,
        rmq: RabbitMqProducer,
        event: EventCreate,
        template_name: str,
) -> None:
    """Хендлер подготовки и публикации сообщений в брокер."""
    async for batch in stream_db_user_data(db=db, batch_size=1000, event=event):
        await send_to_rmq(
            rmq=rmq,
            batch=batch,
            event=event,
            template_name=template_name,
        )


async def stream_db_user_data(db: AsyncSession, batch_size: int, event: EventCreate):
    """Получение пользовательских данных с базы."""
    batch = []

    query = sql.users_by_roles() if event.volume_type == 'massive' else sql.users_by_user_id()

    async for row in db.stream(query, {'roles': event.roles, 'user_id': event.user_id}):
        batch.append(dict(row))
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    if batch:
        yield batch


async def send_to_rmq(
        rmq: RabbitMqProducer,
        batch: list[dict],
        event: EventCreate,
        template_name: str,
) -> None:
    """Публикация сообщений в брокер."""
    for row in batch:
        await rmq.publish(
            {
                "subject": event.title,
                "email": row['email'],
                "template_name": template_name,
                "render_params": {
                    "username": row['username'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                },
                "user_id": event.user_id,
            }
        )
