from asyncio import TimeoutError as AsyncIoTimeout
from http import HTTPStatus

import backoff
import core.session as session
from aiohttp import ClientError
from core.config import PROVIDERS_URL
from fastapi import HTTPException
from schemas.integration import UniUserOAuth


@backoff.on_exception(
    backoff.expo, (ClientError, HTTPException, AsyncIoTimeout), max_tries=5
)
async def get_user_info_oauth(provider: str, oauth_token: str) -> UniUserOAuth:
    """Получение информации о пользователе от внешнего OAuth."""

    if not (provider_url := PROVIDERS_URL.get(provider)):
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")

    headers = {"Authorization": f"OAuth {oauth_token}"}

    async with session.aiohttp_session.get(
        provider_url, headers=headers, timeout=3
    ) as response:
        if response.status != 200:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
            )

        res = await response.json()

    return UniUserOAuth(**res)
