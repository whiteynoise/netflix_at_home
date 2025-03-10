from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Request
from models.beanie_models import Like, LikeEntry, Review
from models.entity_models import CreateLike
from models.response_models import LikeList
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.post("/create_like", summary="Добавление лайка на рецензию")
async def create_like(request: Request, like: CreateLike) -> bool:
    """Доабвление лайка на рецензию"""
    try:
        await Like(**like.model_dump(), user_id=request.state.user.user_id).insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Like in this review already exists.",
        )
    review = await Review.find_one(Review.review_id == like.review_id)

    like_entry = LikeEntry(user_id=request.state.user.user_id, action=like.action)
    review.likes.append(like_entry)
    await review.save()

    return True


@router.get("/get_likes", summary="Получение всех лайков/дизлайков юзера на рецензии")
async def get_user_likes(
    request: Request, action: Annotated[bool, Query(title="Лайк или дизлайк")] = True
) -> list[LikeList]:
    return await Like.find(
        Like.user_id == request.state.user.user_id, Like.action == action
    ).to_list()


@router.delete("/delete_like/{review_id}", summary="Удаление лайка на рецензию")
async def delete_like(
    request: Request, review_id: Annotated[str, Path(title="Id ревью")]
) -> bool:
    like = await Like.find_one(
        Like.review_id == review_id, Like.user_id == request.state.user.user_id
    )
    if not like:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Like in this review does not exists.",
        )
    await like.delete()
    return True
