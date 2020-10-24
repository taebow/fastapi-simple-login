from fastapi_simple_login.db import session
from fastapi_simple_login.db.mixin import Base


def create_all(reset: bool = False) -> None:
    if reset:
        drop_all()
    Base.metadata.create_all(session.bind)
    session.commit()


def drop_all() -> None:
    session.close()
    Base.metadata.drop_all(session.bind)
    session.commit()
