from typing import AsyncGenerator

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import pg_config
from config.sqlalchemy import sqlalchemy_config


class Base(DeclarativeBase):
    metadata = sqlalchemy.MetaData(schema="events_admin")


dsn = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
    **pg_config.dict()
)
dsn_for_alembic = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    **pg_config.dict()
)

engine = create_async_engine(dsn, **sqlalchemy_config)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
