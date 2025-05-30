from datetime import datetime

from beanie.odm.operators.update.general import Set
from commons.models.beanie_models import Review
from commons.models.entity_models import AddReview, UpdReview, UserFilmBase
from commons.models.response_models import ListReview
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError


class ReviewService():
    async def add_review(
            review_info: AddReview,
    ) -> bool:
        """Создать рецензию."""

        result = True

        try:
            await Review(**review_info.model_dump()).insert()
        except DuplicateKeyError:
            result = False

        return result

    async def update_review(
            review_info: UpdReview,
    ) -> bool:
        """Обновить рецензию."""

        if not (
            review := await Review.find_one(
                Review.review_id == review_info.review_id,
            )
        ):
            return False

        update_data = review_info.model_dump(exclude_none=True)
        update_data["edited_at"] = str(datetime.now())
        await review.update(Set(update_data))

        return True

    async def delete_review(
            review_info: UserFilmBase,
    ) -> bool:
        """Удалить рецензию."""

        if not (
            review := await Review.find_one(
                **review_info.model_dump(),
            )
        ):
            return False
        
        await review.delete()
        return True

    async def get_my_reviews(
            user_id: int,
    ) -> list[ListReview]:
        """Получить рецензию по пользователю."""

        return await Review.find(
            Review.user_id == user_id,
        ).to_list()
    
    async def get_film_review(
            film_id: str,
            sort: str | None = None,
    ) -> list[ListReview]:
        """Получить все рецензии на фильм."""
        
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
