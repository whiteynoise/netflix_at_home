from pydantic import BaseModel
from typing import Annotated
from fastapi import Query


class PaginatedParams(BaseModel):
    page_number: Annotated[int, Query(ge=1)] = 1
    page_size: Annotated[int, Query(ge=1)] = 50
