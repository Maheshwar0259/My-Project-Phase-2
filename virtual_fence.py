import numpy as np
import cv2

# Define the virtual fence as a polygon
virtual_fence = np.array([[100, 100], [500, 100], [500, 400], [100, 400]], np.int32)
virtual_fence = virtual_fence.reshape((-1, 1, 2))

def check_breach(object_center):
    """
    Check if the detected object is inside the virtual fence.
    Returns True if there's a breach, False otherwise.
    """
    return cv2.pointPolygonTest(virtual_fence, object_center, False) >= 0

def draw_fence(frame):
    """
    Draws the virtual fence on the frame.
    """
    cv2.polylines(frame, [virtual_fence], isClosed=True, color=(0, 255, 0), thickness=2)
    return frame