from ultralytics import YOLO
import cv2
import os


# Load YOLOv8 nano model
try:
    model = YOLO("yolov8n.pt")
except Exception as e:
    print(f"Warning: Could not load YOLOv8 model: {e}")
    model = None


def detect_objects(image_path):
    """Detect objects in an image using YOLOv8."""
    if model is None:
        return None, []
    
    try:
        results = model(image_path)
        img = cv2.imread(image_path)
        
        if img is None:
            return None, []
        
        detections = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = r.names[int(box.cls[0])]
                conf = float(box.conf[0])
                
                detections.append({
                    'class': cls,
                    'confidence': round(conf, 4),
                    'bbox': [x1, y1, x2, y2]
                })
                
                # Draw rectangle and label on image
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{cls} {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Save the output image
        out_path = image_path.replace(".jpg", "_det.jpg").replace(".png", "_det.png")
        cv2.imwrite(out_path, img)
        
        return out_path, detections
    except Exception as e:
        print(f"Error in object detection: {e}")
        return None, []
