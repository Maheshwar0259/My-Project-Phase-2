import numpy as np
def calculate_object_distance(depth_map, bbox):
    x1, y1, x2, y2 = bbox  # Bounding box coordinates
    object_region = depth_map[y1:y2, x1:x2]
    avg_distance = np.mean(object_region)  # Calculate average depth
    return avg_distance
