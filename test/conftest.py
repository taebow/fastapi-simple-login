import pytest

from fastapi_simple_login.db import session as db_session, SessionManager
from fastapi_simple_login.db import create_all, drop_all


@pytest.fixture(scope="module", autouse=True)
def prepare():
    with db_session:
        create_all(reset=True)
    yield
    with db_session:
        drop_all()


@pytest.fixture
def session():
    with SessionManager() as session:
        yield session
