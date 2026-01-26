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
                if cls == 0:
                    persons.append(box.xyxy[0].tolist())

        return persons
