from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError, SocketTimeoutError
from kafka import KafkaConsumer

import backoff
from kafka.errors import NoBrokersAvailable

from configs.constants import TOPIC, BOOTSTRAP_SERVERS, GROUP_ID, CLICKHOUSE_NODE_MAIN


@backoff.on_exception(backoff.expo, max_tries=10, exception=NoBrokersAvailable)
def kafka_consumer_create():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id=GROUP_ID,
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
    client = Client(host=CLICKHOUSE_NODE_MAIN)
    return client
