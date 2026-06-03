import cv2
import time
import numpy as np

from detector import detect_people
from tracker import update_tracks
from event_generator import save_zone_event
from store_config import load_store_config, get_zone_polygon, point_inside_polygon

VIDEO_PATH = r"Store_video/ZONE_CAM.mp4"
STORE_ID = "STORE_BLR_002"
CAMERA_ID = "ZONE_CAM"
ZONE_ID = "ZONE_1"

config = load_store_config(STORE_ID)
ZONE_POLYGON = get_zone_polygon(config)

track_state = {}
cap = cv2.VideoCapture(VIDEO_PATH)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_people(frame)
    tracks = update_tracks(detections)

    if tracks.tracker_id is None:
        if ZONE_POLYGON:
            contour = np.array(ZONE_POLYGON, dtype=int).reshape((-1, 1, 2))
            cv2.polylines(frame, [contour], True, (255, 0, 0), 3)
        cv2.imshow("STORE2 ZONE CAM", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    for box, track_id in zip(tracks.xyxy, tracks.tracker_id):
        x1, y1, x2, y2 = map(int, box)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        inside_zone = point_inside_polygon((center_x, center_y), ZONE_POLYGON)

        state = track_state.setdefault(
            track_id,
            {"inside": False, "entered_at": None, "dwell_saved": False}
        )

        if inside_zone and not state["inside"]:
            state["inside"] = True
            state["entered_at"] = time.time()
            state["dwell_saved"] = False
            save_zone_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID,
                event_type="ZONE_ENTER",
                zone_id=ZONE_ID
            )
            print(f"STORE2 ZONE_ENTER SAVED -> VIS_{track_id}")

        if inside_zone and state["entered_at"] is not None:
            dwell_ms = int((time.time() - state["entered_at"]) * 1000)
            if dwell_ms > 5000 and not state["dwell_saved"]:
                save_zone_event(
                    track_id,
                    store_id=STORE_ID,
                    camera_id=CAMERA_ID,
                    event_type="ZONE_DWELL",
                    zone_id=ZONE_ID,
                    dwell_ms=dwell_ms
                )
                state["dwell_saved"] = True
                print(f"STORE2 ZONE_DWELL SAVED -> VIS_{track_id}")

        if not inside_zone and state["inside"]:
            dwell_ms = 0
            if state["entered_at"] is not None:
                dwell_ms = int((time.time() - state["entered_at"]) * 1000)
            save_zone_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID,
                event_type="ZONE_EXIT",
                zone_id=ZONE_ID,
                dwell_ms=dwell_ms
            )
            state["inside"] = False
            state["entered_at"] = None
            state["dwell_saved"] = False
            print(f"STORE2 ZONE_EXIT SAVED -> VIS_{track_id}")

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if ZONE_POLYGON:
        contour = np.array(ZONE_POLYGON, dtype=int).reshape((-1, 1, 2))
        cv2.polylines(frame, [contour], True, (255, 0, 0), 3)

    cv2.imshow("STORE2 ZONE CAM", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
