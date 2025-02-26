# Тестдрайв ClickHouse и Vertica

Сравнение двух аналитических БД для выбора одной в качестве используемой в ETL процессе хранения части пользовательских действий в онлайн-кинотеатре.
Обе базы имеют схожий набор достоинств и в первую очередь применяются как аналитические хранилища, в рамках тестдрайва проверялась их скорость в рамках возможного использования в проекте.

## Оглавление:
- [О тестируемых системах](#о-тестируемых-системах)
- [Тестирование](#тестирование)
- [Дополнительная информация по тестам](#дополнительная-информация-по-тестам)
- [Код скрипта и компоуз](#код-скрипта-и-компоуз)

# О тестируемых системах
### ClickHouse:
ClickHouse — это высокопроизводительная колонночная система управления базами данных, разработанная для обработки аналитических запросов в реальном времени.
Она оптимизирована для работы с большими объемами данных и обеспечивает высокую скорость выполнения сложных аналитических запросов.

### Vertica:
Vertica — это аналитическая реляционная база данных, разработанная для работы с большими объемами данных и высокопроизводительной обработки запросов.
Она использует колонночное хранение данных, что делает её особенно эффективной для аналитических задач, BI-систем и обработки данных в реальном времени.

# Тестирование

### Было проведено несколько тестов:
- Выборка из 1кк сгенерированных записей (для обеих баз набор идентичен);
- Структура таблицы в обеих БД одинаковая;
- Используются аналогичные запросы к обеим базам (для запись в ClickHouse используются батчи по 10к записей, в Vertica подобный подход приводил к результату в 16 секунд, при записи полной выборкой в 1кк, запись происходит за 11 секунд);
- Обе БД работают в рамках одной ноды своего кластера.

### Результат проверки скорости вставки и чтения из двух БД:

<p align="center"><img width="441" alt="image" src="https://github.com/user-attachments/assets/67fe02fb-a09c-440c-835a-def82d311b52" /></p>

### Результат выбора БД:
При тестировании было выявлено, что при планируемом использовании по скорости значительно выигрывает ClickHouse как по выборке, так и по вставке данных.
Помимо того, что БД полностью удовлетворяет функциональным требованиям, стоит также отметить другие преимущества:
- Активно обновляется;
- Имеет множество популярных клиентов на Python, включая поддерживаемый официальный;
- Имеет большое и активное сообщество;
- Open-source решение, не требует затрат при коммерческом использовании (не считая Enterprise решения).

# Дополнительная информация тестов

<div style="text-align: center;">
  <table>
    <tr>
      <td><strong>Система, на которой проходил тест</strong></td>
      <td><strong>Используемые библиотеки</strong></td>
    </tr>
    <tr>
      <td><strong>OS:</strong> MacOS</td>
      <td><strong>python:</strong> 3.11</td>
    </tr>
    <tr>
      <td><strong>OS Ver.:</strong> 15.0 (24A335)</td>
      <td><strong>vertica_python:</strong> 1.4.0</td>
    </tr>
    <tr>
      <td><strong>CPU:</strong> Apple M1</td>
      <td><strong>clickhouse_driver:</strong> 0.2.9</td>
    </tr>
    <tr>
      <td><strong>RAM:</strong> 8GB</td>
      <td><strong>faker:</strong> 0.7.4</td>
    </tr>
  </table>
</div>

# Код скрипта и компоуз
### Код тестов и генерации данных:

```python
import random
import json
import vertica_python

from clickhouse_driver import Client
from datetime import datetime
from faker import Faker
from time import time


def generate_data_file(
        file_name: str = 'fake_data',
        file_size: int = 1000000,
) -> None:
    """Генерация json файла с фейковыми данными"""
    faker = Faker()
    
    film_event_tags = (
        'video_quality_360',
        'video_quality_720',
        'video_quality_1080',
        'film_end',
    )

    users = tuple({faker.uuid4() for _ in range(0, 2000)})

    data = json.dumps(
        [
            {
                "row_num": row_num,
                "film_event_tag": random.choice(film_event_tags),
                "film_id": faker.uuid4(),
                "user_id": random.choice(users)
            }
            for row_num in range(0, file_size)
        ]
    )
        
    with open(f'{file_name}.json', 'w') as f:
        f.write(data)


def deserialize_file(
    file_name: str = 'fake_data'
) -> list[dict]:
    """Десериализатор файла"""
    with open(f'{file_name}.json', 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data


def timing(func): 
    def wrap_func(*args, **kwargs):
        func_name = func.__name__

        start_datetime = datetime.now()
        print(f'\033[93m{func_name}\033[0m started at {start_datetime.strftime("%d-%m-%Y %H:%M:%S")}')

        func(*args, **kwargs)

        end_datetime = datetime.now()

        print(f'Function \033[93m{func_name}\033[0m was executed in \033[92m{(end_datetime-start_datetime).total_seconds()}s\033[0m\n')
    
    return wrap_func 


@timing
def test_vertica_insert(
        cursor,
        data: list[dict],
) -> None:
    """Тест вставки данных в Vertica."""
    cursor.executemany(
        """
            INSERT INTO test_table (row_num, film_event_tag, film_id, user_id)
            VALUES (:row_num, :film_event_tag, :film_id, :user_id);
        """,
        data,
    )


@timing
def test_vertica_select_1(
        cursor,
) -> None:
    """Тест выборки данных с группировкой данных по тегу и подсчетом фильмов в Vertica."""
    cursor.execute(
        """
            SELECT COUNT(film_id)
            FROM test_table
            GROUP BY film_event_tag;
        """
    )


@timing
def test_vertica_select_2(
        cursor,
) -> None:
    """Тест выборки всех записей с тегом качества видео в 1080p в Vertica."""
    cursor.execute(
        """
            SELECT *
            FROM test_table
            WHERE film_event_tag = 'video_quality_1080';
        """
    )


def start_vertica_test(
        data: list[dict],
) -> None:
    """Хендлер запуска тестов Vertica."""
    connection_info = {
        'host': 'localhost',
        'port': 5433,
        'user': 'dbadmin',
        'password': 'password',
        'database': 'docker',
        'autocommit': True,
    }

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS test_table (
                    row_num BIGINT,
                    film_event_tag VARCHAR(20) NOT NULL,
                    film_id VARCHAR(36) NOT NULL,
                    user_id VARCHAR(36) NOT NULL
                );
            """
        )

        print('\n-------- \033[38;5;214mVERTICA\033[0m --------\n')

        test_vertica_insert(
            cursor=cursor,
            data=data,
        )

        test_vertica_select_1(cursor=cursor)
        test_vertica_select_2(cursor=cursor)


@timing
def test_clickhouse_insert(
        client: Client,
        data: list[dict]
) -> None:
    """Тест вставки данных в ClickHouse."""
    for i in range(0, len(data), 10000):
        batch = data[i : i + 10000]
        client.execute(
            """
                INSERT INTO example.test_table (
                    row_num,
                    film_event_tag,
                    film_id,
                    user_id
                )
                VALUES
            """,
            batch,
        )


@timing
def test_clickhouse_select_1(
        client: Client,
) -> None:
    """Тест выборки данных с группировкой данных по тегу и подсчетом фильмов в ClickHouse."""
    client.execute(
        """    
            SELECT COUNT(film_id)
            FROM example.test_table
            GROUP BY film_event_tag
        """
    )


@timing
def test_clickhouse_select_2(
        client: Client,
) -> None:
    """Тест выборки всех записей с тегом качества видео в 1080p в ClickHouse."""
    client.execute(
        """
            SELECT *
            FROM example.test_table
            WHERE film_event_tag = 'video_quality_1080'
        """
    )


def start_clickhouse_test(
        data: list[dict],
) -> None:
    """Хендлер запуска тестов ClickHouse."""
    client = Client(host='localhost')

    client.execute(
        """
            CREATE DATABASE IF NOT EXISTS example
            ON CLUSTER company_cluster
        """
    )

    client.execute(
        """
            CREATE TABLE IF NOT EXISTS example.test_table
            ON CLUSTER company_cluster (
                row_num Int64,
                film_event_tag String,
                film_id String,
                user_id String
            )
            Engine=MergeTree()
            ORDER BY row_num
        """
    )

    print('\n-------- \033[38;5;214mCLICKHOUSE\033[0m --------\n')

    test_clickhouse_insert(
        client=client,
        data=data,
    )

    test_clickhouse_select_1(client=client)
    test_clickhouse_select_2(client=client)


if __name__ == "__main__":
    generate_data_file()
    data = deserialize_file()

    start_vertica_test(data)
    start_clickhouse_test(data)

```

### Используемый компоуз ClickHouse и Vertica:

```yaml
version: '3.5'

services:
  zookeeper:
    image: zookeeper:3.8
    container_name: zookeeper
    hostname: zookeeper

  clickhouse-node1:
    image: clickhouse/clickhouse-server:23
    container_name: clickhouse-node1
    hostname: clickhouse-node1
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./clickhouse_data/node1:/etc/clickhouse-server
    depends_on:
      - zookeeper

  vertica:
    image: jbfavre/vertica:latest
    container_name: vertica-db
    ports:
      - "5433:5433"
      - "5444:5444"
    environment:
      APP_DB_USER: dbadmin
      APP_DB_PASSWORD: password
      VERTICA_MEMDEBUG: 2
      TZ: "Europe/Prague"
    volumes:
      - vertica_data:/data

volumes:
  vertica_data:
```
