from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/auth/register",
        json={
            "name": "ajay",
            "email": "ajaynani@gmail.com",
            "password": "ajay123",
            "role": "user"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200