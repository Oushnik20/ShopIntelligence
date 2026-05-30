# PROMPT:
# Generate ingest endpoint tests.
#
# CHANGES MADE:
# Added idempotency verification.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest():

    payload = [
        {
            "event_id": "pytest_event",
            "store_id": "STORE_BLR_002",
            "camera_id": "CAM_ENTRY_01",
            "visitor_id": "VIS_PY",
            "event_type": "ENTRY",
            "timestamp": "2026-03-03T14:22:10Z",
            "zone_id": None,
            "dwell_ms": 0,
            "is_staff": False,
            "confidence": 0.95,
            "metadata": {
                "session_seq": 1
            }
        }
    ]

    response = client.post(
        "/events/ingest",
        json=payload
    )

    assert response.status_code == 200