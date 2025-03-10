from abc import ABC, abstractmethod
from json import dumps, loads

from functools import lru_cache, wraps
from typing import Any, Callable
from pydantic import TypeAdapter

from redis.asyncio import Redis
from db.redis import get_redis

from services.utils.constants import ignore_endpoint_params


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class CacheInterface(ABC):
    @abstractmethod
    async def put_to_cache(self, *args, **kwargs) -> None:
        """Сохранить данные в кэш-хранилище."""
        ...

    @abstractmethod
    async def get_from_cache(self, *args, **kwargs) -> Any | None:
        """Получить данные из кэш-хранилища."""
        ...


class RedisCache(CacheInterface):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def put_to_cache(
        self, cache_key: str, data_object: Any | list[Any], only_one: bool
    ) -> None:
        """Сохранить данные в Redis."""

        data = (
            dumps(data_object.model_dump())
            if only_one
            else dumps([_.model_dump() for _ in data_object])
        )

        await self.redis.set(cache_key, data, FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_from_cache(
        self, cache_key: str, pydantic_model: Any, only_one: bool
    ) -> Any | None:
        """Получить данные из Redis."""

        data = await self.redis.get(cache_key)

        if not data:
            return

        if only_one:
            data = pydantic_model.model_validate_json(data)
        else:
            type_adapter = TypeAdapter(list[pydantic_model])
            data = type_adapter.validate_python(loads(data))

        return data


@lru_cache()
def get_redis_cache(redis: Redis) -> RedisCache:
    return RedisCache(redis)


def gen_key_for_redis(key_base: str, endpoint_params: list):
    """Генерация ключа для кэша в Redis."""

    key_attrs = [
        ("".join(str(v).split())).lower()
        for k, v in endpoint_params.items()
        if v and k not in ignore_endpoint_params
    ]

    return f"{key_base}{'_'.join(key_attrs)}"


def redis_caching(key_base: str, response_model: Any, only_one: bool = False):
    """Декоратор для работы с кэшем Redis."""

    def inner(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis_instance = get_redis_cache(await get_redis())

            if request_params := kwargs.get("params"):
                request_params = request_params.model_dump()

            cache_key = gen_key_for_redis(key_base, request_params or kwargs)

            if data_object := await redis_instance.get_from_cache(
                cache_key, response_model, only_one
            ):
                return data_object

            data_object = await func(*args, **kwargs)

            await redis_instance.put_to_cache(cache_key, data_object, only_one)

            return data_object

        return wrapper

    return inner
