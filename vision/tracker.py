from deep_sort_realtime.deepsort_tracker import DeepSort


class PersonTracker:

    def __init__(self):
        self.tracker = DeepSort(
            max_age=30,
            n_init=2
        )

    def update(self, detections, frame):

        tracks = self.tracker.update_tracks(
            detections,
            frame=frame
        )

        people = []

        for track in tracks:

            if not track.is_confirmed():
                continue


            track_id = track.track_id

            l, t, r, b = track.to_ltrb()

            l, t, r, b = map(int, [l, t, r, b])

            people.append({
                "id": track_id,
                "bbox": (l, t, r, b)
            })

        return people