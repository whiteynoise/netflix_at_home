from functools import wraps
from time import sleep

from psycopg import Error as PGError
from elasticsearch import ApiError, ConnectionError
from redis.exceptions import RedisError

from configs.logger_config import logger


class MaxRetriesException(Exception):
    pass


def backoff(max_retries=10, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """Функция для повторного выполнения функции через некоторое время, если возникла ошибка."""
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_retries = 0
            t = start_sleep_time

            while True:
                try:
                    return func(*args, **kwargs)
                except (PGError, ApiError, ConnectionError, RedisError) as err:
                    logger.error(err)
                
                current_retries += 1

                if current_retries > max_retries:
                    raise MaxRetriesException(f"Process is dead, the killer: {func.__name__}")

                t = t * factor if t < border_sleep_time else border_sleep_time

                sleep_tries = f'({current_retries}/{max_retries})'
                logger.info('Sleep after a failed attempt to backoff %s', sleep_tries)
                sleep(t)
                    
        return inner
    
    return func_wrapper
