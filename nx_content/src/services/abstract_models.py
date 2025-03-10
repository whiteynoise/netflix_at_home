from typing import Generator, Protocol

from async_lru import alru_cache


class Service(Protocol):
    """Сервисный класс для раюоты с хранилищем через АПИ"""

    async def get_by_id(*args, **kwargs):
        """Получение объекта по id"""


class Storage(Protocol):
    """Протокол для взаимодействия с хранилищем"""

    async def get(*args, **kwargs):
        """Получение объекта из хранилища"""

    async def search(*args, **kwargs):
        """Поиск объекта в хранилище"""


class ServiceManager:
    def __init__(self, service: Service, factory: Generator):
        self.service = service
        self.factory = factory

    @alru_cache()
    async def get_service_cache(self) -> Service:
        storage = await self.factory()
        sample = self.service(storage)
        return sample

    async def get_service(self) -> Service:
        return await self.get_service_cache()
