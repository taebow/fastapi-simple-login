from datetime import datetime
from fastapi import APIRouter, HTTPException

from fastapi_simple_login.db import User
from fastapi_simple_login.security import create_token
from fastapi_simple_login.schema import LoginInput, LoginOutput


from fastapi_simple_login.config import settings

router = APIRouter()


@router.post("/login", response_model=LoginOutput)
def login(login_input: LoginInput):
    now = datetime.utcnow()

    if User.login(login_input.email, login_input.password, now):
        return {
            "status": "Authorized",
            "token": create_token(login_input.email, now)
        }

    raise HTTPException(
        status_code=401,
        detail="Unauthorized"
    )

