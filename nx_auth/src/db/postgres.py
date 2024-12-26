import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import PG_CONFIG


class Base(DeclarativeBase):
    metadata = sa.MetaData(schema="auth")


dsn = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(**PG_CONFIG)
dsn_for_alembic = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(**PG_CONFIG)

engine = create_async_engine(dsn, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    '''Получение сессии'''
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
