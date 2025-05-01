import os
import shutil
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.constants import TEMPLATE_PATH
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

    upload_dir = os.path.join(os.getcwd(), TEMPLATE_PATH)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(TEMPLATE_PATH, file.filename)

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
