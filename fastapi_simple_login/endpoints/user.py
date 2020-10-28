from typing import List
from fastapi import APIRouter, Depends, status

from fastapi_simple_login.db import User
from fastapi_simple_login.schema import UserCreate, UserUpdate, UserResponse
from fastapi_simple_login.security import get_current_user

router = APIRouter()


@router.get(path="/me", response_model=UserResponse)
def get_self_user(user: UserResponse = Depends(get_current_user)):
    return user


@router.get(path="/{email}", response_model=UserResponse)
def get_user(email: str):
    return User.get(field="email", value=email)


@router.post(
    path="",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    return User.create(
        email=user.email, name=user.name, password=user.password
    )


@router.put(path="/me", status_code=status.HTTP_204_NO_CONTENT)
def update_self_user(
    user_update: UserUpdate,
    user: UserResponse = Depends(get_current_user)
):
    User.update(field="email", value=user.email, **user_update.dict())


@router.put(path="/{email}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(email: str, user: UserUpdate):
    User.update(field="email", value=email, **user.dict())


@router.delete(path="/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_self_user(user: UserResponse = Depends(get_current_user)):
    User.delete(field="email", value=user.email)


@router.delete(path="/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: str):
    User.delete(field="email", value=email)


@router.get(path="", response_model=List[UserResponse]) # noqa)
def list_users():
    return User.list()
