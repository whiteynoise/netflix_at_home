import uuid

from db.postgres import Base
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String, Table,
                        UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_role_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE")
    ),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.role_id")),
    UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    schema="auth",
)


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", "email", name="uq_username_email"),
        {"schema": "auth", "comment": "Пользователи"},
    )

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)
    is_stuff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    outer_oauth_only = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=text("current_timestamp"))

    roles = relationship(
        "Roles", secondary=user_roles, back_populates="users", cascade="all, delete"
    )

    def __init__(
        self,
        username: str,
        password: str,
        email: str | None = None,
        phone: str | None = None,
        is_superuser: bool = False,
        outer_oauth_only: bool = False,
    ) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.phone = phone
        self.is_superuser = is_superuser
        self.outer_oauth_only = outer_oauth_only

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Roles(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), unique=True, nullable=False)
    users = relationship("Users", secondary=user_roles, back_populates="roles")


class LoginHistory(Base):
    __tablename__ = "login_history"
    __table_args__ = {"schema": "auth"}

    log_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="UUID лога"
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="UUID пользователя",
    )
    is_active = Column(
        Boolean, default=True, nullable=False, comment="Активен ли текущий логин"
    )
    login_date = Column(
        DateTime,
        default=text("current_timestamp"),
        nullable=False,
        comment="Дата логина",
    )
    token = Column(String(255), nullable=False, comment="Refresh токен")


class UserSocial(Base):
    __tablename__ = "user_social"
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_id_provider"),
        {"schema": "auth", "comment": "Привязанные соц.сети пользователей"},
    )

    user_social_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="UUID пользователя",
    )
    provider = Column(String(40), nullable=False, comment="Наименование соц.сети")
