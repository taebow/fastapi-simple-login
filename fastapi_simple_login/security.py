from datetime import timedelta
import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security.base import SecurityBase, SecurityBaseModel
from starlette import status as status_code

from .config import settings
from .db import User


class EmailPasswordAuth(SecurityBase):
    def __init__(self):
        self.model = SecurityBaseModel(type="http")
        self.scheme_name = "Authorization"

    def __call__(self, request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer"):
            raise HTTPException(
                status_code=status_code.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        token = token[len("Bearer "):]

        try:
            payload = jwt.decode(
                token,
                settings.CLIENT_SECRET,
                algorithms="HS256"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status_code.HTTP_403_FORBIDDEN,
                detail="Authentication error"
            )
        return payload


email_password_auth = EmailPasswordAuth()


def get_current_user(token_dict: dict = Depends(email_password_auth)):
    email = token_dict.get("sub")
    user = User.get(field="email", value=email)

    if not user:
        raise HTTPException(
            status_code=status_code.HTTP_403_FORBIDDEN,
            detail="Authentication error"
        )

    return user


def create_token(email, now):
    return jsonable_encoder(
        jwt.encode(
            dict(
                sub=email,
                iss=settings.ORIGIN,
                iat=str(int(now.timestamp())),
                exp=str(int((now+timedelta(days=14)).timestamp()))
            ),
            settings.CLIENT_SECRET
        )
    )
