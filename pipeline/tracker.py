import supervision as sv

tracker = sv.ByteTrack()


def update_tracks(detections):

    tracks = tracker.update_with_detections(
        detections
    )

    return tracks