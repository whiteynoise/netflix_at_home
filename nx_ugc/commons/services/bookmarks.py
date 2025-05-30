from beanie.operators import In
from commons.models.beanie_models import Bookmark
from commons.models.entity_models import AddToBookmark, DelFromBookmark, BookmarkBase
from commons.models.response_models import BookmarkResp
from pymongo.errors import DuplicateKeyError


class BookmarkService():
    async def add_to_bookmark(
            bookmark_info: AddToBookmark,
    ) -> bool:
        """Создание контентной закладки."""

        result = True

        try:
            await Bookmark(
                **bookmark_info.model_dump(),
            ).insert()
        except DuplicateKeyError:
            result = False
        
        return result

    async def delete_from_bookmark(
            bookmark_info: DelFromBookmark,
    ) -> bool:
        """Удаление контента из закладки."""

        await Bookmark.find(
            Bookmark.bookmark_name == bookmark_info.bookmark_name,
            Bookmark.user_id == bookmark_info.user_id,
            In(Bookmark.film_id, bookmark_info.film_ids),
        ).delete()

        return True

    async def get_bookmark_info(
            user_id: int,
            bookmark_info: BookmarkBase,
    ) -> list[BookmarkResp]:
        """Получение списка контента в закладке."""

        bm_movies = await Bookmark.find(
            Bookmark.bookmark_name == bookmark_info.bookmark_name,
            Bookmark.user_id == user_id,
        ).to_list()

        return bm_movies
