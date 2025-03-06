from datetime import datetime
from typing import Any, Protocol

from redis import Redis
from utils.backoff import backoff


class KeyValueStorage(Protocol):
    def set_state(self, state: Any) -> None:
        """Сохранить состояние в хранилище."""

    def get_state(self) -> str:
        """Получить состояние из хранилища."""


class RedisStateStorage:
    def __init__(self, config: dict):
        self._redis_connection = None
        self._redis_config = config
        self._datetime_format = "%Y-%m-%d %H:%M:%S.%f"

    def _retrieve_connection(self) -> None:
        """Чекер жизнеспособности клиента Redis, при необходимости создает новый."""
        if not self._redis_connection or not self._redis_ping_bypass():
            self._redis_connection = Redis(**self._redis_config)

    def _redis_ping_bypass(self) -> bool:
        """Пинг редиса с обходом возможного рейза."""
        try:
            self._redis_connection.ping()
        except:
            return False

        return True

    @backoff()
    def set_state(self, state: datetime) -> None:
        """Установка состояния."""
        self._retrieve_connection()
        self._redis_connection.set(
            name="state_time", value=state.strftime(self._datetime_format)
        )

    @backoff()
    def get_state(self) -> str:
        """Получение состояния."""
        self._retrieve_connection()

        if state_time := self._redis_connection.get(name="state_time"):
            state_time = state_time.decode("UTF-8")
        else:
            state_time = datetime.min.strftime(self._datetime_format)

        return state_time
