class LikeService():
    # TODO
    ...
#     async def create_like(
#             self,
#             user_id: int,
#             like: CreateLike,
#     ) -> None:
#         """Добавление лайка на рецензию."""

#         if review := await Review.find_one(Review.review_id == like.review_id):
#             try:
#                 await Like(**like.model_dump(), user_id=user_id).insert()
#             except DuplicateKeyError:
#                 raise HTTPException(
#                     status_code=HTTPStatus.CONFLICT,
#                     detail="Like in this review already exists.",
#                 )

#             like_entry = LikeEntry(user_id=user_id, action=like.action)
#             review.likes.append(like_entry)
#             await review.save()
#         else:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Review wasn't found.",
#             )

#         return None

#     async def get_user_likes(
#             self,
#             user_id: int,
#             action: bool,
#     ) -> list[LikeList]:
#         """Получение пользовательских лайков на рецензии."""

#         return await Like.find(
#             Like.user_id == user_id,
#             Like.action == action,
#         ).to_list()

#     async def delete_like(
#             self,
#             user_id: int,
#             review_id: str,

#                    ReviewUserBase
#     ) -> bool:
#         """Удаление лайка с рецензии."""

#         if not (
#             like := await Like.find_one(
#                 Like.review_id == review_id,
#                 Like.user_id == user_id,
#             )
#         ):
#             return False
        
#         await like.delete()

#         return True
