from uuid import UUID
from functools import lru_cache
from http import HTTPStatus

from aiohttp import ClientError
from fastapi import HTTPException
from sqlalchemy import delete, and_, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from config import session, settings
from schemas.fav_film import FavFilmCreate, FilmWork

from models.user import PinFilm


class FavFilmService:
    """Сервис пройслойка для Любимых фильмов."""

    async def add_fav_film(
        self, db: AsyncSession, fav_film: FavFilmCreate,
    ) -> FavFilmCreate:
        """Добавление фильма в любимые"""

        result = await db.execute(
            select(func.count())
            .select_from(PinFilm)
            .where(PinFilm.user_id == fav_film.user_id)
        )
        count = result.scalar_one()

        if count >= 10:
            raise ValueError("Нельзя добавить больше 10 любимых фильмов!")

        new_fav_film = PinFilm(**fav_film.model_dump())

        db.add(new_fav_film)
        return new_fav_film

    async def delete_fav_film(self, db: AsyncSession, fav_film: FavFilmCreate) -> None:
        """Удаление фильма из любимых."""

        await db.execute(
            delete(PinFilm).where(
                and_(
                    PinFilm.user_id == fav_film.user_id,
                    PinFilm.film_id == fav_film.film_id,
                )
            )
        )
        await db.commit()

    async def get_fav_films_by_user(self, db: AsyncSession, user_id: UUID) -> list[FilmWork]:
        """Получение id фильмов."""
        films = select(PinFilm.film_id).where(PinFilm.user_id == user_id)
        result = await db.execute(films)
        result = result.scalars().all()

        try:
            async with session.aiohttp_session.get(
                    settings.content_url + ','.join(result),
                    timeout=5,
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=HTTPStatus.UNAUTHORIZED,
                        detail="Invalid token",
                    )

                data = await response.json()

        except ClientError as e:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Auth-service is unavailable",
            ) from e

        return [FilmWork(**film) for film in data]


@lru_cache()
def get_fav_film_service_service() -> FavFilmService:
    return FavFilmService()
