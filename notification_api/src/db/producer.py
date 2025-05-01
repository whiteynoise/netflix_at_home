from mq.producer import RabbitMqProducer

rmq_producer: RabbitMqProducer | None = None


async def get_rmq_producer() -> RabbitMqProducer:
    """Возвращает соединение с продьюсером rabbitmq"""
    return rmq_producer
