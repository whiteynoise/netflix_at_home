# Проект netflix_at_home

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
Схема
![вот же она](https://github.com/whiteynoise/netflix_at_home/blob/main/schema.jpg)
