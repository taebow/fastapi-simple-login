from typing import List, Any
from datetime import datetime
from enum import Enum, auto
from sqlalchemy import Column, String, DateTime, Enum as EnumType, func

from fastapi_simple_login.db import session
from .. import Base, CRUD


class UserType(Enum):
    admin = auto()
    standard = auto()


class User(CRUD["Content"], Base):

    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String, nullable=False)
    last_login = Column(DateTime)
    user_type = Column(EnumType(UserType), default=UserType.standard)

    @classmethod
    def list(cls) -> List["User"]:
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs) -> "User":
        kwargs = password_to_hash(kwargs)
        return super().create(**kwargs)

    @classmethod
    def update(cls, field: str, value: Any, **kwargs):
        kwargs = password_to_hash(kwargs)
        return super().update(
            field=field,
            value=value,
            **{k: v for k, v in kwargs.items() if v is not None}
        )

    @classmethod
    def login(cls, email: str, password: str, now: datetime) -> bool:

        password_hash = get_password_hash(password, User.password_hash)
        validated = User.query \
            .filter(User.email == email) \
            .filter(User.password_hash == password_hash) \
            .update(dict(last_login=now), synchronize_session=False) == 1
        session.commit()
        return validated


def password_to_hash(kwargs):
    password = kwargs.pop("password", None)
    if password:
        kwargs["password_hash"] = get_password_hash(password)
    return kwargs


def get_password_hash(password, salt=None):
    salt = salt or func.gen_salt("md5")
    return func.crypt(password, salt)
