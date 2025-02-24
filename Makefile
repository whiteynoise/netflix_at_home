up all:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml -f docker-compose.kafka.yaml
	-f docker-compose.clickhouse.yaml up -d

up kafka_&_ugc:
    docker-compose -f docker-compose.kafka.yaml -f docker-compose.yaml ugc up -d

up clickhouse:
    docker-compose -f docker-compose.clickhouse.yaml up -d

up kafka_&_clickhouse_&_ugc:
    docker-compose -f docker-compose.kafka.yaml docker-compose -f docker-compose.kafka.yaml
    -f docker-compose.yaml ugc up -d