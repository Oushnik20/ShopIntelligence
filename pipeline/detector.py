from ultralytics import YOLO
import supervision as sv

model = YOLO("yolov8n.pt")


def detect_people(frame):

    results = model(
        frame,
        classes=[0],
        verbose=False
    )[0]

    if len(results.boxes) == 0:

        return sv.Detections.empty()

    xyxy = results.boxes.xyxy.cpu().numpy()

    confidence = (
        results.boxes.conf
        .cpu()
        .numpy()
    )

    class_id = (
        results.boxes.cls
        .cpu()
        .numpy()
        .astype(int)
    )

    detections = sv.Detections(
        xyxy=xyxy,
        confidence=confidence,
        class_id=class_id
    )

    return detections