import cv2
import time

from detector import detect_people
from tracker import update_tracks
from event_generator import save_dwell_event

VIDEO_PATH = r"videos/CAM 1.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

track_start_time = {}
saved_tracks = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    detections = detect_people(
        frame
    )

    tracks = update_tracks(
        detections
    )

    for box, track_id in zip(
        tracks.xyxy,
        tracks.tracker_id
    ):

        x1, y1, x2, y2 = map(
            int,
            box
        )

        if track_id not in track_start_time:

            track_start_time[track_id] = time.time()

        dwell_ms = int(
            (
                time.time()
                -
                track_start_time[track_id]
            ) * 1000
        )

        if (
            dwell_ms > 5000
            and track_id not in saved_tracks
        ):

            save_dwell_event(
                track_id,
                "ZONE_1",
                dwell_ms
            )

            saved_tracks.add(
                track_id
            )

            print(
                f"DWELL SAVED -> {track_id}"
            )

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "CAM1 DWELL",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()