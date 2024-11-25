import time

from redis import Redis

from functional.settings import REDIS_CONFIG


if __name__ == '__main__':
    redis_client = Redis(**REDIS_CONFIG)

    while True:
        if redis_client.ping():
            break
        time.sleep(3)
