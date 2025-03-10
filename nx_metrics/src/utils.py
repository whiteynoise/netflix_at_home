import json
from typing import Any

from producer import producer


def send_to_kafka(topic: str, message: Any) -> None:
    """Отправка сообщений в кафку
    Партиционирование round-robin

    :param topic: Топик film или user
    :param message: Сообщение в кафку
    """
    producer.send(
        topic=topic,
        value=json.dumps(message).encode("utf-8"),
    )
