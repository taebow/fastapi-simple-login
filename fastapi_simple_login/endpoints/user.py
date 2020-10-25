from typing import List
from fastapi import APIRouter

from fastapi_simple_login.db import User
from fastapi_simple_login.schema.user import (
    UserCreate, UserUpdate, UserDelete, UserResponse
)

router = APIRouter()


@router.get("/{email}", response_model=UserResponse)
def get_user(email: str):
    return User.get(field="email", value=email)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    return User.create(
        email=user.email,
        name=user.name,
        password=user.password
    )


@router.put("/")
def update_user(user: UserUpdate):
    update_values = dict(
        email=user.email_update,
        name=user.name,
        password=user.password
    )
    update_values = {k: v for k, v in update_values.items() if v}
    User.update(field="email", value=user.email, **update_values)


@router.delete("/")
def delete_user(user: UserDelete):
    User.delete(field="email", value=user.email)


@router.get("/", response_model=List[UserResponse])
def index():
    return User.query.all()
