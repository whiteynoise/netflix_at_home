import copy
from typing import Protocol
import psycopg

from psycopg.rows import dict_row

from datetime import datetime

import utils.sql_queries as sql_queries
from utils.pydantic_models import model_by_index
from utils.backoff import backoff


class Extractor(Protocol):
    def get_data(self, *args, **kwargs):
        """Получение данных для загрузки."""


class PGExtractor:
    def __init__(self, config: dict, batch_size: int = 250):
        self._pg_client = None
        self._pg_config = config
        self.batch_size = batch_size

    def _retrieve_connection(self) -> None:
        """Чекер жизнеспособности клиента PG, при необходимости создает новый."""
        if not self._pg_client or self._pg_client.closed:
            self._pg_client = psycopg.connect(**self._pg_config, row_factory=dict_row)

    @backoff()
    def check_on_update(self, current_state_date: str) -> datetime | None:
        """Получение максимальной даты модификации среди таблиц."""
        self._retrieve_connection()
        return (
            self._pg_client.cursor().execute(
                sql_queries.get_max_time_across_tables(current_state_date)
            )
        ).fetchone()["new_date"]

    @backoff()
    def get_data(self, index_name: str, current_state_date: str):
        """Получение данных для загрузки в ES."""
        self._retrieve_connection()

        sql_query = sql_queries.quaries_by_index[index_name]
        execute_result = self._pg_client.cursor().execute(sql_query(current_state_date))

        model = model_by_index[index_name]

        while results := execute_result.fetchmany(self.batch_size):
            yield [self._prepare_row(result, model) for result in results]

    @staticmethod
    def _prepare_row(row, model) -> dict:
        """Валидация строки, добавление идентификатора в ES."""
        row = model(**row).model_dump()
        row["_id"] = row["id"]
        return row
