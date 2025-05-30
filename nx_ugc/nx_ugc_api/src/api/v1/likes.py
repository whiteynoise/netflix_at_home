from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Request, Depends
from models.beanie_models import Like, LikeEntry, Review
from models.entity_models import CreateLike
from models.response_models import LikeList
from pymongo.errors import DuplicateKeyError
from services.likes import like_service, LikeService

router = APIRouter()


@router.post(
    "/create_like",
    response_model=bool,
    summary="Добавление лайка на рецензию",
    status_code=201,
)
async def create_like(
        request: Request,
        like: CreateLike,
        ls: LikeService = Depends(like_service.get_service),
) -> None:
    """Доабвление лайка на рецензию"""
    # TODO:
    if review := await Review.find_one(Review.review_id == like.review_id):
        try:
            await Like(**like.model_dump(), user_id=request.state.user.user_id).insert()
        except DuplicateKeyError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Like in this review already exists.",
            )

        like_entry = LikeEntry(user_id=request.state.user.user_id, action=like.action)
        review.likes.append(like_entry)
        await review.save()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Review wasn't found.",
        )

    return


@router.get(
    "/get_likes",
    response_model=list[LikeList],
    summary="Получение всех лайков/дизлайков юзера на рецензии",
    status_code=200,
)
async def get_user_likes(
        request: Request,
        action: Annotated[bool, Query(title="Лайк или дизлайк")] = True,
        ls: LikeService = Depends(like_service.get_service),
) -> list[LikeList]:
    return await ls.get_user_likes(
        user_id=request.state.user.user_id,
        action=action,
    )


@router.delete(
    "/delete_like/{review_id}",
    response_model=bool,
    summary="Удаление лайка на рецензию",
    status_code=200,
)
async def delete_like(
        request: Request,
        review_id: Annotated[str, Path(title="Id ревью")],
        ls: LikeService = Depends(like_service.get_service),
) -> bool:
    if not await ls.delete_like(
        user_id=request.state.user.user_id,
        review_id=review_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Like in this review does not exists.",
        )
    
    return True
