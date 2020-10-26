from typing import List
from fastapi import APIRouter

from fastapi_simple_login.db import User
from fastapi_simple_login.schema.user import (
    UserCreate, UserUpdate, UserResponse
)
router = APIRouter()


@router.get("/{email}", response_model=UserResponse)
def get_user(email: str):
    return User.get(field="email", value=email)


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    return User.create(
        email=user.email,
        name=user.name,
        password=user.password
    )


@router.put("/{email}")
def update_user(email: str, user: UserUpdate):
    User.update(
        field="email",
        value=email,
        **{k: v for k, v in user if v is not None}
    )


@router.delete("/{email}")
def delete_user(email: str):
    User.delete(field="email", value=email)


@router.get("", response_model=List[UserResponse])
def index():
    return User.list()
