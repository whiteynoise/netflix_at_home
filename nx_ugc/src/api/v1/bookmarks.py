from pymongo.errors import DuplicateKeyError
from beanie.operators import In
from fastapi import APIRouter, Request, HTTPException
from http import HTTPStatus

from models.beanie_models import Bookmark
from models.entity_models import BookmarkAdd, BookmarkDel, BookmarkBase
from models.response_models import BookmarkResp

router = APIRouter()


@router.post(
    '/add_to_bookmark',
    response_model=bool,
    summary='Добавление контента в закладку',
    description='Добавление контента в пользовательскую закладку',
)
async def add_to_bookmark(
        request: Request,
        bookmark_info: BookmarkAdd,
) -> bool:
    '''Создание контентной закладки.'''
    
    try:
        await Bookmark(
            **bookmark_info.model_dump(),
            user_id = request.state.user.user_id
        ).insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Film in this bookmark already exists."
        )

    return True


@router.post(
    '/delete_from_bookmark',
    response_model=bool,
    summary='Удаление контента из закладки',
    description='Удаление контента из пользовательской закладки',
)
async def delete_from_bookmark(
        request: Request,
        bookmark_info: BookmarkDel,
) -> bool:
    '''Удаление контента из закладки.'''

    await Bookmark.find(
        Bookmark.bookmark_name == bookmark_info.bookmark_name,
        Bookmark.user_id == request.state.user.user_id,
        In(Bookmark.film_id, bookmark_info.film_ids),
    ).delete()

    return True


@router.get(
    '/get_bookmark_info',
    response_model=list[BookmarkResp],
    summary='Получение списка контента в закладке',
    description='Получение списка контента в пользовательской закладке',
)
async def get_bookmark_info(
        request: Request,
        bookmark_info: BookmarkBase,
) -> list[BookmarkResp]:
    '''Получение списка контента в закладке.'''

    bm_movies = await Bookmark.find(
        Bookmark.bookmark_name == bookmark_info.bookmark_name,
        Bookmark.user_id == request.state.user.user_id,
    ).to_list()
    
    return bm_movies
