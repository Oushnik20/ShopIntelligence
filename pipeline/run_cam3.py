import cv2

from detector import detect_people
from tracker import update_tracks
from event_generator import save_entry_event, save_exit_event
from store_config import load_store_config, get_entry_line

VIDEO_PATH = r"videos/CAM 3.mp4"
STORE_ID = "STORE_BLR_001"
CAMERA_ID = "ENTRY_CAM_1"

config = load_store_config(STORE_ID)
ENTRY_LINE_X = get_entry_line(config, CAMERA_ID)

cap = cv2.VideoCapture(VIDEO_PATH)

crossed_in = set()
crossed_out = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    detections = detect_people(frame)
    tracks = update_tracks(detections)

    if tracks.tracker_id is None:
        cv2.imshow("CAM3 Entry Tracking", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    for box, track_id in zip(
        tracks.xyxy,
        tracks.tracker_id
    ):

        x1, y1, x2, y2 = map(int, box)
        center_x = (x1 + x2) // 2

        if center_x > ENTRY_LINE_X and track_id not in crossed_in:
            crossed_in.add(track_id)
            save_entry_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID
            )
            print(f"ENTRY SAVED -> VIS_{track_id}")

        if center_x <= ENTRY_LINE_X and track_id in crossed_in and track_id not in crossed_out:
            crossed_out.add(track_id)
            save_exit_event(
                track_id,
                store_id=STORE_ID,
                camera_id=CAMERA_ID
            )
            print(f"EXIT SAVED -> VIS_{track_id}")

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