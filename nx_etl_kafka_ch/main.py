import sentry_sdk
from time import sleep

from configs.constants import settings
from configs.logger_config import logger
from utils.waiters import clickhouse_client_create, kafka_consumer_create
from related.ch_loader import ClickHouseLoader
from related.kafka_extractor import KafkaExtractor
from utils.ch_queries import queries_by_topic


def start_etl_process():
    sleep_time_etl: int = 600
    query: str = queries_by_topic.get(settings.TOPIC)
    consumer = kafka_consumer_create()

    extractor: KafkaExtractor = KafkaExtractor(consumer=consumer)
    loader: ClickHouseLoader = ClickHouseLoader(client=clickhouse_client_create())

    while True:
        logger.info("Collecting data from Kafka...")

        for batch in extractor.extract():
            logger.info("Loading data to ClickHouse...")
            loader.load_data(batch=batch, query=query)
            consumer.commit()

        logger.info("Data loaded. I'm going to sleep for %s seconds.", sleep_time_etl)
        sleep(sleep_time_etl)


if __name__ == "__main__":
    sentry_sdk.init(settings.SENTRY_DSN)
    logger.info("ETL process starting...")
    start_etl_process()
