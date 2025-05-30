import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Request, Path
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session

from schemas.fav_film import FavFilmCreate, FilmBody
from services.repo import FavFilmService, get_fav_film_service_service

router = APIRouter(tags=["p"])


@router.post(
    "/add_fav_film",
    summary="Добавить любимый фильм на витрину",
    description="Добавление любимого фильма на витрину. Максимум может быть 10.",
)
async def add_fav_film(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
    film: Annotated[FilmBody, Body()],
    fav_film_service: Annotated[FavFilmService, Depends(get_fav_film_service_service)]
) -> None:
    data = FavFilmCreate(user_id=request.state.user.user_id, film_id=film.film_id)
    """Добавить любимый фильм на витрину"""
    await fav_film_service.add_fav_film(db=db, fav_film=data)


@router.delete(
    "/delete_fav_film/{film_id}",
    summary="Удалить любимый фильм с витрины",
    description="Удаление любимого фильма с витрины. Максимум может быть 10.",
)
async def add_fav_film(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
    film_id: Annotated[uuid.UUID, Path()],
    fav_film_service: Annotated[FavFilmService, Depends(get_fav_film_service_service)]
) -> None:
    data = FavFilmCreate(user_id=request.state.user.user_id, film_id=film_id)
    """Добавить любимый фильм на витрину"""
    await fav_film_service.delete_fav_film(db=db, fav_film=data)


@router.get(
    "/fav_films",
    summary="Список фильмов на витрине",
)
async def add_fav_film(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
    fav_film_service: Annotated[FavFilmService, Depends(get_fav_film_service_service)]
) -> None:
    """Добавить любимый фильм на витрину"""
    films = await fav_film_service.get_fav_films_by_user(db=db, user_id=request.state.user.user_id)
    print(films)
