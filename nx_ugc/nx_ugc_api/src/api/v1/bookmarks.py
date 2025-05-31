from fastapi import APIRouter, Request

from commons.models.entity_models import BookmarkBase
from commons.models.response_models import BookmarkResp
from commons.services.bookmarks import BookmarkService as bs

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
) -> list[BookmarkResp]:
    return await bs.get_bookmark_info(
        user_id=request.state.user.user_id,
        bookmark_info=bookmark_info,
    )
