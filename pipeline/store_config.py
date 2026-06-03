import json
from pathlib import Path


STORE_CONFIGS = {
    "STORE_BLR_001": "store1.json",
    "STORE_BLR_002": "store2.json"
}


def load_store_config(store_id: str):
    root_dir = Path(__file__).resolve().parents[1]
    config_name = STORE_CONFIGS.get(store_id)

    if not config_name:
        raise ValueError(
            f"Unsupported store_id: {store_id}."
        )

    config_path = root_dir / "configs" / config_name

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_entry_line(config: dict, camera_id: str):
    entry_line = config.get("entry_line", [])

    if isinstance(entry_line, int):
        return entry_line

    if isinstance(entry_line, list):
        if camera_id == "ENTRY_CAM_2" and len(entry_line) > 1:
            return entry_line[1]
        if len(entry_line) > 0:
            return entry_line[0]

    raise ValueError("No entry_line configured for camera_id")


def get_zone_polygon(config: dict):
    return config.get("zone_polygon", [])


def get_queue_polygon(config: dict):
    return config.get("queue_polygon", [])


def point_inside_polygon(point, polygon):
    import cv2
    import numpy as np

    if not polygon:
        return False

    contour = np.array(polygon, dtype=int)
    return cv2.pointPolygonTest(contour, point, False) >= 0
