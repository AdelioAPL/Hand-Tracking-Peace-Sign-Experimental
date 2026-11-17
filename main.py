import os
import sys

# Konfigurasi display untuk Linux/Wayland/X11 agar GUI OpenCV (Qt) berjalan lancar
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import mediapipe as mp
import urllib.request

# Siapkan model gesture recognizer untuk MediaPipe versi baru (Tasks API)
MODEL_NAME = "gesture_recognizer.task"
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_NAME)
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"

use_legacy = hasattr(mp, 'solutions')

if not use_legacy:
    if not os.path.exists(MODEL_PATH):
        print("Mengunduh model pendeteksi gestur (sekali saja)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
else:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
background = None

print("=== INVISIBLE PEACE GESTURE ===")
print("Tekan 'b': Simpan/reset background ruangan.")
print("Tekan 'q': Keluar aplikasi.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Cermin
    h, w, _ = frame.shape

    # Set background awal
    if background is None:
        background = frame.copy()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    is_peace = False

    if not use_legacy:
        # MediaPipe modern (Tasks API)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = recognizer.recognize(mp_image)
        if result.gestures:
            for gesture_list in result.gestures:
                for gesture in gesture_list:
                    # 'Victory' adalah gestur jari peace (✌️)
                    if gesture.category_name in ["Victory", "Peace"]:
                        is_peace = True
                        break
    else:
        # MediaPipe versi lama (Solutions API)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark
                index_up = lm[8].y < lm[6].y
                middle_up = lm[12].y < lm[10].y
                ring_down = lm[16].y > lm[14].y
                pinky_down = lm[20].y > lm[18].y
                if index_up and middle_up and ring_down and pinky_down:
                    is_peace = True
                    break

    # Tampilkan background saat pose peace terdeteksi, atau frame asli saat biasa
    output = background.copy() if is_peace else frame

    # Teks status di layar
    status_text = "HILANG (Peace Sign! ✌️)" if is_peace else "Terlihat"
    color = (0, 0, 255) if is_peace else (0, 255, 0)
    cv2.putText(output, f"Status: {status_text}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(output, "[b] Reset Background | [q] Keluar", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("Peace Disappear", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('b'):
        background = frame.copy()

cap.release()
cv2.destroyAllWindows()
