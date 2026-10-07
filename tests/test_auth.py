from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser123",
            "email": "testuser123@example.com",
            "password": "password123",
        },
    )

    assert response.status_code in [200, 400]


def test_login():
    response = client.post(
        "/auth/login", data={"username": "testuser123", "password": "password123"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_users_me_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401
