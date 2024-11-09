from typing import Optional
from redis.asyncio import Redis

redis: Optional[Redis] = None

async def get_redis() -> Redis:
    '''Возвращает соединение с Redis'''
    return redis
