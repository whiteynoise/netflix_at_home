from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.postgres import engine


class ConstManager:
    def __init__(self, engine):
        self.engine = engine
        self.roles = {}

    async def initialize(self):
        """Инициализация констант при старте."""

        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            self.roles = await self._load_roles(session)

    async def _load_roles(self, session):
        """Загрузка ролей."""
        result = (
            await session.execute(
                text("""
                    SELECT role_id, title
                    FROM auth.roles
                """)
            )
        ).mappings().all()

        if not result:
            raise Exception(
                f"Константа ролей не может быть пустой"
            )

        return {row["title"]: row["role_id"] for row in result}


constants = ConstManager(engine)
