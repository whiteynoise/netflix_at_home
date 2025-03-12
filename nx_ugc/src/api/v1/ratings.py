from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from models.beanie_models import Rating
from models.entity_models import RatingAdd, RatingBase, RatingGet, RatingUpd
from models.response_models import AvgFilmRating, RatingResp
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.post(
    "/add_rating",
    response_model=bool,
    summary="Добавление оценки",
    description="Добавление оценки пользователя",
    status_code=201
)
async def add_rating(
    request: Request,
    rating_info: RatingAdd,
) -> None:
    """Добавление оценки контенту."""

    try:
        await Rating(
            **rating_info.model_dump(),
            user_id=request.state.user.user_id,
        ).insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Rating for this movie already exists.",
        )

    return


@router.patch(
    "/update_rating",
    response_model=bool,
    summary="Обновление оценки",
    description="Обновление оценки пользователя",
    status_code=200
)
async def update_rating(
    request: Request,
    rating_info: RatingUpd,
) -> None:
    """Обновление оценки контента."""

    doc = await Rating.find_one(
        Rating.film_id == rating_info.film_id,
        Rating.user_id == request.state.user.user_id,
    )

    if doc:
        doc.updated_at = datetime.now()
        doc.rating = rating_info.rating
        await doc.save()

    return


@router.post(
    "/delete_rating",
    response_model=bool,
    summary="Удаление оценки",
    description="Удаление оценки пользователя",
    status_code=200
)
async def delete_rating(
    request: Request,
    rating_info: RatingBase,
) -> None:
    """Удаление оценки фильма."""

    await Rating.find(
        Rating.user_id == request.state.user.user_id,
        Rating.film_id == rating_info.film_id,
    ).delete()

    return


@router.get(
    "/get_rating",
    response_model=list[RatingResp],
    summary="Получение оценок",
    description="Получение оценок пользователя",
    status_code=200
)
async def get_rating(
    request: Request,
    rating_info: RatingGet,
) -> list[RatingResp]:
    """Получение оценок пользователя."""

    query_filter: dict = {
        "user_id": request.state.user.user_id,
    }

    if film_id := rating_info.film_id:
        query_filter["film_id"] = film_id

    user_ratings = await Rating.find(query_filter).to_list()

    return user_ratings


@router.get(
    "/get_avg_film_rating",
    response_model=AvgFilmRating,
    summary="Получение средней оценки фильма",
    description="Получение средней оценки фильма",
    status_code=200
)
async def get_avg_film_rating(
    rating_info: RatingBase,
) -> AvgFilmRating:
    """Получение средней оценки фильма."""

    film_id = rating_info.film_id

    avg_rating = await Rating.find(
        Rating.film_id == film_id,
    ).avg(Rating.rating)

    return AvgFilmRating(film_id=film_id, avg_rating=avg_rating)
