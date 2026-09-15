from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    response = client.post(
        "/predict",
        json={
            "age": 25,
            "salary": 50000,
            "experience": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "score" in data
    assert "message" in data


def test_invalid_input():
    response = client.post(
        "/predict",
        json={
            "age": 10,
            "salary": 50000,
            "experience": 2
        }
    )

    assert response.status_code == 422


def test_user_not_found():
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_async_demo():
    response = client.get("/async-demo")

    assert response.status_code == 200
    assert response.json()["status"] == "success"