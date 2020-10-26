from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

from fastapi_simple_login.db import User
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import jwt

from fastapi_simple_login.config import settings

router = APIRouter()


from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str


class LoginOutput(BaseModel):
    status: str
    token: str


@router.post("/login", response_model=LoginOutput)
def login(login_input: LoginInput):
    now = datetime.utcnow()

    if User.login(login_input.email, login_input.password, now):
        return {"status": "ok", "token": create_token(login_input.email, now)}

    raise HTTPException(
        status_code=401,
        detail="Unauthorized"
    )


def create_token(email, now):
    return jsonable_encoder(
        jwt.encode(
            dict(
                sub=email,
                iss=settings.ORIGIN,
                iat=to_timestamp(now),
                exp=to_timestamp(now+timedelta(days=14))
            ),
            settings.CLIENT_SECRET
        )
    )


def to_timestamp(dt):
    return str(int(dt.timestamp()))
