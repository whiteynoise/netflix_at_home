from core.config import PG_CONFIG
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()

dsn = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}'.format(**PG_CONFIG)

engine = create_async_engine(dsn, echo=True, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    '''Получение сессии'''
    async with async_session() as session:
        yield session


async def create_database() -> None:
    '''Создание всех таблиц'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    '''Удаление всех таблиц'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        