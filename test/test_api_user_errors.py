import pytest


@pytest.fixture(scope="function")
def user(client):
    test_user = client.post(
        "/users",
        json=dict(
            email="test@example.com",
            password="password",
            name="Test user"
        )
    ).json()

    yield test_user

    client.delete(f"/users/{test_user['email']}")


def test_create_user_twice_fails(client, user):
    response = client.post(
        "/users",
        json=dict(
            email="test@example.com",
            password="password",
            name="Test user"
        )
    )

    assert response.status_code == 403
