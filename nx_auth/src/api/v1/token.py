from fastapi import APIRouter

router = APIRouter(tags=["token"])


@router.post("/")
async def renew_access_token():
    '''Обновление access-токена'''
    pass

