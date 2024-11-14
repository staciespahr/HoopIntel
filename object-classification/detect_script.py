import cv2
from ultralytics import YOLO
from detect import detect_and_classify_colors

model = YOLO("yolov8n.pt")


cap = cv2.VideoCapture("./videos/clip_2.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    result_img = detect_and_classify_colors(model, frame, conf=0.5)
    cv2.imshow("Teams", result_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
