from fastapi import APIRouter, HTTPException, Body, Request
from pydantic import ValidationError

from starlette.status import HTTP_400_BAD_REQUEST

from commons.shared_config import SERVICE_INFO_BY_TOPIC

from producer import kafka_producer

from schemas.event import BaseEvent

router = APIRouter(tags=["UGC Gateway"])


@router.post(
    "/send_ugc_event",
    summary="Отправка эвентов ugc",
    status_code=201,
)
async def send_ugc_event(
        request: Request,
        topic: str = Body(..., embed=True),
        method: str = Body(..., embed=True),
        payload: dict = Body(..., embed=True),
):
    """Обработчик событий UGC"""
    topic_info = SERVICE_INFO_BY_TOPIC.get(topic)
    if not topic_info:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unknown topic",
        )

    payload["user_id"] = request.state.user.user_id

    schema_class = topic_info["service_methods_schemes"].get(method)
    if not schema_class:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Unknown action for this topic",
        )

    try:
        validated_payload = schema_class(**payload)
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        ) from e

    event = BaseEvent(topic=topic, method=method, payload=validated_payload.model_dump())

    await kafka_producer.send(topic, event.model_dump())

    return {"status": "sent"}
