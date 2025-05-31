from fastapi import APIRouter, Request

from commons.models.entity_models import RatingBase
from commons.models.response_models import AvgFilmRating, RatingResp
from commons.services.ratings import RatingService as rs

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=list[RatingResp],
    summary="Получение оценки пользователя на фильм",
    description="Получение оценок пользователя",
    status_code=200,
)
async def get_rating(
        film_id: str,
        request: Request,
) -> list[RatingResp]:
    return await rs.get_rating(
        user_id=request.state.user.user_id,
        film_id=film_id,
    )


@router.get(
    "/get_avg_film_rating",
    response_model=AvgFilmRating,
    summary="Получение средней оценки фильма",
    description="Получение средней оценки фильма",
    status_code=200,
)
async def get_avg_film_rating(
        rating_info: RatingBase,
) -> AvgFilmRating:
    return await rs.get_avg_film_rating(
        film_id=rating_info.film_id,
    )
