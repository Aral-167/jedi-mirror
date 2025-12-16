import time
import numpy as np
import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
from picamera2 import Picamera2

# Set to your monitor resolution
SCREEN_W, SCREEN_H = 1920, 1080

mouse = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

# Smoothing
smooth = 0.25
prev_x, prev_y = SCREEN_W // 2, SCREEN_H // 2

pinch_down = False
last_click_time = 0.0

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# --- Picamera2 setup ---
picam2 = Picamera2()

# Smaller capture size = faster tracking. 1280x720 is a good start.
config = picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

while True:
    frame = picam2.capture_array()  # RGB image (H, W, 3)

    # Mirror feel: flip horizontally
    frame = cv2.flip(frame, 1)

    # MediaPipe expects RGB
    result = hands.process(frame)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark

        # Index fingertip (8)
        ix, iy = lm[8].x, lm[8].y
        # Thumb tip (4)
        tx, ty = lm[4].x, lm[4].y

        # Map normalized coords -> screen coords
        target_x = int(ix * SCREEN_W)
        target_y = int(iy * SCREEN_H)

        # Smooth cursor
        new_x = int(prev_x + (target_x - prev_x) * smooth)
        new_y = int(prev_y + (target_y - prev_y) * smooth)
        prev_x, prev_y = new_x, new_y

        mouse.position = (clamp(new_x, 0, SCREEN_W - 1), clamp(new_y, 0, SCREEN_H - 1))

        # Pinch distance (normalized)
        pinch_dist = float(np.hypot(ix - tx, iy - ty))

        # Tune these thresholds if needed
        pinch_close = pinch_dist < 0.04
        pinch_open  = pinch_dist > 0.06

        now = time.time()

        # Click/drag
        if pinch_close and not pinch_down and (now - last_click_time) > 0.3:
            mouse.press(Button.left)
            pinch_down = True
            last_click_time = now

        if pinch_open and pinch_down:
            mouse.release(Button.left)
            pinch_down = False

    # Optional: add a tiny sleep to reduce CPU load
    time.sleep(0.001)
