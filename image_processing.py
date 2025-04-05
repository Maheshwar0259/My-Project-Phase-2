import cv2
import time
from collections import deque
import numpy as np
from virtual_fence import check_breach, draw_fence
from alert_system import send_alert
from depth_estimation import process_frame_with_depth


# Initialize FPS calculation variables
fps_queue = deque(maxlen=30)
last_frame_time = time.time()
last_alert_time = 0
ALERT_COOLDOWN = 3.0  # seconds between alerts

# def calculate_fps():
#     global last_frame_time
#     current_time = time.time()
#     fps = 1 / (current_time - last_frame_time)
#     fps_queue.append(fps)
#     last_frame_time = current_time
#     return np.mean(fps_queue)

def process_frame(frame, results):
    """
    Process the frame for object detection and breach detection.
    Draws the detected objects and checks if they breach the virtual fence.
    """
    global last_alert_time
    current_time = time.time()

    # Skip processing if insufficient time has passed (frame limiting)
    if current_time - last_frame_time < 0.01:  # Limit to ~100 FPS max
        return frame

    if len(results) and len(results[0].boxes):
        for obj in results[0].boxes:
            # Get object coordinates
            object_center = (int((obj.xyxy[0][0] + obj.xyxy[0][2]) // 2),
                            int((obj.xyxy[0][1] + obj.xyxy[0][3]) // 2))

            # Check if the object breaches the virtual fence
            if check_breach(object_center):
                if current_time - last_alert_time > ALERT_COOLDOWN:
                    send_alert("Breach detected at the virtual fence!")
                    last_alert_time = current_time
                
                cv2.putText(frame, "Breach!", (object_center[0], object_center[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Annotate object on the frame
            cv2.putText(frame, "Object Detected", (object_center[0], object_center[1] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Draw the virtual fence on the frame
    frame = draw_fence(frame)

    # Calculate and display FPS
    # fps = calculate_fps()
    # cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame