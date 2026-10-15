
from app import app


def test_homepage_returns_success():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"DevOps CI/CD Dashboard" in response.data


def test_health_endpoint_returns_success():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_health_endpoint_includes_version():
    client = app.test_client()
    response = client.get("/health")

    assert "version" in response.json
    assert response.json["version"] == "1.0.0"
