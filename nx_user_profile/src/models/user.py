import uuid

from sqlalchemy import Column, UUID, String

from db.postgres import Base


class UserProfile(Base):
    __tablename__ = "users_profile"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    avatar_path = Column(String, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.user_id}>"
