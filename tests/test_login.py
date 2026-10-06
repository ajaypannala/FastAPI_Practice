from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "ajaynani@gmail.com",
            "password": "ajay123"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()