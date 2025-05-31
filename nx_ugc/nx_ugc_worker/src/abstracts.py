from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Any


class AbstractConsumer(ABC):
    @abstractmethod
    async def __aenter__(self) -> "AbstractConsumer":
        """Инициализация подключения."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Завершение подключения."""
        pass

    @abstractmethod
    async def start_consumption(
        self,
        callback: Callable[[dict], Awaitable[None]]
    ) -> None:
        """Запуск потребления сообщений с передачей callback."""
        pass


class AbstractWorker(ABC):
    @abstractmethod
    async def __call__(self, message: dict[str, Any]) -> None:
        """Обработка входящего сообщения."""
        pass
