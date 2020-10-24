from fastapi import APIRouter

from fastapi_simple_login.db import User

router = APIRouter()


@router.get("/")
def get_user():
    return User.query.first()
