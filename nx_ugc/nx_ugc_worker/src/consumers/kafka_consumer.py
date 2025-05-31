import orjson

from loguru import logger
from typing import Callable, Awaitable
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from abstracts import AbstractConsumer


class KafkaConsumer(AbstractConsumer):
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        group_id: str,
    ):
        self.topic = topic
        self.dlq_topic = f'{topic}_dlq'
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self._consumer: AIOKafkaConsumer | None = None
        self._dlq_producer: AIOKafkaProducer | None = None

    async def __aenter__(self):
        await self._start_consumer()
        await self._start_dlq_prod()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._consumer.stop()
        logger.info('Kafka consumer stopped')

        await self._dlq_producer.stop()
        logger.info('Kafka producer (DLQ) stopped')

    async def _start_consumer(self):
        """Запуск консьюмера топика."""

        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda _: orjson.loads(_),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        await self._consumer.start()

        logger.info(f'Kafka consumer started to read topic: {self.topic}')

    async def _start_dlq_prod(self):
        """Запуск продюсера для DLQ топика."""

        self._dlq_producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda _: orjson.dumps(_),
        )
        await self._dlq_producer.start()

        logger.info(f'Kafka producer started for DLQ (topic: {self.dlq_topic})')

    async def start_consumption(
            self,
            callback: Callable[[dict], Awaitable[None]],
    ) -> None:
        """Точка входа в воркер, запускает потребление сообщений."""

        if not self._consumer:
            await self.setup_connection()

        async for msg in self._consumer:
            try:
                logger.info(f'Received message {msg.value}')
                await callback(msg.value)
            except Exception as e:
                logger.error(f'Failed to process message: {e}')
                await self._send_to_dlq(
                    message=msg,
                    error=str(e),
                )

    async def _send_to_dlq(
            self,
            message: dict,
            error: str,
    ) -> None:
        """Метод отправки сообщений в DLQ."""

        await self._dlq_producer.send_and_wait(
            self.dlq_topic,
            {
                'original_message': message,
                'error': error,
            },
        )
        logger.warning(f'Message sent to DLQ (topic: {self.dlq_topic})')
