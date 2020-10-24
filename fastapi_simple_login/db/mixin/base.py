from sqlalchemy import Column, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID

from .. import session
from ..utils import camel_to_snake_case


@as_declarative()
class Base:
    __abstract__ = True

    query = session.query_property()

    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())

    @declared_attr
    def __tablename__(cls) -> str: # noqa
        return camel_to_snake_case(cls.__name__)
