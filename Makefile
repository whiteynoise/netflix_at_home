up_kafka_clickhouse_ugc:
	docker-compose -f docker-compose.kafka.yaml -f docker-compose.clickhouse.yaml -f docker-compose.yaml -f docker-compose.override.yaml up -d --build ugc kafka-init clickhouse-node4
down_kafka_clickhouse_ugc:
	docker-compose -f docker-compose.kafka.yaml -f docker-compose.clickhouse.yaml -f docker-compose.yaml -f docker-compose.override.yaml down -v


up_elk:
	docker-compose -f docker-compose.elk.yaml -f docker-compose.yaml -f docker-compose.override.yaml up -d --build nx_ugc nx_backend kibana

down_elk:
	docker-compose -f docker-compose.elk.yaml -f docker-compose.yaml -f docker-compose.override.yaml down -v

restart_elk:
	docker-compose -f docker-compose.elk.yaml -f docker-compose.yaml -f docker-compose.override.yaml restart

restart_kinaba:
	docker-compose -f docker-compose.elk.yaml -f docker-compose.yaml -f docker-compose.override.yaml restart kibana
