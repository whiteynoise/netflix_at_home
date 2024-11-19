up:
	docker-compose up -d

down:
	docker-compose down

up_prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up

down_prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml down

clear_down:
	docker-compose down -v

build:
	docker-compose up -d --build

restart:
	docker-compose up restart

build_db:
	docker-compose up -d --build database

up_bd:
	docker-compose up -d database
