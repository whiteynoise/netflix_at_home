import uuid
from sqlalchemy import Column, UUID, String

from db.postgres import Base


class Template(Base):
    """Таблица шаблонов"""

    __tablename__ = "template"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, comment="Id шаблона", primary_key=True)
    path = Column(String, unique=True, comment="Путь до шаблона")

    """Таблица событий"""