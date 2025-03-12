from datetime import datetime
from http import HTTPStatus
from typing import Annotated, Optional

from beanie.odm.operators.update.general import Set
from fastapi import APIRouter, Body, HTTPException, Query, Request
from loguru import logger
from models.beanie_models import Review
from models.entity_models import CreateReview, UpdateReview
from models.response_models import ListReview
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.post("/create_review", summary="Создание рецензии", status_code=200)
async def create_review(
    request: Request, review: Annotated[CreateReview, Body()]
):
    try:
        await Review(**review.model_dump(), user_id=request.state.user.user_id).insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Review already exists."
        )

    return


@router.patch("/update_review/{review_id}", summary="Обновление рецензии", status_code=200)
async def update_review(
    review_id: str, data: Annotated[UpdateReview, Body()]
):
    review = await Review.find_one(Review.review_id == review_id)

    if not review:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Review does not found."
        )

    update_data = data.model_dump(exclude_none=True)
    update_data["edited_at"] = str(datetime.now())
    await review.update(Set(update_data))

    return True


@router.delete("/{film_id}/delete_review", summary="Удаление рецензии", status_code=200)
async def delete_review(request: Request, film_id: str):
    review = await Review.find_one(
        Review.film_id == film_id, Review.user_id == request.state.user.user_id
    )
    if not review:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Like in this review does not exists.",
        )
    await review.delete()

    return


@router.get("/me", summary="Получение моих рецензий", status_code=200)
async def get_my_reviews(
    request: Request
) -> list[ListReview]:
    logger.info("Getting me reviews")
    return await Review.find(Review.user_id == request.state.user.user_id).to_list()


@router.get("/{film_id}", summary="Получение всех рецензий на фильм", status_code=200)
async def get_film_review(
    film_id: str, sort: Annotated[Optional[str], Query()] = None
) -> list[ListReview]:
    match sort:
        case "like" | "dislike":
            pipeline = [
                {"$match": {"film_id": film_id}},
                {
                    "$addFields": {
                        "count": {
                            "$size": {
                                "$filter": {
                                    "input": "$likes",
                                    "as": "like",
                                    "cond": {"$eq": ["$$like.action", "like" == sort]},
                                }
                            }
                        },
                    }
                },
                {"$sort": {"count": -1}},
            ]
            return await Review.aggregate(pipeline).to_list()
        case "date_create":
            return (
                await Review.find(Review.film_id == film_id)
                .sort(("created_at", DESCENDING))
                .to_list()
            )
        case _:
            return await Review.find(Review.film_id == film_id).to_list()
