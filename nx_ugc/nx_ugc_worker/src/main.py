import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from abstracts import AbstractConsumer, AbstractWorker
from base_worker import BaseWorker
from commons.models.beanie_models import Bookmark, Rating, Like, Review
from commons.shared_config import MONGODB_CONFIG, SERVICE_INFO_BY_TOPIC
from configs.settings import settings
from consumers.kafka_consumer import KafkaConsumer


def get_consumer() -> AbstractConsumer:
    """Хендлер получения консьюмера."""
    return KafkaConsumer(
        topic=settings.TOPIC,
        group_id=settings.GROUP_ID,
        bootstrap_servers=settings.BOOTSTRAP_SERVERS,
    )


def get_worker() -> AbstractWorker:
    """Хендлер создания воркера."""
    if not (service_info := SERVICE_INFO_BY_TOPIC.get(settings.TOPIC)):
        raise ValueError("Unknown service.")
    
    return BaseWorker(**service_info)


@asynccontextmanager
async def db_connection_handler() -> AsyncGenerator[None, None]:
    """Хендлер коннекта к БД."""
    client = AsyncIOMotorClient(
        "mongodb://{user}:{password}@{host}:{port}".format(**MONGODB_CONFIG),
    )
    await init_beanie(
        database=client.db_name,
        document_models=[Bookmark, Rating, Like, Review],
    )
    try:
        yield
    finally:
        client.close()


async def main() -> None:
    async with db_connection_handler():
        async with get_consumer() as consumer:
            await consumer.start_consumption(
                callback=get_worker(),
            )


if __name__ == "__main__":
    asyncio.run(main())
