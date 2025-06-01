from commons.models.beanie_models import Like, Review, LikeEntry
from commons.models.entity_models import AddLike
from pymongo.errors import DuplicateKeyError


class LikeService():
    @staticmethod
    async def create_like(
            like_info: AddLike,
    ) -> None:
        """Добавление лайка на рецензию."""

        if review := await Review.find_one(Review.review_id == like_info.review_id):
            try:
                await Like(**like_info.model_dump()).insert()
            except DuplicateKeyError:
                return None

            like_entry = LikeEntry(user_id=like_info.user_id, action=like_info.action)
            review.likes.append(like_entry)
            await review.save()

    @staticmethod
    async def delete_like(
            ReviewUserBase,
    ) -> None:
        """Удаление лайка с рецензии."""

        await Like.find_one(**ReviewUserBase.model_dump()).delete()

    @staticmethod
    async def get_user_likes(
            user_id: int,
            action: bool,
    ) -> list[Like]:
        """Получение пользовательских лайков на рецензии."""

        return await Like.find(
            Like.user_id == user_id,
            Like.action == action,
        ).to_list()
