from json import dumps, loads

from typing import Any, Callable
from pydantic import TypeAdapter
from redis.asyncio import Redis
from db.redis import get_redis
from functools import lru_cache, wraps


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5

class RedisCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def get_key_for_cache(key_base: str, key_attrs: list):
        '''Получение ключа для кэша в Redis'''
        return f"{key_base}{'_'.join(key_attrs)}"

    async def put_to_cache(
            self,
            cache_key: str,
            data_object: Any | list[Any],
            only_one: bool
        ) -> None:
        '''Сохранение данных в кэше Redis'''
        data = (dumps(data_object.model_dump()) if only_one else
                dumps([_.model_dump() for _ in data_object]))
        
        await self.redis.set(
            cache_key,
            data,
            FILM_CACHE_EXPIRE_IN_SECONDS
        )
    
    async def get_from_cache(
            self,
            cache_key: str,
            pydantic_model: Any,
            only_one: bool
        ) -> Any | None:
        '''Получение кинопроизведения из Redis'''
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
def get_redis_cache(
    redis: Redis
) -> RedisCache:
    return RedisCache(redis)


def redis_caching(
        key_base: str,
        response_model: Any,
        only_one: bool = False
    ):
    '''Декоратор для работы с кэшем Redis'''
    def inner(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis_instance = get_redis_cache(await get_redis())

            key_attrs = [(''.join(str(v).split())).lower()
                         for k, v in kwargs.items()
                         if v and k not in ('film_service',
                                            'genre_service',
                                            'person_service')]
            
            cache_key = redis_instance.get_key_for_cache(key_base, key_attrs)

            if data_object := await redis_instance.get_from_cache(cache_key,
                                                                  response_model,
                                                                  only_one):
                return data_object

            data_object = await func(*args, **kwargs)

            await redis_instance.put_to_cache(cache_key, data_object, only_one)

            return data_object
        
        return wrapper
    
    return inner
