from functional.settings import REDIS_CONFIG
from functional.utils.waiter import get_waiter
from redis import Redis

if __name__ == "__main__":
    redis_client = Redis(**REDIS_CONFIG)

    get_waiter(redis_client, 3)
