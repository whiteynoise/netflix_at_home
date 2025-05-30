from http import HTTPStatus

from fastapi import APIRouter, Request, Depends
from models.entity_models import RatingBase, RatingGet
from models.response_models import AvgFilmRating, RatingResp
from services.ratings import RatingService, rating_service

router = APIRouter()


@router.get(
    "/get_rating",
    response_model=list[RatingResp],
    summary="Получение оценок",
    description="Получение оценок пользователя",
    status_code=200,
)
async def get_rating(
        request: Request,
        rating_info: RatingGet,
        rs: RatingService = Depends(rating_service.get_service()),
) -> list[RatingResp]:
    return await rs.get_rating(
        user_id=request.state.user.user_id,
        film_id=rating_info.film_id,
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
        rs: RatingService = Depends(rating_service.get_service()),
) -> AvgFilmRating:
    return await rs.get_avg_film_rating(
        film_id=rating_info.film_id,
    )
