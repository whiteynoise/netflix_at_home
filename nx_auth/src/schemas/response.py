from uuid import UUID

from pydantic import BaseModel


class GetRolesResponse(BaseModel):
    role_id: UUID
    title: str

    class Config:
        orm_mode = True
        