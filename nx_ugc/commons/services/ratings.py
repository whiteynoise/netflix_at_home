from datetime import datetime

from commons.models.beanie_models import Rating
from commons.models.entity_models import UserFilmBase, RatingChange
from commons.models.response_models import AvgFilmRating, RatingResp
from pymongo.errors import DuplicateKeyError


class RatingService():
    async def add_rating(
            self,
            rating_info: RatingChange,
    ) -> bool:
        """Добавление оценки контенту."""

        result = True

        try:
            await Rating(**rating_info.model_dump()).insert()
        except DuplicateKeyError:
            result = False

        return result

    async def update_rating(
            self,
            rating_info: RatingChange,
    ) -> bool:
        """Обновление оценки контента."""

        doc = await Rating.find_one(**rating_info.model_dump())

        if not doc:
            return False
        
        doc.updated_at = datetime.now()
        doc.rating = rating_info.rating
        await doc.save()

        return True

    async def delete_rating(
            self,
            rating_info: UserFilmBase,
    ) -> bool:
        """Удаление оценки фильма."""

        await Rating.find(**rating_info.model_dump()).delete()
        return True
    
    async def get_rating(
            self,
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

    async def get_avg_film_rating(
            self,
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
