import uuid

from sqlalchemy import Boolean, Column, DateTime, String, Table, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres import Base


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_role_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.user_id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.role_id')),
    UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
    schema='auth',
)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username', 'email', name='uq_username_email'),
        {
            'schema': 'auth',
            'comment': 'Пользователи'
        },
    )

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))

    is_active = Column(Boolean, nullable=False, default=True)
    is_stuff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=text('current_timestamp'))

    roles = relationship('Roles', secondary=user_roles, back_populates='users')

    def __init__(
        self,
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        is_superuser: bool = False
    ) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>' 
    

class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'auth'}

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), unique=True, nullable=False)
    users = relationship('Users', secondary=user_roles, back_populates='roles')
    

class LoginHistory(Base):
    __tablename__ = 'login_history'
    __table_args__ = {'schema': 'auth'}

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
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
        default=text('current_timestamp'),
        nullable=False,
        comment='Дата логина'
    )
    token = Column(
        String(255), nullable=False, comment='Refresh токен'
    )
