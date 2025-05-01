import os
import shutil
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.constants import (
    REGULAR_NOTIFICATION_SERVICE_API,
    INSTANCE_NOTIFICATION_SERVICE_API,
    EventType,
)
from config import session
from db.postgres import get_session
from models.entity import Template

from models.response import TemplateCommon, CreateEventSchema

router = APIRouter(tags=["Шаблоны"])


@router.post("/upload_template", summary="Загрузить шаблон")
async def upload_file(
    db: Annotated[AsyncSession, Depends(get_session)],
    file: UploadFile = File(...),
):
    _, ext = os.path.splitext(file.filename)

    if ext != ".html":
        raise HTTPException(status_code=400, detail="Можно загружать только .html")

    upload_dir = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(upload_dir, file.filename)

    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    template = Template(path=dest)
    db.add(template)
    await db.commit()

    return {"filename": file.filename}


@router.get("/templates", summary="Получение всех шаблонов")
async def get_templates(
    db: Annotated[AsyncSession, Depends(get_session)],
) -> List[TemplateCommon]:
    result = await db.execute(select(Template))
    templates = result.scalars().all()
    return templates


@router.post("/create_event", summary="Отправить событие", status_code=201)
async def create_event(event: Annotated[CreateEventSchema, Body(...)]) -> None:
    print(event.model_dump())

    match event.type:
        case EventType.INSTANCE.value:
            url = INSTANCE_NOTIFICATION_SERVICE_API
        case EventType.REGULAR.value:
            url = REGULAR_NOTIFICATION_SERVICE_API

    async with session.aiohttp_session.post(url, json=event.model_dump(mode='json')) as response:
        if response.status not in (200, 201):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Create event: error",
            )
