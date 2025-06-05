from http import HTTPStatus

from aiohttp import ClientError
from fastapi import Header, HTTPException, Request

from schemas.user import TokenPayload

from config import session, settings


async def get_user_from_auth_service(
    request: Request, authorization: str = Header(None)
) -> TokenPayload:
    """Запрос в nx_auth для получения информации о пользователе по токену."""

    if not authorization:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Missing Authorization header"
        )
    try:
        async with session.aiohttp_session.get(
            settings.auth_service_settings.auth_service_url,
            headers={"Authorization": authorization},
            timeout=5,
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
                )

            data = await response.json()
            request.state.user = TokenPayload(**data)

    except ClientError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Auth-service is unavailable"
        ) from e
