import asyncio
import logging
import time

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from functional.settings import PG_CONFIG

logger = logging.getLogger(__name__)


def get_waiter(engine: AsyncEngine, sleep_time: int = 10, limit: int = 10):
    async def _wait():
        retries = 0
        while retries < limit:
            try:
                async with engine.begin() as conn:
                    await conn.execute("SELECT 1")
                logger.info("Success ping database")
                return
            except Exception as e:
                logger.warning(
                    "Try connect to database: attempt %d/%d, error: %s",
                    retries + 1,
                    limit,
                    e,
                )
                retries += 1
                await asyncio.sleep(sleep_time)

        logger.error("Error during ping database, connection failed")
        raise ConnectionError("Could not connect to database after %d attempts" % limit)

    return _wait


if __name__ == "__main__":
    # while True:
    #     time.sleep(1000)
    dsn = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        **PG_CONFIG
    )
    logger.info("DNS: %s" % dsn)

    engine = create_async_engine(dsn, echo=True, future=True)

    get_waiter(engine, 3)
