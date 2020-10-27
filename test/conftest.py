import pytest
from fastapi.testclient import TestClient

from fastapi_simple_login.db import session as db_session, SessionManager
from fastapi_simple_login.db import create_all, drop_all
from fastapi_simple_login import app
from fastapi_simple_login.config import settings


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


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def root_email():
    return settings.ROOT_EMAIL


@pytest.fixture(scope="session")
def root_password():
    return settings.ROOT_PASSWORD


