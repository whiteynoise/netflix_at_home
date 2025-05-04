import orjson

from aio_pika import connect_robust, RobustConnection, RobustChannel, ExchangeType

from configs.logger_config import logger


class RabbitMQConsumer:
    def __init__(self, broker_config: dict):
        self.broker_config = broker_config
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None

    async def setup_connection(self) -> None:
        """Установка соединения клиента с брокером."""
        self.connection = await connect_robust(
            host=self.broker_config['host'],
            port=int(self.broker_config['port']),
            login=self.broker_config['user'],
            password=self.broker_config['password'],
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=100)

    async def process_message(self, notification_info: dict):
        """Обработка сообщений, переопределяется в наследнике."""
        ...

    async def start_consumption(self) -> None:
        """Запуск приема сообщений консьюмером для обработки."""
        await self.setup_connection()

        queue_name = self.broker_config['queue_name']

        await self.channel.declare_exchange("dlx.exchange", ExchangeType.DIRECT, durable=True)
        dlx_queue = await self.channel.declare_queue("dlx.queue", durable=True)
        await dlx_queue.bind("dlx.exchange", routing_key=f"dlx.{queue_name}")

        queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": "dlx.exchange",
                "x-dead-letter-routing-key": f"dlx.{queue_name}",
            },
        )

        logger.info('Ready to consume messages')

        async with queue.iterator() as iterator:
            async for message in iterator:
                try:
                    async with message.process():
                        await self.process_message(notification_info=orjson.loads(message.body))
                except Exception as e:
                    logger.error("Failed to process message from queue '%s': %s", queue_name, e)
