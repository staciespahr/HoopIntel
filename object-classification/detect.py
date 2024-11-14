import numpy as np
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)
    return results


def classify_color(region):
    """
    Classifies the dominant color of a given region as 'Light' or 'Dark' based on HSV value.
    """
    hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    mean_value = np.mean(hsv_region[:, :, 2])  # V channel (brightness)

    if mean_value > 127:
        return "Light"
    else:
        return "Dark"


def detect_and_classify_colors(chosen_model, img, conf=0.5):
    results = chosen_model.predict(img, conf=conf)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3])

            # Get central region of the bounding box
            center_x1 = x1 + (x2 - x1) // 4
            center_y1 = y1 + (y2 - y1) // 4
            center_x2 = x2 - (x2 - x1) // 4
            center_y2 = y2 - (y2 - y1) // 4
            person_region = img[center_y1:center_y2, center_x1:center_x2]

            color_class = classify_color(person_region)
            color = (255, 255, 255) if color_class == "Light" else (0, 0, 0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{color_class} Color", (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

    return img
