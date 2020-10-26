from fastapi import APIRouter, Depends

from fastapi_simple_login.security import get_current_user
from fastapi_simple_login.schema.user import UserResponse

router = APIRouter()


@router.get("/public")
def get_public_resource():
    return {"status": "ok"}


@router.get("/protected")
def get_protected_endpoint(_: UserResponse = Depends(get_current_user)):
    return {"status": "ok"}
