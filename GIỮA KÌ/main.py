import cv2
from ultralytics import YOLO
import numpy as np

# Khởi tạo
cap = cv2.VideoCapture("mvideo.mp4")
model = YOLO('yolov8n.pt')  # hoặc yolov8s.pt nếu muốn chính xác hơn
LINE_Y = 250                # vị trí line ngang (chỉnh nếu cần, ví dụ 300-400)
count = 0
tracked_ids = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect + Track (chỉ xe: car, motorcycle, bus, truck)
    results = model.track(frame, persist=True, classes=[2, 3, 5, 7], conf=0.4, verbose=False)
    
    # Vẽ line đếm (đỏ)
    cv2.line(frame, (0, LINE_Y), (frame.shape[1], LINE_Y), (0, 0, 255), 3)
    
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id.int().cpu().numpy()
        
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            # Vẽ bounding box xanh lá
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Hiển thị ID xe (luôn hiển thị)
            obj_id = int(track_ids[i])
            cv2.putText(frame, f"ID: {obj_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Đếm khi tâm vượt line (ngưỡng 20 để ổn định hơn)
            if abs(cy - LINE_Y) < 20:
                if obj_id not in tracked_ids:
                    tracked_ids.add(obj_id)
                    count += 1
    
    # Chỉ hiển thị Count (xanh lá, lớn, nổi bật)
    cv2.putText(frame, f"Count: {count}", (30, 80),
                cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 255, 0), 6)
    
    cv2.imshow('Vehicle Counting - YOLO', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Tổng số xe đã đếm: {count}")