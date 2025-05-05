import asyncio

from loguru import logger
from typing import Any
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from db.postgres import dsn


def get_waiter(engine: AsyncEngine, sleep_time: int = 10, limit: int = 10) -> Any:
    async def _wait() -> None:
        retries = 0
        while retries < limit:
            try:
                async with engine.begin() as conn:
                    await conn.execute("SELECT 1")
                logger.info("Success ping database")
                return None
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
    logger.info("DNS: %s" % dsn)
    engine = create_async_engine(dsn, echo=True)
    get_waiter(engine, 3)
