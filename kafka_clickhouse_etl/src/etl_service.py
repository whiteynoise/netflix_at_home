from kafka import KafkaConsumer


class ETL:

    def __init__(self, consumer: KafkaConsumer, batch_size: int = 10000):
        self.consumer = consumer
        self.batch_size = batch_size

    def extract(self):
        """Собирает сообщение в батч и отдает в transform"""
        print("Start extracting...")
        batch: list = []

        for message in self.consumer:
            batch.append(message)

            if len(batch) >= self.batch_size:
                yield batch
                batch = []

    def transform(self):
        for batch in self.extract():
            print(f'Batch {batch}. Сделай с ним что нибудь')

