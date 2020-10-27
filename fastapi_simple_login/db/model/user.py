from typing import List
from datetime import datetime
from enum import Enum, auto
from sqlalchemy import Column, String, DateTime, Enum as EnumType

from fastapi_simple_login.db import session
from .. import Base, CRUD


class UserType(Enum):
    admin = auto()
    standard = auto()


class User(CRUD["Content"], Base):

    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime)
    user_type = Column(EnumType(UserType), default=UserType.standard)

    @classmethod
    def list(cls) -> List["User"]:
        return cls.query.all()

    @classmethod
    def login(cls, email: str, password: str, now: datetime) -> bool:
        validated = User.query \
            .filter(User.email == email) \
            .filter(User.password == password) \
            .update(dict(last_login=now)) == 1
        session.commit()
        return validated
