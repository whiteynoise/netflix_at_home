import time

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from redis.asyncio import Redis
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.responses import JSONResponse, Response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения кол-ва поступаемых запросов"""

    RATE_LIMIT = 20
    WINDOW_SIZE = 60

    def __init__(self, app: FastAPI, redis_: Redis):
        super().__init__(app)
        self.redis_ = redis_

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        is_rate_limit: bool = await self.is_rate_limit(request.client.host)

        if is_rate_limit:
            return JSONResponse({"detail": "Too many requests"}, status_code=429)
        return await call_next(request)

    async def is_rate_limit(self, host: str) -> bool:
        """
        С помощью метода скользящего окна проверяем достигнут ли лимит по кол-ву запросов у юзера
        """

        async with self.redis_.pipeline() as pipe:
            await pipe.lpush(host, time.time())
            await pipe.ltrim(
                host, 0, self.WINDOW_SIZE - 1
            )  # нас интересуют запросы за прошедшие 60 сек
            await pipe.expire(host, self.WINDOW_SIZE)
            result = await pipe.execute()

        result = result[0]

        # N или менее запросов - лимит не превышен
        if result <= self.RATE_LIMIT:
            return False

        result_data = await self.redis_.lrange(host, 0, -1)

        # самая старая запись должна быть старше, чем минута
        return time.time() - float(result_data[-1]) <= self.WINDOW_SIZE


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки request_id и записи его в спан"""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-Id")

        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "X-Request-Id is required"},
            )

        tracer = trace.get_tracer(__name__)

        with tracer.start_as_current_span("auth-request-span") as span:
            if request_id:
                span.set_attribute("http.request_id", request_id)

            response = await call_next(request)

        return response
