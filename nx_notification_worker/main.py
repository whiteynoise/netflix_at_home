import asyncio

import workers.mail_worker as mail_worker

from consumers.rmq_consumer import RabbitMQConsumer
from configs.smtp_settings import transfer_setup_data
from configs.worker_settings import rabbit_mq_config, start_settings


def create_worker() -> mail_worker.MailWorker:
    """Хендлер создания воркера."""
    if start_settings.consumer_type == 'rmq':
        broker = RabbitMQConsumer(rabbit_mq_config)
    else:
        raise ValueError("Unsupported broker type")

    if start_settings.worker_type == 'mail':
        return mail_worker.MailWorker(
            broker_consumer=broker,
            transfer_setup_data=transfer_setup_data,
        )
    else:
        raise ValueError("Unknown worker type")


async def main() -> None:
    worker = create_worker()
    await worker.start_worker()


if __name__ == "__main__":
    asyncio.run(main())
