# import cv2
# import mediapipe as mp
# import time
# import math
# from pathlib import Path
# from gesture_recognition import is_fingers_closed_over_thumb
# from gesture_recognition import is_thumb_folded, is_fingers_closed_over_thumb


# # =====================================
# # 1. MODEL FILE
# # =====================================

# MODEL_PATH = Path(__file__).resolve().parent / "hand_landmarker.task"

# if not MODEL_PATH.exists():
#     raise FileNotFoundError(
#         "hand_landmarker.task not found inside ai_engine folder!"
#     )

# # =====================================
# # 2. MEDIAPIPE SETTINGS
# # =====================================

# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# RunningMode = mp.tasks.vision.RunningMode

# options = HandLandmarkerOptions(
#     base_options=BaseOptions(
#         model_asset_path=str(MODEL_PATH)
#     ),
#     running_mode=RunningMode.VIDEO,
#     num_hands=1,
#     min_hand_detection_confidence=0.5,
#     min_hand_presence_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# # =====================================
# # 3. HAND CONNECTIONS
# # =====================================

# connections = [
#     (0, 1), (1, 2), (2, 3), (3, 4),
#     (0, 5), (5, 6), (6, 7), (7, 8),
#     (5, 9), (9, 10), (10, 11), (11, 12),
#     (9, 13), (13, 14), (14, 15), (15, 16),
#     (13, 17), (17, 18), (18, 19), (19, 20),
#     (0, 17)
# ]

# # =====================================
# # 4. FINGER DETECTION
# # =====================================

# def is_finger_open(points, tip, pip):

#     wrist = points[0]

#     tip_distance = math.dist(
#         wrist, points[tip]
#     )

#     pip_distance = math.dist(
#         wrist, points[pip]
#     )

#     return tip_distance > pip_distance * 1.1


# # =====================================
# # 5. OPEN PALM DETECTION
# # =====================================

# def is_open_palm(points):

#     if len(points) != 21:
#         return False

#     fingers = [
#         (8, 6),    # Index
#         (12, 10),  # Middle
#         (16, 14),  # Ring
#         (20, 18)   # Pinky
#     ]

#     thumb_open = is_finger_open(
#         points, 4, 3
#     )

#     other_fingers_open = all(
#         is_finger_open(points, tip, pip)
#         for tip, pip in fingers
#     )

#     return thumb_open and other_fingers_open

# def is_open_palm(points):

#     if len(points) != 21:
#         return False

#     fingers = [
#         (8, 6),
#         (12, 10),
#         (16, 14),
#         (20, 18)
#     ]

#     thumb_open = is_finger_open(points, 4, 3)

#     other_fingers_open = all(
#         is_finger_open(points, tip, pip)
#         for tip, pip in fingers
#     )

#     return thumb_open and other_fingers_open


# # NEW FUNCTION - এখানে বসাবে

# def is_thumb_folded(points):

#     if len(points) != 21:
#         return False

#     thumb_tip = points[4]

#     palm_center_x = sum(
#         points[i][0] for i in [0, 5, 9, 13, 17]
#     ) / 5
#     palm_center_y = sum(
#         points[i][1] for i in [0, 5, 9, 13, 17]
#     ) / 5

#     palm_center = (palm_center_x, palm_center_y)

#     palm_width = math.dist(points[5], points[17])

#     thumb_distance = math.dist(
#         thumb_tip, palm_center
#     )

#     return thumb_distance < palm_width * 0.45



# # =====================================
# # 6. OPEN WEBCAM
# # =====================================

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("ERROR: Camera cannot open!")
#     raise SystemExit

# print("SakhiSetu Vision started!")
# print("Show your hand in front of camera.")
# print("Press Q to close camera.")

# start_time = time.monotonic()

# # =====================================
# # 7. START HAND DETECTION
# # =====================================

# try:

#     with HandLandmarker.create_from_options(options) as detector:

#         while True:

#             success, frame = cap.read()

#             if not success:
#                 print("Camera frame not received!")
#                 break

#             height, width, _ = frame.shape

#             # Convert BGR to RGB
#             rgb_frame = cv2.cvtColor(
#                 frame,
#                 cv2.COLOR_BGR2RGB
#             )

#             mp_image = mp.Image(
#                 image_format=mp.ImageFormat.SRGB,
#                 data=rgb_frame
#             )

#             timestamp_ms = int(
#                 (time.monotonic() - start_time) * 1000
#             )

#             # Detect hands
#             result = detector.detect_for_video(
#                 mp_image,
#                 timestamp_ms
#             )

