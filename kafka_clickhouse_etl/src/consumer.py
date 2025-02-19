import os

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    os.getenv("TOPIC"),
    bootstrap_servers=['kafka-0:9092'],
    auto_offset_reset='earliest',
    group_id=os.getenv("GROUP_ID"),
)

