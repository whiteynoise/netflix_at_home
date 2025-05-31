from fastapi import APIRouter, HTTPException, Body, Request
from pydantic import ValidationError

from starlette.status import HTTP_400_BAD_REQUEST

from commons.shared_config import SERVICE_INFO_BY_TOPIC

from producer import kafka_producer

from schemas.event import BaseEvent

router = APIRouter(tags=["UGC Gateway"])

# TODO: 1. Поднять KafkaProducer (aiokafka) с возможностью записи в разные топики, часть settings уже лежит в commons, список возможных топиков можно сформировать из ключей SERVICE_INFO_BY_TOPIC
# TODO: 2. Добавить проверку доступных методов (через дикт SERVICE_INFO_BY_TOPIC), при неправильном методе сообщения отбрасывать сразу
# TODO: 3. Валидация данных через схемы методов классов, отбрасывать неправильное сразу
# TODO: 4. Написать фастапишный main.py (за реф можно взять nx_ugc_api, выкинув лишнее), добавить чекер токена auth с получением юзера middleware, реф на основном API сервиса, все общее для сервисов лежит в commons, если не лежит, то добавь
# TODO: 5. (!!!) user_id распаковывать в каждое сообщение как часть payload (!!!)
# TODO: 6. Реализовать фильтрацию для метода добавления/обновления рецензии (ДЕЛАЙ ЭТО В ПОСЛЕДНЮЮ ОЧЕРЕДЬ)
# TODO: 7. Структура сообщения представлена ниже, с неймингом топиков и методов можно ознакомиться в SERVICE_INFO_BY_TOPIC (commons.shared_configs)

"""
    {
        "topic": "ugc_ratings",
        "method": "add_rating",
        "payload": {
            "film_id": "tt1234567",
            "user_id": "ef123123",
            "rating": 5
        }
    }
"""


@router.post("/send_ugc_event", summary="Отправка эвентов ugc", status_code=201)
async def send_ugc_event(
    request: Request,
    topic: str = Body(..., embed=True),
    method: str = Body(..., embed=True),
    payload: dict = Body(..., embed=True),
):
    """Обработчик событий UGC"""
    topic_info = SERVICE_INFO_BY_TOPIC.get(topic)
    if not topic_info:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unknown topic")

    payload["user_id"] = request.state.user.user_id

    schema_class = topic_info["service_methods_schemes"].get(method)
    if not schema_class:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Unknown action for this topic"
        )

    try:
        validated_payload = schema_class(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e.errors()) from e

    event = BaseEvent(topic=topic, method=method, payload=validated_payload.model_dump())

    await kafka_producer.send(topic, event.model_dump())

    return {"status": "sent"}
