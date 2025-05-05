from abc import ABC, abstractmethod
from typing import Callable, Awaitable


class AbstractBrokerConsumer(ABC):
    @abstractmethod
    async def setup_connection(self) -> None:
        """Устанавливает соединение с брокером сообщений."""
        pass

    @abstractmethod
    async def start_consumption(self, callback: Callable[[dict], Awaitable[None]]) -> None:
        """Запускает потребление сообщений и вызывает callback для обработки каждого сообщения."""
        pass


class AbstractWorker(ABC):
    @abstractmethod
    async def start_worker(self) -> None:
        """Точка входа в воркер."""
        pass

    @abstractmethod
    async def process_message(self, notification_info: dict) -> None:
        """Логика обработки сообщения."""
        pass

    @abstractmethod
    def render_message(self, notification_info: dict) -> str:
        """Рендеринг сообщения."""
        pass
