from ultralytics import YOLO


class ObjectDetector:

    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image):
        results = self.model(image)

        detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                label = self.model.names[class_id]

                detections.append({
                    "label": label,
                    "confidence": confidence
                })

        return results, detections