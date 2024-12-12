import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres import Base


user_roles = Table(
    'user_roles',
    Base.metadata,
        Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
        Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
        UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String, nullable=True, index=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50))

    is_active= Column(Boolean, default=True)
    is_stuff = Column(Boolean, default=False)
    is_superuser = is_stuff = Column(Boolean(), default=False)

    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    roles = relationship('Role', secondary=user_roles, back_populates='users')

    def __init__(self, username: str, password: str, first_name:str, last_name: str) -> None:
        self.username = username
        self.password = self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>' 
    

class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(255), unique=True, nullable=False, index=True)
    users = relationship('User', secondary=user_roles, back_populates='roles')

    def __repr__(self) -> str:
        return f'<User {self.title}>' 
