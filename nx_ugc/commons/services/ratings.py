from datetime import datetime

from commons.models.beanie_models import Rating
from commons.models.entity_models import UserFilmBase, RatingChange
from commons.models.response_models import AvgFilmRating, RatingResp

from pymongo.errors import DuplicateKeyError


class RatingService():
    @staticmethod
    async def add_rating(
            rating_info: RatingChange,
    ) -> None:
        """Добавление оценки контенту."""

        try:
            await Rating(**rating_info.model_dump()).insert()
        except DuplicateKeyError:
            pass
    
    @staticmethod
    async def update_rating(
            rating_info: RatingChange,
    ) -> None:
        """Обновление оценки контента."""

        if not (
            rating := await Rating.find_one(
                Rating.film_id == rating_info.film_id,
                Rating.user_id == rating_info.user_id,
            )
        ):
            return None
        
        rating.updated_at = datetime.now()
        rating.rating = rating_info.rating
        await rating.save()

    @staticmethod
    async def delete_rating(
            rating_info: UserFilmBase,
    ) -> None:
        """Удаление оценки фильма."""

        await Rating.find(**rating_info.model_dump()).delete()
    
    @staticmethod
    async def get_rating(
            user_id: int,
            film_id: int | None = None,
    ) -> list[RatingResp]:
        """Получение оценок пользователя."""

        query_filter: dict = {
            "user_id": user_id,
        }

        if film_id:
            query_filter["film_id"] = film_id

        user_ratings = await Rating.find(query_filter).to_list()

        return user_ratings

    @staticmethod
    async def get_avg_film_rating(
            film_id: str,
    ) -> AvgFilmRating:
        """Получение средней оценки фильма."""

        avg_rating = await Rating.find(
            Rating.film_id == film_id,
        ).avg(Rating.rating)

        return AvgFilmRating(
            film_id=film_id,
            avg_rating=avg_rating,
        )
