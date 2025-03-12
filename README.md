# Проект netflix_at_home

## Используемый стэк технологий
<div>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi"/>&nbsp;
    <img src="https://img.shields.io/badge/SqlAlchemy-%2307405e.svg?&style=flat&logo=SqlAlchemy&logoColor=white"alt="SQLAlchemy"/>&nbsp;
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white"/>&nbsp;
    <img src="https://img.shields.io/badge/-Swagger-%23Clojure?style=flat&logo=swagger&logoColor=white"/>&nbsp;
    <img src="https://img.shields.io/badge/Alembic-%23075e.svg?&style=flat&logo=Alembic&logoColor=white"/>&nbsp;
    <img src="https://img.shields.io/badge/Pydantic-%23e75e.svg?&style=flat&logo=Alembic&logoColor=white"/>&nbsp;
    <img src="https://img.shields.io/badge/JWT-black?style=flat&logo=JSON%20web%20tokens"/>&nbsp;
    <img src="https://img.shields.io/badge/PostgreSQL-%23316192.svg?style=flat&logo=postgresql&logoColor=white" title="PostgreSQL" alt="PostgreSQL"/>&nbsp;
</div>

##  Локальный запуск

1) Добавить .env в корень проекта и папки сервисов
```
REDIS_HOST=
REDIS_PORT=

ELASTIC_HOST=http://elasticsearch
ELASTIC_PORT=9200
ELASTIC_HOST_CLEAR=http://elasticsearch

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=database
POSTGRES_PORT=5432

SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_MINUTES=
```
2. Запустить докер: ```docker-compose up -d --build```

---

## Схема решений
![схема](https://github.com/whiteynoise/netflix_at_home/blob/main/schema_.jpg)

## Сервисы

+ ### nx_backend
Сервис отвечающий за хранение и управление фильмами, пользователями и ролями. ```Дока на порту 8000.``` 
Предназначен для работы с основными сущностями. Берет данные из ElasticSearch.
Представляет собой бекенд для работы с клиентом.

+ ### nx_auth
Сервис отвечающий за аунтификацию и авторизацию. ```Дока на порту 8001.``` 
Используется система связки рефреша + аксес токенов. Управляет и следит за состояниями токенов, назначает роли персоналу и
пользователям. Реализует также утилизацию неактулальных токенов, логин, логаут.

+ ### nx_etl
Сервис процесса транспортировки данных из бд в полнотекстовое хранилище. Дает 
доступ nx_backend к различным данным. Активируется и перекачивает новые данные 
каждое N-ное количество времени.


---
# Исследование по выбору хранилища:
https://github.com/whiteynoise/netflix_at_home/blob/main/DB_research.md

# Спринт 9 Исследование по выбору хранилища:
https://github.com/whiteynoise/netflix_at_home/blob/main/DB_research_2.md

---
Запуск тестов:
nx_ugc: docker-compose -f docker-compose.yaml -f docker-compose.override.yaml -f nx_ugc/tests/functional/docker-compose.tests.yaml up nx_auth mongodb app tests
