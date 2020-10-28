import pytest
from datetime import datetime, timedelta


COMMON_USER_EMAIL = "common@example.com"
COMMON_USER_PASSWORD = "commonuserpass"
COMMON_USER_NAME = "Common User Name"


@pytest.fixture(scope="module")
def common_user(client, root_token):
    return client.post(
        "/users",
        json=dict(
            email=COMMON_USER_EMAIL,
            password=COMMON_USER_PASSWORD,
            name=COMMON_USER_NAME
        )
    )


def test_get_me(client, token, common_user):
    now = datetime.now()

    tok = token(COMMON_USER_EMAIL, COMMON_USER_PASSWORD)

    response = client.get(
        "/users/me",
        headers={"Authorization": tok}
    )

    assert response.status_code == 200

    user = response.json()

    assert user["email"] == COMMON_USER_EMAIL
    assert user["name"] == COMMON_USER_NAME
    assert isinstance(user["last_login"], str)

    last_login = datetime.fromisoformat(user["last_login"])

    assert last_login - now < timedelta(seconds=1)
