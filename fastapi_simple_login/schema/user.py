from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserType(Enum):
    standard = "standard"
    admin = "admin"


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[str]
    password: Optional[str]
    name: Optional[str]


class UserResponse(UserBase):
    last_login: Optional[datetime]

    class Config:
        orm_mode = True


class UserInDB(UserResponse):
    user_type: UserType
