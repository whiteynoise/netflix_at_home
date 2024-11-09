up:
	docker-compose up -d

down:
	docker-compose down

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
