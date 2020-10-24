from enum import Enum, auto
from sqlalchemy import Column, String, DateTime, Enum as EnumType

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
    def list(cls):
        return cls.query.all()
