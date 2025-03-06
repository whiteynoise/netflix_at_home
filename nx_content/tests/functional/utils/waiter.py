import time
from functional.test_logger import logger

def get_waiter(client, sleep_time: int = 10, limit: int = 10):
    retries = 0
    while retries < limit:
        logger.info("Try connect %s: try %d", client, retries)
        if client.ping():
            logger.info("Success ping %s", client)
            return
        retries += 1
        time.sleep(sleep_time)

    logger.error("Error during ping %s", client)
    raise ConnectionError
