from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email_update: Optional[str]
    password: Optional[str]
    name: Optional[str]


class UserDelete(BaseModel):
    email: str


class UserResponse(UserBase):
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

