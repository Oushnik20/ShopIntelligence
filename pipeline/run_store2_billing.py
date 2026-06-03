import cv2
import time
import numpy as np

from detector import detect_people
from tracker import update_tracks
from event_generator import save_queue_event
from store_config import load_store_config, get_queue_polygon, point_inside_polygon

VIDEO_PATH = r"Store_video/BILLING_CAM.mp4"
STORE_ID = "STORE_BLR_002"
CAMERA_ID = "BILLING_CAM"

config = load_store_config(STORE_ID)
QUEUE_POLYGON = get_queue_polygon(config)
track_state = {}

cap = cv2.VideoCapture(VIDEO_PATH)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_people(frame)
    tracks = update_tracks(detections)

    if tracks.tracker_id is None:
        if QUEUE_POLYGON:
            contour = np.array(QUEUE_POLYGON, dtype=int).reshape((-1, 1, 2))
            cv2.polylines(frame, [contour], True, (255, 0, 0), 3)
        cv2.imshow("STORE2 BILLING CAM", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    for box, track_id in zip(tracks.xyxy, tracks.tracker_id):
        x1, y1, x2, y2 = map(int, box)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        inside_queue = point_inside_polygon((center_x, center_y), QUEUE_POLYGON)

        state = track_state.setdefault(
            track_id,
            {"inside": False, "joined_at": None}
        )

        if inside_queue and not state["inside"]:
            state["inside"] = True
            state["joined_at"] = time.time()
            save_queue_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID,
                event_type="BILLING_QUEUE_JOIN"
            )
            print(f"STORE2 QUEUE JOIN SAVED -> VIS_{track_id}")

        if not inside_queue and state["inside"]:
            queue_time = 0
            if state["joined_at"] is not None:
                queue_time = int((time.time() - state["joined_at"]) * 1000)

            event_type = (
                "BILLING_QUEUE_COMPLETED"
                if queue_time >= 4000
                else "BILLING_QUEUE_ABANDON"
            )

            save_queue_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID,
                event_type=event_type,
                dwell_ms=queue_time
            )
            print(f"STORE2 {event_type} SAVED -> VIS_{track_id} ({queue_time}ms)")

            state["inside"] = False
            state["joined_at"] = None

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if QUEUE_POLYGON:
        contour = np.array(QUEUE_POLYGON, dtype=int).reshape((-1, 1, 2))
        cv2.polylines(frame, [contour], True, (255, 0, 0), 3)

    cv2.putText(frame, "QUEUE ZONE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow("STORE2 BILLING CAM", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
