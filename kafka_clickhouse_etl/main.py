import os
from time import sleep

from clickhouse_driver import Client
from configs.logger_config import logger
from related.consumer import consumer
from related.ch_loader import ClickHouseLoader
from related.kafka_extractor import KafkaExtractor
from utils.ch_queries import queries_by_topic


def start_etl_process():
    sleep_time_etl: int = 600
    query: str = queries_by_topic.get(os.getenv("TOPIC"))

    extractor: KafkaExtractor = KafkaExtractor(consumer=consumer)
    loader: ClickHouseLoader = ClickHouseLoader(
        client=Client(host='clickhouse-node1')
    )

    while True:
        logger.info("Collecting data from Kafka...")

        for batch in extractor.extract():
            logger.info("Loading data to ClickHouse...")
            loader.load_data(batch=batch, query=query)
        
        logger.info("Data loaded. I'm going to sleep for %s seconds.", sleep_time_etl)
        sleep(sleep_time_etl)


if __name__ == "__main__":
    logger.info("ETL process starting...")
    start_etl_process()
