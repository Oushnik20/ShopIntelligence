import json
from datetime import datetime

OUTPUT_FILE = "pipeline/generated_events.jsonl"


def save_entry_event(track_id):

    event = {
        "event_id": f"entry_{track_id}_{int(datetime.now().timestamp())}",
        "store_id": "STORE_BLR_002",
        "camera_id": "CAM3",
        "visitor_id": f"VIS_{track_id}",
        "event_type": "ENTRY",
        "timestamp": datetime.utcnow().isoformat(),
        "zone_id": None,
        "dwell_ms": 0,
        "is_staff": False,
        "confidence": 0.95,
        "metadata": {}
    }

    with open(
        OUTPUT_FILE,
        "a"
    ) as f:

        f.write(
            json.dumps(event)
            + "\n"
        )

    print(
        f"ENTRY SAVED -> VIS_{track_id}"
    )

def save_dwell_event(
    track_id,
    zone_id,
    dwell_ms
):

    event = {
        "event_id": f"dwell_{track_id}_{zone_id}_{int(datetime.now().timestamp())}",
        "store_id": "STORE_BLR_002",
        "camera_id": "CAM1",
        "visitor_id": f"VIS_{track_id}",
        "event_type": "ZONE_DWELL",
        "timestamp": datetime.utcnow().isoformat(),
        "zone_id": zone_id,
        "dwell_ms": dwell_ms,
        "is_staff": False,
        "confidence": 0.95,
        "metadata": {}
    }

    with open(
        OUTPUT_FILE,
        "a"
    ) as f:

        f.write(
            json.dumps(event)
            + "\n"
        )

def save_queue_event(
    track_id
):

    import json
    from datetime import datetime

    event = {
        "event_id": f"queue_{track_id}_{int(datetime.now().timestamp())}",
        "store_id": "STORE_BLR_002",
        "camera_id": "CAM5",
        "visitor_id": f"VIS_{track_id}",
        "event_type": "BILLING_QUEUE_JOIN",
        "timestamp": datetime.utcnow().isoformat(),
        "zone_id": "BILLING",
        "dwell_ms": 0,
        "is_staff": False,
        "confidence": 0.95,
        "metadata": {}
    }

    with open(
        OUTPUT_FILE,
        "a"
    ) as f:

        f.write(
            json.dumps(event)
            + "\n"
        )

    print(
        f"QUEUE SAVED -> VIS_{track_id}"
    )

