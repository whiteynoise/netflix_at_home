from abc import ABC, abstractmethod
from functools import lru_cache
from redis.asyncio import Redis

from constants import BLACKLIST


class Storage(ABC):
    @abstractmethod
    async def set_value(self, *args, **kwargs) -> None:
        '''Положить данные в хранилище'''
        pass


class RedisStorage(Storage):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_value(self, user_id: str, access_token: str) -> None:
        await self.redis.sadd(user_id, access_token)

    async def add_in_blacklist(self, access_token: str) -> None:
        await self.redis.sadd(BLACKLIST, access_token)

    async def check_in_blacklist(self, access_token: str):
        return await self.redis.sismember(BLACKLIST, access_token)


@lru_cache()
def get_redis_storage(redis: Redis) -> RedisStorage:
    return RedisStorage(redis)
