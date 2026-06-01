from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_funnel():
    response = client.get("/stores/STORE_BLR_002/funnel")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data.get("entry"), int)
    assert isinstance(data.get("zone_visit"), int)
    assert isinstance(data.get("billing_queue"), int)
    assert isinstance(data.get("purchase"), int)

    assert data["entry"] >= 0
    assert data["zone_visit"] >= 0
    assert data["billing_queue"] >= 0
    assert data["purchase"] >= 0
    assert data["purchase"] <= data["entry"]
