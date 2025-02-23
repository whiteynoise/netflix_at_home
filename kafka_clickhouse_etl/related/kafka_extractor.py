import json
from datetime import datetime
from kafka import KafkaConsumer


class KafkaExtractor:

    def __init__(self, consumer: KafkaConsumer, batch_size: int = 10000):
        self.consumer = consumer
        self.batch_size = batch_size

    def extract(self):
        """Собирает сообщения из Kafka в батч."""
        batch: list = []

        for message in self.consumer:
            message: dict = self.prepare_data(message)
            batch.append(message)

            if len(batch) >= self.batch_size:
                yield batch
                batch = []

    def prepare_data(self, message: bytes):
        """Конвертирует сообщение в словарь."""
        message: dict = json.loads(message.decode("utf-8"))
        message['event_time'] = datetime.strptime(message['event_time'], "%Y-%m-%d %H:%M:%S")
        
        return message

