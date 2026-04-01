import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ────────────────────────────────────────────────
#  CÁC HẰNG SỐ & HÀM HỖ TRỢ
# ────────────────────────────────────────────────

model_path = "hand_landmarker.task"  # Đã có trong thư mục, OK

# Các kết nối (connections) giữa các landmark - giống hệt phiên bản cũ
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # ngón cái
    (0, 5), (5, 6), (6, 7), (7, 8),           # ngón trỏ
    (0, 9), (9, 10), (10, 11), (11, 12),      # ngón giữa
    (0, 13), (13, 14), (14, 15), (15, 16),    # ngón áp út
    (0, 17), (17, 18), (18, 19), (19, 20),    # ngón útdeactivate
    (5, 9), (9, 13), (13, 17)                 # lòng bàn tay
]

def draw_landmarks(
    image: np.ndarray,
    detection_result: vision.HandLandmarkerResult
) -> np.ndarray:
    """Vẽ landmarks và connections lên ảnh (tương tự draw_landmarks cũ)"""
    annotated_image = image.copy()

    # Vẽ các điểm landmark
    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            for landmark in hand_landmarks:
                x = int(landmark.x * annotated_image.shape[1])
                y = int(landmark.y * annotated_image.shape[0])
                cv2.circle(annotated_image, (x, y), radius=4, color=(0, 255, 0), thickness=-1)

            # Vẽ các đường nối
            for connection in HAND_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                start_point = (int(start.x * annotated_image.shape[1]), int(start.y * annotated_image.shape[0]))
                end_point = (int(end.x * annotated_image.shape[1]), int(end.y * annotated_image.shape[0]))
                cv2.line(annotated_image, start_point, end_point, (0, 255, 255), 2)

    # Vẽ nhãn Left / Right (handedness)
    if detection_result.handedness:
        for i, handedness in enumerate(detection_result.handedness):
            if detection_result.hand_landmarks:
                # Lấy điểm landmark đầu tiên (cổ tay) để đặt text
                wrist = detection_result.hand_landmarks[i][0]
                x = int(wrist.x * annotated_image.shape[1]) + 10
                y = int(wrist.y * annotated_image.shape[0]) - 10
                label = handedness[0].category_name  # "Left" hoặc "Right"
                cv2.putText(
                    annotated_image,
                    label,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA
                )

    return annotated_image


# ────────────────────────────────────────────────
#  PHẦN WEBCAM (LIVE) - SỬ DỤNG VIDEO MODE
# ────────────────────────────────────────────────

def run_webcam():
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,  # ← Chuyển sang VIDEO mode
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    
    # Lấy FPS của camera (nếu có), fallback 30 nếu không
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    frame_time_ms = int(1000 / fps)  # Thời gian mỗi frame

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        timestamp_ms = 0  # Tăng dần theo thời gian

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Bỏ qua frame rỗng.")
                continue

            # Chuẩn bị ảnh cho MediaPipe (RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            # Xử lý frame với VIDEO mode (blocking, trả về kết quả ngay)
            detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

            # Vẽ kết quả
            annotated_frame = draw_landmarks(frame, detection_result)

            # Hiển thị (lật ngang cho selfie view)
            cv2.imshow('MediaPipe Hand Landmarker (Video Mode)', cv2.flip(annotated_frame, 1))

            if cv2.waitKey(5) & 0xFF == 27:  # ESC để thoát
                break

            timestamp_ms += frame_time_ms  # Tăng timestamp cho frame tiếp theo

    cap.release()
    cv2.destroyAllWindows()


# ────────────────────────────────────────────────
#  PHẦN XỬ LÝ ẢNH TĨNH (giữ nguyên, dùng IMAGE mode)
# ────────────────────────────────────────────────

def process_static_images(image_files: list[str]):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=2,
        min_hand_detection_confidence=0.5
    )

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        for idx, file_path in enumerate(image_files):
            image = cv2.imread(file_path)
            if image is None:
                print(f"Không đọc được ảnh: {file_path}")
                continue

            # Lật ngang để đúng handedness (tùy chọn)
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

            detection_result = landmarker.detect(mp_image)

            annotated_image = draw_landmarks(image, detection_result)

            # Lưu ảnh kết quả
            output_path = f"annotated_{idx}.jpg"
            cv2.imwrite(output_path, cv2.flip(annotated_image, 1))
            print(f"Đã lưu: {output_path}")

            # In tọa độ đầu ngón trỏ (ví dụ) - tương tự code cũ
            if detection_result.hand_landmarks:
                for hand_landmarks in detection_result.hand_landmarks:
                    tip = hand_landmarks[8]  # INDEX_FINGER_TIP = 8
                    h, w, _ = image.shape
                    print(f"Index finger tip: ({int(tip.x * w)}, {int(tip.y * h)})")


# ────────────────────────────────────────────────
#  CHẠY CHƯƠNG TRÌNH
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Chạy webcam (mặc định)
    run_webcam()

    # Nếu muốn xử lý ảnh tĩnh, uncomment và thêm đường dẫn
    # IMAGE_FILES = ["hand1.jpg", "hand2.jpg"]
    # process_static_images(IMAGE_FILES)