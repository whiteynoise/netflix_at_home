# Тестдрайв PostgreSQL и Mongo

## Оглавление:
- [О тестируемых системах](#о-тестируемых-системах)
- [Тестирование](#тестирование)
- [Дополнительная информация по тестам](#дополнительная-информация-по-тестам)
- [Код скрипта и компоуз](#код-скрипта-и-компоуз)

# О тестируемых системах

### PostgreSQL:
Мощная реляционная база данных
### Mongo:
Документо-ориентированная база данных (NoSQL).

# Тестирование

### Тесты:
- вставка оценок (10^6)
- вставка лайков (10^6)
- средняя оценка юзера
- кол-во лайков, который поставил юзер (есть еще и дизлайки)

### Результат проверки скорости вставки и чтения из двух БД:

| Операция             | PostgreSQL (сек) | MongoDB (сек) |
|----------------------|----------------|---------------|
| Вставка оценок       | 260.035266   | 8.477232      |
| Вставка лайков       | 221.102484   | 7.874845      |
| Средняя оценка юзера | 0.134737    | 0.381803      |
| Кол-во лайков юзера  | 0.051303    | 0.285749      |


### Результат выбора БД:
По результатам замера операций с выбранными структурами выигрывает Mongo

# Дополнительная информация по тестам

<div style="text-align: center;">
  <table>
    <tr>
      <td><strong>Система, на которой проходил тест</strong></td>
      <td><strong>Используемые библиотеки</strong></td>
    </tr>
    <tr>
      <td><strong>OS:</strong> Linux 22.04 </td>
      <td><strong>python:</strong> 3.11</td>
    </tr>
    <tr>
      <td><strong>Postgres:</strong> 16.0</td>
      <td><strong>psycopg2-binary:</strong> 2.9.10 </td>
    </tr>
    <tr>
      <td><strong>Mongo:</strong> 6.0.21 </td>
      <td><strong>pymongo:</strong> 4.11.1 </td>
    </tr>
    <tr>
      <td><strong>CPU:</strong> Ryzen 5</td>
      <td></td>
    </tr>
    <tr>
      <td><strong>RAM:</strong> 16GB</td>
      <td></td>
    </tr>
  </table>
</div>

# Код скрипта и компоуз

### Генерация тестов
```python
import random
import uuid
from datetime import datetime

batch_size = 1000

user_uuid = str(uuid.uuid4())


def generate_rating():
    """Оценка"""
    return {
        "film_id": str(uuid.uuid4()),
        "film_name": f"Film {random.randint(1, 100)}",
        "user_id": user_uuid,
        "rating": random.randint(1, 10),
        "created_at": datetime.utcnow(),
    }


def generate_like():
    """Лайк на рецензию"""
    return {
        "review_id": str(uuid.uuid4()),
        "user_id": user_uuid,
        "created_at": datetime.utcnow(),
        "action": random.choice([True, False]),
    }


rating_data = [generate_rating() for _ in range(1000000)]
likes_data = [generate_like() for _ in range(1000000)]
```

### Тест Postgres
```python
import psycopg2

from generate_test import generate_rating, generate_like, rating_data, likes_data
from utils import timing


class PostgresqlTest:
    def __init__(self, dsn):
        self.dsn = dsn

    def create_table(self):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS rating (
                    id SERIAL PRIMARY KEY,
                    film_id UUID,
                    user_id UUID,
                    film_name TEXT,
                    rating INT,
                    created_at TIMESTAMP WITH TIME ZONE
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS likes (
                    id SERIAL PRIMARY KEY,
                    review_id UUID,
                    user_id UUID,
                    created_at TIMESTAMP,
                    action BOOLEAN
                );
                """)
                conn.commit()

    @timing
    def insert_rating(self, data, batch_size=10000):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                for i in range(0, len(data), batch_size):
                    batch = data[i : i + batch_size]
                    cur.executemany(
                        """
                    INSERT INTO rating (film_id, film_name, user_id, rating, created_at)
                    VALUES (%(film_id)s, %(film_name)s, %(user_id)s, %(rating)s, %(created_at)s);
                    """,
                        batch,
                    )
                    conn.commit()

    @timing
    def insert_likes(self, data, batch_size=10000):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                for i in range(0, len(data), batch_size):
                    batch = data[i: i + batch_size]
                    cur.executemany(
                        """
                        INSERT INTO likes (review_id, user_id, action, created_at)
                        VALUES (%(review_id)s, %(user_id)s, %(action)s, %(created_at)s);
                        """,
                        batch,
                    )
                    conn.commit()

    @timing
    def avg_rating(self):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT AVG(rating) FROM rating
                """)

    @timing
    def count_likes(self):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT COUNT(*) FROM likes WHERE action is true
                """)


def main():
    dsn = "dbname=db user=admin host=localhost port=5433 password=password"

    pg_test = PostgresqlTest(dsn)

    pg_test.create_table()
    pg_test.insert_rating(rating_data)
    pg_test.insert_likes(likes_data)

    pg_test.avg_rating()
    pg_test.count_likes()


main()
```
### Тест mongo
```python
from pymongo import MongoClient

from generate_test import rating_data, likes_data
from utils import timing


class MongoTest:
    def __init__(self, uri):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["db"]

    @timing
    def insert_rating(self, data, batch_size=10000):
        collection = self.db["rating"]
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            collection.insert_many(batch)

    @timing
    def insert_likes(self, data, batch_size=10000):
        collection = self.db["likes"]
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            collection.insert_many(batch)

    @timing
    def avg_rating(self):
        collection = self.db["rating"]
        cond = [{"$group": {"_id": None, "arg_rating": {"$avg": "$rating"}}}]
        collection.aggregate(cond)

    @timing
    def count_likes(self):
        collection = self.db["likes"]
        cond = [
            {"$match": {"action": True}},
            {"$group": {"_id": None, "count_likes": {"$sum": 1}}},
        ]
        collection.aggregate(cond)


def main():
    uri = "mongodb://localhost:27019/"

    mongo_test = MongoTest(uri)

    mongo_test.insert_rating(rating_data)
    mongo_test.insert_likes(likes_data)

    mongo_test.avg_rating()
    mongo_test.count_likes()


main()
```

### Компоуз

```yaml
version: '3.9'

services:
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    restart: unless-stopped

  postgres:
    image: postgres:16
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: db
    ports:
      - "5433:5432"


volumes:
  mongo-config:
  mongo-shard-1:
```
