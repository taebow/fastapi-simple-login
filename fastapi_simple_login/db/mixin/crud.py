import logging
from typing import TypeVar, Generic, Any, Optional, Type

from sqlalchemy.exc import SQLAlchemyError

from ...db import session
from ...db.exception import (
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
            instance: ModelType = cls(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            log.info(f"Created {instance}")
        except SQLAlchemyError:
            raise CreateError(model=cls, params=kwargs)
        return instance

    # noinspection PyShadowingBuiltins
    @classmethod
    def get(cls: ModelType, id: Any) -> Optional[ModelType]:
        try:
            instance = cls.query.filter(cls.id == id).first()
            log.info(f"Fetched {instance}")
        except SQLAlchemyError:
            raise GetError(model=cls, id=id)
        return instance

    def update(self: ModelType, **kwargs) -> ModelType:
        try:
            for attr, value in kwargs.items():
                setattr(self, attr, value)

            session.add(self)
            session.commit()
            session.refresh(self)
            log.info(f"Updated {self} with params {kwargs}")
        except SQLAlchemyError:
            raise UpdateError(self)
        return self

    def delete(self: ModelType) -> bool:
        try:
            session.delete(self)
            session.commit()
            log.info(f"Deleted {self}")
        except SQLAlchemyError:
            session.rollback()
            if type(self).query.filter(type(self).id == self.id).first():
                raise DeleteError(self)
            return False
        return True
