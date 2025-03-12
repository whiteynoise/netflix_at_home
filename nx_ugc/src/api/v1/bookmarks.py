from http import HTTPStatus

from beanie.operators import In
from fastapi import APIRouter, HTTPException, Request
from models.beanie_models import Bookmark
from models.entity_models import BookmarkAdd, BookmarkBase, BookmarkDel
from models.response_models import BookmarkResp
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.post(
    "/add_to_bookmark",
    response_model=bool,
    summary="Добавление контента в закладку",
    description="Добавление контента в пользовательскую закладку",
    status_code=201
)
async def add_to_bookmark(
    request: Request,
    bookmark_info: BookmarkAdd,
) -> None:
    """Создание контентной закладки."""

    try:
        await Bookmark(
            **bookmark_info.model_dump(), user_id=request.state.user.user_id
        ).insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Film in this bookmark already exists.",
        )

    return


@router.post(
    "/delete_from_bookmark",
    response_model=bool,
    summary="Удаление контента из закладки",
    description="Удаление контента из пользовательской закладки",
    status_code=200
)
async def delete_from_bookmark(
    request: Request,
    bookmark_info: BookmarkDel,
) -> None:
    """Удаление контента из закладки."""

    await Bookmark.find(
        Bookmark.bookmark_name == bookmark_info.bookmark_name,
        Bookmark.user_id == request.state.user.user_id,
        In(Bookmark.film_id, bookmark_info.film_ids),
    ).delete()

    return


@router.get(
    "/get_bookmark_info",
    response_model=list[BookmarkResp],
    summary="Получение списка контента в закладке",
    description="Получение списка контента в пользовательской закладке",
    status_code=200
)
async def get_bookmark_info(
    request: Request,
    bookmark_info: BookmarkBase,
) -> list[BookmarkResp]:
    """Получение списка контента в закладке."""

    bm_movies = await Bookmark.find(
        Bookmark.bookmark_name == bookmark_info.bookmark_name,
        Bookmark.user_id == request.state.user.user_id,
    ).to_list()

    return bm_movies
