from fastapi import APIRouter

router = APIRouter(prefix="/token", tags=["auth"])


@router.post("/")
async def renew_access_token():
    '''Обновление access-токена'''
    pass

