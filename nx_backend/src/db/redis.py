from redis.asyncio import Redis

redis: Redis | None = None

async def get_redis() -> Redis:
    '''Возвращает соединение с Redis'''
    return redis
