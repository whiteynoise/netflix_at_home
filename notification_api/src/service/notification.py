from queries import notification as sql
from models.response import EventCreate
from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from mq.producer import RabbitMqProducer
from models.notification_model import NotificationMessage


async def msg_generation(
        db: AsyncSession,
        rmq: RabbitMqProducer,
        event: EventCreate,
        template_name: str | None = None,
) -> None:
    """Хендлер подготовки и публикации сообщений в брокер."""
    async for batch in stream_db_user_data(db=db, batch_size=1000, event=event):
        await send_to_rmq(
            rmq=rmq,
            batch=batch,
            event=event,
            template_name=template_name,
        )


async def stream_db_user_data(
        db: AsyncSession,
        batch_size: int,
        event: EventCreate,
) -> AsyncGenerator[list, Any, None]:
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
        template_name: str | None,
) -> None:
    """Публикация сообщений в брокер."""
    for row in batch:
        await rmq.publish(
            NotificationMessage(
                subject=event.title,
                user_id=event.user_id,
                recipient_data=row,
                template_name=template_name,
                msg_text=event.msg_text,
            ).model_dump()
        )
