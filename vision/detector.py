from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_name):
        self.model = YOLO(model_name)

    def detect(self, frame):
        results = self.model(frame, stream=True)
        persons = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                # Class 0 = person in COCO
                if cls == 0:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])

                    width = x2 - x1
                    height = y2 - y1

                    persons.append(
                        ([x1, y1, width, height], confidence, "person")
                    )

        return persons