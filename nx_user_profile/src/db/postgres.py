import sqlalchemy as sa
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.settings import pg_settings


class Base(DeclarativeBase):
    metadata = sa.MetaData(schema="auth")


dsn = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(**pg_settings.model_dump())
dsn_for_alembic = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
    **pg_settings.model_dump()
)

engine = create_async_engine(dsn, echo=True, future=True)

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
