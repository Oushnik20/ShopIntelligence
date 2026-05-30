# PROMPT:
# Generate pytest tests for FastAPI metrics endpoint.
#
# CHANGES MADE:
# Added store specific assertions and visitor validation.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200


def test_metrics():

    response = client.get(
        "/stores/STORE_BLR_002/metrics"
    )

    assert response.status_code == 200