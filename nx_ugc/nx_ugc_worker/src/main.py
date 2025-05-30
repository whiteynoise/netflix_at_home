import asyncio

from consumers.kafka_consumer import KafkaConsumer
from base_worker import BaseWorker
from configs.settings import settings
from commons.models.beanie_models import Bookmark, Rating, Like, Review
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from commons.shared_config import MONGODB_CONFIG, SERVICE_INFO_BY_TOPIC
from contextlib import asynccontextmanager


def get_consumer():
    """Хендлер получения консьюмера."""
    return KafkaConsumer(
        topic=settings.TOPIC,
        group_id=settings.GROUP_ID,
        bootstrap_servers=settings.BOOTSTRAP_SERVERS,
    )


def get_worker():
    """Хендлер создания воркера."""
    if not (service_info := SERVICE_INFO_BY_TOPIC.get(settings.TOPIC)):
        raise ValueError("Unknown service.")
    
    return BaseWorker(**service_info)


@asynccontextmanager
async def db_connection_handler():
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