#             hand_count = len(
#                 result.hand_landmarks
#             )

#             label = "NO HAND DETECTED"

#             # =================================
#             # 8. PROCESS HAND LANDMARKS
#             # =================================

#             for hand in result.hand_landmarks:

#                 points = []

#                 # Collect 21 landmarks
#                 for landmark in hand:

#                     x = int(landmark.x * width)
#                     y = int(landmark.y * height)

#                     points.append((x, y))
                    
#                 thumb_result=is_thumb_folded(points)
#                 fingers_result=is_fingers_closed_over_thumb(points)
#                 print("Thumb Folded:", thumb_result)
#                 print("Fingers Closed:", fingers_result)

#                 # Safety check
#                 if len(points) != 21:
#                     continue

#                 # Draw hand connections
#                 for start, end in connections:

#                     cv2.line(
#                         frame,
#                         points[start],
#                         points[end],
#                         (0, 255, 0),
#                         2
#                     )

#                 # Draw landmark points and IDs
#                 for i, point in enumerate(points):

#                     cv2.circle(
#                         frame,
#                         point,
#                         5,
#                         (0, 0, 255),
#                         -1
#                     )

#                     cv2.putText(
#                         frame,
#                         str(i),
#                         (point[0] + 5, point[1] - 5),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         0.5,
#                         (255, 255, 0),
#                         2
#                     )

#                 # Open Palm Detection
#                 if is_open_palm(points):

#                     label = "OPEN PALM DETECTED"
                    
#                 elif is_thumb_folded(points):
#                     label="Thumb folded"

#                 else:

#                     label = "HAND DETECTED"

#             # =================================
#             # 9. DISPLAY RESULT
#             # =================================

#             cv2.putText(
#                 frame,
#                 f"Hands detected: {hand_count}",
#                 (20, 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.8,
#                 (255, 255, 255),
#                 2
#             )

#             cv2.putText(
#                 frame,
#                 label,
#                 (20, 80),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (0, 255, 0),
#                 2
#             )

#             cv2.imshow(
#                 "SakhiSetu Vision - Hand Detection",
#                 frame
#             )

#             # Press Q to exit
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break

# finally:

#     cap.release()
#     cv2.destroyAllWindows()
#     print("Camera closed safely.")





##new code 


import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture_recognition import (
    is_open_palm,
    is_thumb_folded,
    is_fingers_closed_over_thumb,
    GestureSequenceDetector
)


model_path = "ai_engine/hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


def main():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera cannot open!")
        return

    detector = GestureSequenceDetector()
    frame_index = 0

    with vision.HandLandmarker.create_from_options(options) as landmarker:

        while True:

            success, frame = camera.read()

            if not success:
                print("Camera frame error!")
                break

            frame = cv2.flip(frame, 1)

            height, width, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp_ms = frame_index * 33
            frame_index += 1

            result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            hand_detected = False
            open_palm = False
            thumb_folded = False
            fingers_closed = False
            alert = False

            if result.hand_landmarks:

                hand_detected = True

                landmarks = result.hand_landmarks[0]
                points = []

                for index, landmark in enumerate(landmarks):
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    points.append((x, y))
                    #draw green landmark points

                    cv2.circle(
                        frame, (x, y), 5, (0, 255, 0), -1
                    )
                    
                    #draw landmark number
                    cv2.putText(
                        frame, str(index), (x+8, y-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,0),
                        2
                    )

                for start, end in connections:
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 0, 0),
                        2
                    )

                open_palm = is_open_palm(points)
                thumb_folded = is_thumb_folded(points)
                fingers_closed = is_fingers_closed_over_thumb(points)

                alert = detector.update(points)

            # Terminal TRUE / FALSE output
            print(
                f"Hand: {hand_detected} | "
                f"Open Palm: {open_palm} | "
                f"Thumb Folded: {thumb_folded} | "
                f"Fingers Closed: {fingers_closed} | "
                f"Alert: {alert}"
            )

            # Show results on webcam screen
            results = [
                ("Hand Detected", hand_detected),
                ("Open Palm", open_palm),
                ("Thumb Folded", thumb_folded),
                ("Fingers Closed", fingers_closed),
                ("SOS Alert", alert)
            ]

            y_position = 35

            for label, value in results:

                text = f"{label}: {value}"

                color = (0, 255, 0) if value else (0, 0, 255)

                cv2.putText(
                    frame,
                    text,
                    (15, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

                y_position += 30

            if alert:
                print("CANDIDATE SOS ALERT GENERATED!")

            cv2.imshow("SakhiSetu Vision", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


