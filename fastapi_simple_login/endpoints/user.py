from typing import List
from fastapi import APIRouter, status

from fastapi_simple_login.db import User
from fastapi_simple_login.schema.user import (
    UserCreate, UserUpdate, UserResponse
)
router = APIRouter()


@router.get(
    path="/{email}",
    response_model=UserResponse
)
def get_user(email: str):
    return User.get(field="email", value=email)


@router.post(
    path="",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    return User.create(
        email=user.email,
        name=user.name,
        password=user.password
    )


@router.put(
    path="/{email}",
    status_code=status.HTTP_204_NO_CONTENT
)
def update_user(email: str, user: UserUpdate):
    User.update(
        field="email",
        value=email,
        **{k: v for k, v in user if v is not None}
    )


@router.delete(
    path="/{email}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(email: str):
    User.delete(field="email", value=email)


@router.get(
    path="",
    response_model=List[UserResponse]
)
def index():
    return User.list()
