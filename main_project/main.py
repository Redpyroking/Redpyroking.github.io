import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv #pip install supervision=='0.3.0'
import voice

setting_startup = False
cap = None

ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

def setup():
    global setting_startup
    if not setting_startup:
        global cap
        cap = cv2.VideoCapture(0)
        setting_startup = True

def switch_camera(key):
    global cap
    if key == ord('a'):
        print("'a' key was pressed!")
        cap = cv2.VideoCapture(0)
    elif key == ord('s'):
        print("'s' key was pressed!")
        cap = cv2.VideoCapture(1)

def main():
    global cap
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Unable to access built-in camera. Attempting to use Iriun Webcam.")
        cap = cv2.VideoCapture(0)  # Use the first camera device (Iriun Webcam)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    model = YOLO("yolov8n-seg.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array([frame_width, frame_height])).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=(frame_width, frame_height))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('a') or key == ord('s'):
            switch_camera(key)

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )
        person_count = sum(1 for label in labels if 'person' in label.lower()  and float(label.split()[1]) > 0.6)
        # Print or use the count as needed
        say = f"Number of person detected: {person_count}"
        if key == 13:
            voice.speak(say)

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)

        cv2.imshow("yolov8", frame)
        

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setup()
    main()
    
