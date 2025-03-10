from redis import Redis
from functional.settings import REDIS_CONFIG
from functional.utils.waiter import get_waiter

if __name__ == "__main__":
    redis_client = Redis(**REDIS_CONFIG)

    get_waiter(redis_client, 3)
