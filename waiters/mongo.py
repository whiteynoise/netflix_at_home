import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_CONFIG = {
    "host": "mongodb",
    "port": 27017,
    "user": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
}


async def wait_for_mongo(sleep_time: int = 3, limit: int = 10) -> bool:
    """Waiter для MongoDB."""
    retries = 0
    uri = f"mongodb://{MONGO_CONFIG['user']}:{MONGO_CONFIG['password']}@{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}"

    while retries < limit:
        try:
            client = AsyncIOMotorClient(uri)
            await client.server_info()
            return True
        except Exception:
            retries += 1
            await asyncio.sleep(sleep_time)
    raise ConnectionError("Could not connect to MongoDB")


if __name__ == "__main__":
    asyncio.run(wait_for_mongo())
