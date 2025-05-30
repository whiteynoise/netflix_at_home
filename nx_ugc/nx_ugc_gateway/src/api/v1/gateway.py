from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException


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
