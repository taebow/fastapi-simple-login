from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


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

