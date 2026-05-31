import cv2

from detector import detect_people
from tracker import update_tracks
from event_generator import save_entry_event

VIDEO_PATH = r"videos/CAM 3.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

ENTRY_LINE_X = 900

crossed_in = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    detections = detect_people(frame)

    tracks = update_tracks(detections)

    if tracks.tracker_id is None:
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

        if (
            center_x > ENTRY_LINE_X
            and track_id not in crossed_in
        ):

            crossed_in.add(track_id)

            save_entry_event(
                track_id
            )

            print(
                f"ENTRY SAVED -> VIS_{track_id}"
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

    cv2.line(
        frame,
        (ENTRY_LINE_X, 0),
        (ENTRY_LINE_X, frame.shape[0]),
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        "ENTRY LINE",
        (ENTRY_LINE_X - 120, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "CAM3 Entry Tracking",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()