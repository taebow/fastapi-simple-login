from __future__ import annotations
from contextvars import ContextVar
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fastapi_simple_login.config import settings
from ..exception import MissingSessionError

_session: ContextVar[Optional[Session]] = ContextVar("_session", default=None)


class SessionManager(object):

    def __init__(self, db_uri: str = settings.DB_URI):
        global session
        session = self
        self.sessionmaker = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=create_engine(db_uri, echo=True)
        )
        self.token = None

    def __call__(self) -> Session:
        global _session
        if (sess := _session.get()) is None:
            raise MissingSessionError

        return sess

    def query_property(self):

        class QueryDescriptor:
            def __get__(s, instance, owner): # noqa
                return self.query(owner) # noqa

        return QueryDescriptor()

    def __enter__(self):
        sess = self.sessionmaker()
        self.token = _session.set(sess)
        return sess

    def __exit__(self, exc_type, exc_value, traceback):
        sess = _session.get()
        if exc_type is not None:
            sess.rollback()

        sess.close()


session = SessionManager()


def instrument(name):
    def do(self, *args, **kwargs):
        return getattr(self(), name)(*args, **kwargs)
    return do


for meth in Session.public_methods:
    setattr(SessionManager, meth, instrument(meth))


def makeprop(name):
    def set_(self, attr):
        setattr(self(), name, attr)

    def get(self):
        return getattr(self(), name)

    return property(get, set_)


for prop in (
    "bind",
    "dirty",
    "deleted",
    "new",
    "identity_map",
    "is_active",
    "autoflush",
    "no_autoflush",
    "info",
    "autocommit",
):
    setattr(SessionManager, prop, makeprop(prop))


def clslevel(name):
    def do(cls, *args, **kwargs): # noqa
        return getattr(Session, name)(*args, **kwargs)

    return classmethod(do)


for prop in ("close_all", "object_session", "identity_key"):
    setattr(SessionManager, prop, clslevel(prop))
