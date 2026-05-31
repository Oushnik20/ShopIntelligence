import cv2
import time

from detector import detect_people
from tracker import update_tracks
from event_generator import save_queue_event

VIDEO_PATH = r"videos/CAM 5.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

QUEUE_X1 = 450
QUEUE_Y1 = 250

QUEUE_X2 = 1400
QUEUE_Y2 = 1080

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

    if tracks.tracker_id is None:

        cv2.imshow(
            "CAM5 Queue",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

        continue

    for box, track_id in zip(
        tracks.xyxy,
        tracks.tracker_id
    ):

        x1, y1, x2, y2 = map(
            int,
            box
        )

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        inside_queue = (
            QUEUE_X1 <= center_x <= QUEUE_X2
            and
            QUEUE_Y1 <= center_y <= QUEUE_Y2
        )

        if inside_queue:

            if track_id not in track_start_time:

                track_start_time[track_id] = time.time()

            queue_time = int(
                (
                    time.time()
                    -
                    track_start_time[track_id]
                ) * 1000
            )

            if (
                queue_time > 4000
                and track_id not in saved_tracks
            ):

                save_queue_event(
                    track_id
                )

                saved_tracks.add(
                    track_id
                )

                print(
                    f"QUEUE SAVED -> VIS_{track_id}"
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

    cv2.rectangle(
        frame,
        (QUEUE_X1, QUEUE_Y1),
        (QUEUE_X2, QUEUE_Y2),
        (255, 0, 0),
        3
    )

    cv2.putText(
        frame,
        "QUEUE ZONE",
        (QUEUE_X1, QUEUE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    cv2.imshow(
        "CAM5 Queue",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()