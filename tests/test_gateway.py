from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_gateway_requires_authentication():
    response = client.get("/gateway/internal/data")

    assert response.status_code == 401
