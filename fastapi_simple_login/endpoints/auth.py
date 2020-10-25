from datetime import datetime, timedelta
from fastapi import APIRouter

from fastapi_simple_login.db import User
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import jwt

from fastapi_simple_login.config import settings

router = APIRouter()


@router.post("/login")
def login(email: str, password: str):
    now = datetime.utcnow()

    if User.login(email, password, now):
        return {"status": "ok", "token": create_token(email, now)}

    return JSONResponse(
        status_code=401,
        content={"status": "unauthorized"}
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