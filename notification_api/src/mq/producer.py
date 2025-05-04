import aio_pika
import json

from loguru import logger

from config.rabbit import RabbitMQConfig


class RabbitMqProducer:
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.queue_name: str | None = None
        self.channel: aio_pika.RobustChannel | None = None

    async def connect(self):
        self.connection: aio_pika.abc.AbstractRobustConnection = (
            await aio_pika.connect_robust(
                host=self.config.host,
                port=int(self.config.port),
                login=self.config.user,
                password=self.config.password,
            )
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.config.queue_name, durable=True)

    async def publish(self, message: dict):
        if self.channel is None:
            logger.info({"message": "Reopen channel."})
            self.channel = await self.connection.channel()

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self.config.queue_name,
        )
        logger.info("Publish successfull!")

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
