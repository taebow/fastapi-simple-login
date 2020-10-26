import pytest
from fastapi_simple_login.db import bootstrap as _bootstrap


@pytest.fixture(scope="module", autouse=True)
def bootstrap():
    _bootstrap()


@pytest.fixture(scope="module")
def root_token(client, root_email, root_password):
    response = client.post(
        "/login",
        json={"email": root_email, "password": root_password}
    )
    return "Bearer "+ response.json()["token"]


def test_root_login(client, root_email, root_password):
    response = client.post(
        "/login",
        json={"email": root_email, "password": root_password}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response.keys()) == 2
    assert json_response["status"] == "ok"
    assert isinstance(json_response["token"], str)


def test_protected_endpoint_success(client, root_token):
    response = client.get(
        "/resource/protected",
        headers={"Authorization": root_token}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.parametrize("invalid_token", [
    "nothing",
    "Bearer super",
    None
])
def test_protected_endpoint_fails_invalid_token(client, invalid_token):
    response = client.get(
        "/resource/protected",
        headers={"Authorization": invalid_token}
    )
    assert response.status_code in [401, 403]


def test_protected_endpoint_fails_no_auth_header(client):
    response = client.get("/resource/protected")
    assert response.status_code in [401, 403]
