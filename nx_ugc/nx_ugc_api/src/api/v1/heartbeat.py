from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.post("/ping", summary="Пинг", status_code=200)
async def create_like() -> str:
    logger.info("Pong!")
    return "Pong from ugc-service!"
