from typing import Annotated, Optional

from fastapi import APIRouter, Query, Request
from commons.models.response_models import ListReview
from commons.services.reviews import ReviewService as rs

router = APIRouter()


@router.get(
    "/get_my_reviews",
    response_model=list[ListReview],
    summary="Получение моих рецензий",
    status_code=200,
)
async def get_my_reviews(
        request: Request,
) -> list[ListReview]:
    return await rs.get_my_reviews(
        user_id=request.state.user.user_id,
    )


@router.get(
    "/{film_id}",
    response_model=list[ListReview],
    summary="Получение всех рецензий на фильм",
    status_code=200,
)
async def get_film_review(
        film_id: str,
        sort: Annotated[Optional[str], Query()] = None,
) -> list[ListReview]:
    return await rs.get_film_review(
        film_id=film_id,
        sort=sort,
    )
