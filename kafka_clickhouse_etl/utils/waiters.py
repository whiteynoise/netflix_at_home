from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError, SocketTimeoutError
from kafka import KafkaConsumer

import backoff
from kafka.errors import NoBrokersAvailable

from configs.constants import settings


@backoff.on_exception(backoff.expo, max_tries=10, exception=NoBrokersAvailable)
def kafka_consumer_create():
    consumer = KafkaConsumer(
        settings.TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id=settings.GROUP_ID,
        enable_auto_commit=False
    )
    return consumer


@backoff.on_exception(
    backoff.expo,
    max_tries=10,
    exception=(
        NetworkError,
        SocketTimeoutError,
    ),
)
def clickhouse_client_create():
    client = Client(host=settings.CLICKHOUSE_NODE_MAIN)
    return client
