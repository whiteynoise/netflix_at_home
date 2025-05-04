from queries import notification as sql
from models.response import EventCreate

from sqlalchemy.ext.asyncio import AsyncSession

from mq.producer import RabbitMqProducer


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
