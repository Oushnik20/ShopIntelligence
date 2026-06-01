from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_anomalies():
    response = client.get("/stores/STORE_BLR_002/anomalies")

    assert response.status_code == 200

    data = response.json()

    assert data["store_id"] == "STORE_BLR_002"
    assert isinstance(data.get("anomalies"), list)
