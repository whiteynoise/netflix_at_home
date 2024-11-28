from elasticsearch import Elasticsearch, helpers

from utils.backoff import backoff
from utils.es_indexes import base_index_settings
from typing import Protocol
from utils.es_indexes import index_by_name


class Loader(Protocol):
    def save_data(self, *args, **kwargs):
        """Получение данных для загрузки в Loader."""

    def prepare(self, *args, **kwargs):
        """Подготовка окружения для загрузки данных"""


class ESLoader:
    def __init__(self, config: dict):
        self._elastic_client = None
        self._elastic_config = config
        self.indexes = index_by_name

    def _retrieve_connection(self) -> None:
        """Чекер жизнеспособности клиента ES, при необходимости создает новый."""
        if not self._elastic_client or not self._elastic_client.ping():
            self._elastic_client = Elasticsearch(
                "{host}:{port}".format(**self._elastic_config), verify_certs=False
            )

    @backoff()
    def save_data(self, batch: list[dict], index_name: str) -> None:
        """Сохранение данных в ES."""
        self._retrieve_connection()
        helpers.bulk(client=self._elastic_client, actions=batch, index=index_name)

    @backoff()
    def create_index_if_not_exists(self, index_name: str, index_mapping: dict) -> None:
        """Создание индекса movies при необходимости."""
        self._retrieve_connection()

        if not self._elastic_client.indices.exists(index=index_name):
            self._elastic_client.indices.create(
                index=index_name, settings=base_index_settings, mappings=index_mapping
            )

    def prepare(self) -> None:
        """Подготовка окружения ESLoader"""
        for index_name, index_mapping in self.indexes.items():
            self.create_index_if_not_exists(index_name, index_mapping)
