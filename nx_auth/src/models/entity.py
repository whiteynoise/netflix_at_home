import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment='UUID пользователя'
    )
    login = Column(
        String(255),
        unique=True,
        nullable=False,
        comment='Логин пользователя'
    )
    password = Column(
        String(255), nullable=False, comment='Пароль пользователя'
    )
    first_name = Column(
        String(50), nullable=True, comment='Имя пользователя'
    )
    last_name = Column(
        String(50), nullable=True, comment='Фамилия пользователя'
    )
    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
        comment='Дата создания профиля'
    )
    is_staff = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='Является ли пользователь сотрудником'
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment='Активен ли аккаунт пользователя'
    )
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='Имеет ли пользователь права супер пользователя'
    )

    def __init__(self, login: str, password: str, first_name:str, last_name: str) -> None:
        self.login = login
        self.password = self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'
    

class LoginHistory(Base):
    __tablename__ = 'login_history'
    __table_args__ = {'schema': 'auth'}

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment='UUID лога'
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.user_id'),
        nullable=False,
        comment='UUID пользователя'
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment='Активен ли текущий логин'
    )
    login_date = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
        comment='Дата логина'
    )
    token = Column(
        String(255), nullable=False, comment='Refresh токен'
    )


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'auth'}

    role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment='UUID роли'
    )
    name_role = Column(
        String(255), nullable=False, comment='Наименование роли'
    )


class UserRoles(Base):
    __tablename__ = 'user_roles'
    __table_args__ = {'schema': 'auth'}

    user_role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment='UUID пользователя-роли'
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.user_id'),
        nullable=False,
        comment='UUID пользователя'
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey('roles.role_id'),
        nullable=False,
        comment='UUID роли'
    )
