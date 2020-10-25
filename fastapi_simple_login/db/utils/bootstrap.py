import logging
from contextlib import suppress

from sqlalchemy.exc import SQLAlchemyError

from fastapi_simple_login.exception import ServerError
from fastapi_simple_login.config import settings
from fastapi_simple_login.db.model import User, UserType

from .schema_init import create_all
from .session_manager import SessionManager, session

log = logging.getLogger(__name__)


def create_root_user():
    User.create(
        email=settings.ROOT_EMAIL,
        password=settings.ROOT_PASSWORD,
        name="Root user",
        user_type=UserType.admin.name
    )


def bootstrap(reset=False):
    with SessionManager():
        with suppress(SQLAlchemyError):
            create_all(reset)

        try:
            create_root_user()
            log.info("Root user initiated")
        except ServerError as e:
            session.rollback()
            root_user = User.query \
                .filter(User.email == settings.ROOT_EMAIL) \
                .first()
            if not root_user:
                raise ServerError("Cannot initiate root user") from e
