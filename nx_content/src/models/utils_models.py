from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class PaginatedParams(BaseModel):
    page_number: Annotated[int, Query(ge=1)] = 1
    page_size: Annotated[int, Query(ge=1)] = 50
