from beanie.operators import In
from pymongo.errors import DuplicateKeyError

from commons.models.beanie_models import Bookmark
from commons.models.entity_models import AddToBookmark, DelFromBookmark, BookmarkBase


class BookmarkService():
    @staticmethod
    async def add_to_bookmark(
            bookmark_info: AddToBookmark,
    ) -> None:
        """Создание контентной закладки."""

        try:
            await Bookmark(**bookmark_info.model_dump()).insert()
        except DuplicateKeyError:
            pass

    @staticmethod
    async def delete_from_bookmark(
            bookmark_info: DelFromBookmark,
    ) -> None:
        """Удаление контента из закладки."""

        await Bookmark.find(
            Bookmark.bookmark_name == bookmark_info.bookmark_name,
            Bookmark.user_id == bookmark_info.user_id,
            In(Bookmark.film_id, bookmark_info.film_ids),
        ).delete()

    @staticmethod
    async def get_bookmark_info(
            user_id: int,
            bookmark_info: BookmarkBase,
    ) -> list[Bookmark]:
        """Получение списка контента в закладке."""

        bm_movies = await Bookmark.find(
            Bookmark.bookmark_name == bookmark_info.bookmark_name,
            Bookmark.user_id == user_id,
        ).to_list()

        return bm_movies
