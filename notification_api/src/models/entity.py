import uuid

from sqlalchemy import Column, UUID, String, DateTime, Enum, Text, JSON


from db.postgres import Base
from models.constants import VolumeEventType


class Event(Base):
    """Таблица событий"""

    __tablename__ = "event"

    id = Column(
        UUID(as_uuid=True), default=uuid.uuid4, comment="Id шаблона", primary_key=True
    )
    title = Column(String, nullable=False, comment="Название события")
    description = Column(Text, nullable=True)
    time = Column(DateTime(timezone=True), nullable=True)
    volume_type = Column(Enum(VolumeEventType), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    roles = Column(JSON, nullable=False, default=list)
    template_id = Column(UUID(as_uuid=True), nullable=False)
