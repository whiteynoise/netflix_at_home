from asyncio import TimeoutError as AsyncIoTimeout
from http import HTTPStatus
from typing import Annotated

import backoff
import core.session as session
from aiohttp import ClientError
from core.config import YNDX_AUTH_URL
from fastapi import Header, HTTPException


@backoff.on_exception(
    backoff.expo, (ClientError, HTTPException, AsyncIoTimeout), max_tries=5
)
async def get_user_info_yndx(
    yndx_user_token: Annotated[str, Header(alias="Authorization")],
) -> dict:
    """Получение информации о пользователе от Яндекса"""

    headers = {"Authorization": f"OAuth {yndx_user_token}"}

    async with session.aiohttp_session.get(
        YNDX_AUTH_URL, headers=headers, timeout=3
    ) as response:
        if response.status != 200:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
            )

        return await response.json()
