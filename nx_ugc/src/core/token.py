import core.session as session
from aiohttp import ClientError
from http import HTTPStatus
from fastapi import Header, HTTPException, Request
from models.entity_models import TokenPayload

from core.config import AUTH_SERVICE_URL


async def get_user_from_auth_service(
    request: Request, authorization: str = Header(None)
) -> TokenPayload:
    """Запрос в nx_auth для получения информации о пользователе по токену."""

    if not authorization:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Missing Authorization header"
        )

    ENDPOINT = "/api/v1/token/get_user_from_token"

    try:
        async with session.aiohttp_session.get(
            f"{AUTH_SERVICE_URL}{ENDPOINT}",
            headers={"Authorization": authorization},
            timeout=5,
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
                )

            data = await response.json()
            request.state.user = TokenPayload(**data)

    except ClientError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Auth-service is unavailable"
        )
