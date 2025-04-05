import cv2
import time
from collections import deque
from ultralytics import YOLO
from virtual_fence import check_breach
from alert_system import send_alert
from image_processing import process_frame

# Initialize the YOLO model
model = YOLO("yolov8n.pt")

# FPS calculation variables
fps_queue = deque(maxlen=30)
last_time = time.time()
frame_counter = 0
PROCESS_EVERY_N_FRAMES = 3  # Process every 3rd frame

# Start the surveillance system
def start_surveillance():
    cap = cv2.VideoCapture(0)  # Use 0 for camera feed or replace with a video file path
    
    # Set lower resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Get initial frame for when we skip processing
    ret, last_processed_frame = cap.read()
    last_results = [type('EmptyResult', (), {'boxes': []})()]  # Empty result object

    while True:
        global frame_counter, last_time
        
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_counter += 1
        
        # Only process every Nth frame
        if frame_counter % PROCESS_EVERY_N_FRAMES == 0:
            # Detect objects in the frame
            results = model(frame, conf=0.5)  # Increased confidence threshold
            last_processed_frame = frame
            last_results = results
        else:
            # Use the last processed frame's results
            results = last_results
        
        # Process the frame (virtual fencing and breach detection)
        processed_frame = process_frame(frame, results)
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - last_time)
        last_time = current_time
        fps_queue.append(fps)
        avg_fps = sum(fps_queue) / len(fps_queue)
        
        cv2.putText(processed_frame, f'FPS: {avg_fps:.1f}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Encode the frame for the Flask stream
        ret, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()