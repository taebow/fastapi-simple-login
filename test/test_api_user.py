import random

from fastapi.testclient import TestClient
import pytest

from fastapi_simple_login.db import SessionManager, User
from fastapi_simple_login import app

client = TestClient(app)

test_sample = [
    ("test@example.com", "test_password", "Test user"),
    ("test2@example.com", "test_password2", "Test user2"),
    ("test3@example.com", "test_password3", "Test user3"),
]


def get_values(field):
    return [
        sample[["email", "password", "name"].index(field)]
        for sample in test_sample
    ]


@pytest.mark.parametrize("email, password, name", test_sample)
def test_create_user(email, password, name):
    response = client.post(
        "/users/",
        json=dict(email=email, password=password, name=name)
    )
    assert response.status_code == 200
    test_user = response.json()
    assert len(test_user.keys()) == 3
    assert test_user["email"] == email
    assert test_user["name"] == name
    assert test_user["last_login"] is None


@pytest.mark.parametrize("email, password, name", test_sample)
def test_get_user(email, name, password):
    response = client.get(f"/users/{email}")
    assert response.status_code == 200
    test_user = response.json()
    assert len(test_user.keys()) == 3
    assert test_user["email"] == email
    assert test_user["name"] == name
    assert test_user["last_login"] is None


def test_list_users():
    response = client.get(f"/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3
    assert all(len(user.keys()) == 3 for user in users)
    assert all(user["email"] in get_values("email") for user in users)
    assert all(user["name"] in get_values("name") for user in users)
    assert all(user["last_login"] is None for user in users)


@pytest.mark.parametrize("fields_update", [
    {"email_update": "newemail@example.com"},
    {"password": "newpassword"},
    {"name": "Changed name"},
    {"email_update": "newemail2@example.com", "name": "Changed name2"}
])
def test_update_user(fields_update):
    rand_user_email = random.choice(client.get("/users/").json())["email"]
    client.put("/users/", json=dict(**fields_update, email=rand_user_email))

    email = fields_update.pop("email_update", rand_user_email)

    with SessionManager():
        updated_user = User.query.filter(User.email == email).first()

    assert all(
        getattr(updated_user, field) == value
        for field, value in fields_update.items()
    )


def test_delete_user():
    initial_users = client.get("/users/").json()
    rand_user_email = random.choice(initial_users)["email"]

    client.delete("/users/", json=dict(email=rand_user_email))

    final_users = client.get("/users/").json()

    assert len(initial_users) - len(final_users) == 1
    assert all(rand_user_email not in user for user in final_users)
