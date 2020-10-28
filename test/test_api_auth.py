from datetime import datetime, timedelta
import pytest

invalid_passwords = ["no password", "invalid pass", "try again"]
invalid_tokens = ["nothing", "Bearer super", None]


@pytest.mark.usefixtures("bootstrap_root_user")
def test_root_login(client, login, root_email, root_password):
    response = login(root_email, root_password)
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response.keys()) == 2
    assert json_response["status"] == "Authorized"
    assert isinstance(json_response["token"], str)

    last_login = client.get(f"/users/{root_email}").json()["last_login"]

    last_login = datetime.fromisoformat(last_login)
    assert isinstance(last_login, datetime)
    assert datetime.utcnow() - last_login < timedelta(seconds=1)


def test_protected_endpoint_success(client, root_token):
    response = client.get(
        "/resource/protected",
        headers={"Authorization": root_token}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.parametrize("invalid_token", invalid_tokens)
def test_protected_endpoint_fails_invalid_token(client, invalid_token):
    response = client.get(
        "/resource/protected",
        headers={"Authorization": invalid_token}
    )
    assert response.status_code in [401, 403]


def test_protected_endpoint_fails_no_auth_header(client):
    response = client.get("/resource/protected")
    assert response.status_code in [401, 403]


@pytest.mark.parametrize("invalid_password", invalid_passwords)
def test_login_fails_last_login_remain(
        client, login, root_email, invalid_password
):
    def get_last_login():
        return client.get(f"/users/{root_email}").json()["last_login"]

    last_login_before = get_last_login()

    login(root_email, invalid_password)

    last_login_after = get_last_login()

    assert last_login_before == last_login_after
