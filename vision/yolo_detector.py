import cv2
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")  # Path to model
input_folder = "data/dummy_frames"
output_folder = "data/annotated_frames"

os.makedirs(output_folder, exist_ok=True)

for file in sorted(os.listdir(input_folder)):
    if file.lower().endswith((".jpg", ".png")):
        path = os.path.join(input_folder, file)
        img = cv2.imread(path)

        results = model(img)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]

                # Bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw rectangle
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put label text
                cv2.putText(
                    img,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

        # Save annotated frame
        out_path = os.path.join(output_folder, file)
        cv2.imwrite(out_path, img)

print(f"[INFO] Annotated images saved to: {output_folder}")