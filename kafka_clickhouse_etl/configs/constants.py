import os

TOPIC = os.getenv("TOPIC")
BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS").split(",")
GROUP_ID = os.getenv("GROUP_ID")
CLICKHOUSE_NODE_MAIN = os.getenv("CLICKHOUSE_NODE_MAIN")
