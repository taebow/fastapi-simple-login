import pytest
from fastapi.testclient import TestClient

from fastapi_simple_login.db import session as db_session, SessionManager
from fastapi_simple_login.db import create_all, drop_all, bootstrap
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


@pytest.fixture(scope="module")
def bootstrap_root_user():
    bootstrap()


@pytest.fixture(scope="session")
def login(client):
    def _login(email, password):
        return client.post(
            "/login",
            json={"email": email, "password": password}
        )
    return _login


@pytest.fixture(scope="module")
def token(client, login):
    def _token(email, password):
        response = login(email, password)
        return "Bearer " + response.json()["token"]
    return _token


@pytest.fixture(scope="module")
def root_token(bootstrap_root_user, token, root_email, root_password):
    return token(root_email, root_password)
