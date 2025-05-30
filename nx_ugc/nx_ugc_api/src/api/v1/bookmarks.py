from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request, Depends
from models.entity_models import BookmarkAdd, BookmarkBase, BookmarkDel
from models.response_models import BookmarkResp
from services.bookmarks import bookmark_service, BookmarkService

router = APIRouter()


@router.get(
    "/get_bookmark_info",
    response_model=list[BookmarkResp],
    summary="Получение списка контента в закладке",
    description="Получение списка контента в пользовательской закладке",
    status_code=200,
)
async def get_bookmark_info(
        request: Request,
        bookmark_info: BookmarkBase,
        bs: BookmarkService = Depends(bookmark_service.get_service),
) -> list[BookmarkResp]:
    return await bs.get_bookmark_info(
        user_id=request.state.user.user_id,
        bookmark_info=bookmark_info,
    )
