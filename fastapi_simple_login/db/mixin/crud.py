import logging
from typing import TypeVar, Generic, Any, Optional, Type

from sqlalchemy.exc import SQLAlchemyError

from fastapi_simple_login.db import session
from fastapi_simple_login.exception import (
    CreateError,
    UpdateError,
    DeleteError,
    GetError
)

log = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")


class CRUD(Generic[ModelType]):

    @classmethod
    def create(cls: Type[ModelType], **kwargs) -> ModelType:
        try:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            log.info(f"Created {instance}")
        except SQLAlchemyError as e:
            raise CreateError(model=cls, params=kwargs) from e
        return instance

    @classmethod
    def get(cls, field: str, value: Any) -> Optional[ModelType]:
        try:
            instance = _get_query(cls, field, value).one_or_none()
            log.info(f"Fetched {instance}")
        except SQLAlchemyError as e:
            raise GetError(cls, field, value) from e
        return instance

    @classmethod
    def update(cls, field: str, value: Any, **kwargs) -> None:
        try:
            if _get_query(cls, field, value).update(kwargs) > 1:
                raise UpdateError(cls, field, value, unique=False)
            session.commit()
            log.info(f"Updated {cls.__name__} with params {kwargs}")
        except SQLAlchemyError as e:
            raise UpdateError(cls, field, value, kwargs) from e

    @classmethod
    def delete(cls, field: str, value: Any) -> None:
        try:
            if _get_query(cls, field, value).delete() > 1:
                raise DeleteError(cls, field, value, unique=False)
            session.commit()
            log.info(f"Deleted {cls.__name__}")
        except SQLAlchemyError as e:
            raise DeleteError(cls, field, value) from e


def _get_query(model: Type[ModelType], field: str, value: Any):
    return model.query.filter(getattr(model, field) == value)
