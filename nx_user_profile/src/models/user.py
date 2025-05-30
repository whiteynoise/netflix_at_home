import uuid

from sqlalchemy import Column, UUID, String, PrimaryKeyConstraint

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


class PinFilm(Base):
    __tablename__ = "pin_film"

    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    film_id = Column(UUID(as_uuid=True), default=uuid.uuid4)

    __table_args__ = (PrimaryKeyConstraint("user_id", "film_id"),)
