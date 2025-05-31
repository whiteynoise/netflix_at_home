from fastapi import APIRouter, Query, Request
from typing import Annotated

from commons.models.response_models import LikeList
from commons.services.likes import LikeService as ls

router = APIRouter()


@router.get(
    "/get_likes",
    response_model=list[LikeList],
    summary="Получение всех лайков/дизлайков юзера на рецензии",
    status_code=200,
)
async def get_user_likes(
        request: Request,
        action: Annotated[bool, Query(title="Лайк или дизлайк")] = True,
) -> list[LikeList]:
    return await ls.get_user_likes(
        user_id=request.state.user.user_id,
        action=action,
    )
