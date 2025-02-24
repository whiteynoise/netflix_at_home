up_kafka_clickhouse_ugc:
	docker-compose -f docker-compose.kafka.yaml -f docker-compose.clickhouse.yaml -f docker-compose.yaml -f docker-compose.override.yaml up -d --build ugc kafka-init clickhouse-node4
down_kafka_clickhouse_ugc:
	docker-compose -f docker-compose.kafka.yaml -f docker-compose.clickhouse.yaml -f docker-compose.yaml -f docker-compose.override.yaml down -v