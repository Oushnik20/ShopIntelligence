import json
from datetime import datetime

OUTPUT_FILE = "pipeline/generated_events.jsonl"


def write_event(event: dict):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def create_event(
    track_id: int,
    store_id: str,
    camera_id: str,
    event_type: str,
    zone_id=None,
    zone_name=None,
    zone_type=None,
    is_revenue_zone=None,
    dwell_ms: int = 0,
    is_staff: bool = False,
    confidence: float = 0.95,
    metadata: dict = None,
):
    return {
        "event_id": f"{event_type.lower()}_{track_id}_{int(datetime.now().timestamp())}",
        "store_id": store_id,
        "camera_id": camera_id,
        "visitor_id": f"VIS_{track_id}",
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "zone_id": zone_id,
        "zone_name": zone_name,
        "zone_type": zone_type,
        "is_revenue_zone": is_revenue_zone,
        "dwell_ms": dwell_ms,
        "is_staff": is_staff,
        "confidence": confidence,
        "metadata": metadata or {}
    }


def save_entry_event(
    track_id,
    store_id="STORE_BLR_002",
    camera_id="CAM3",
    metadata=None,
):
    event = create_event(
        track_id,
        store_id,
        camera_id,
        "ENTRY",
        dwell_ms=0,
        metadata=metadata,
    )
    write_event(event)


def save_exit_event(
    track_id,
    store_id="STORE_BLR_002",
    camera_id="CAM3",
    metadata=None,
):
    event = create_event(
        track_id,
        store_id,
        camera_id,
        "EXIT",
        dwell_ms=0,
        metadata=metadata,
    )
    write_event(event)


def save_zone_event(
    track_id,
    store_id,
    camera_id,
    event_type,
    zone_id,
    zone_name=None,
    zone_type=None,
    is_revenue_zone=None,
    dwell_ms: int = 0,
    metadata=None,
):
    event = create_event(
        track_id,
        store_id,
        camera_id,
        event_type,
        zone_id=zone_id,
        zone_name=zone_name,
        zone_type=zone_type,
        is_revenue_zone=is_revenue_zone,
        dwell_ms=dwell_ms,
        metadata=metadata,
    )
    write_event(event)


def save_queue_event(
    track_id,
    store_id="STORE_BLR_002",
    camera_id="CAM5",
    event_type="BILLING_QUEUE_JOIN",
    zone_id="BILLING",
    dwell_ms: int = 0,
    metadata=None,
):
    event = create_event(
        track_id,
        store_id,
        camera_id,
        event_type,
        zone_id=zone_id,
        dwell_ms=dwell_ms,
        metadata=metadata,
    )
    write_event(event)
