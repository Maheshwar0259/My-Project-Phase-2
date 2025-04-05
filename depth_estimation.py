import torch
import cv2
import numpy as np
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image

# Initialize MiDaS Model
def load_midas_model():
    model_type = "DPT_Large"  # Options: "DPT_Large", "DPT_Hybrid", "MiDaS_small"
    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    midas.eval()

    # Transformation pipeline specific to MiDaS
    midas_transforms = Compose([
        Resize(384),  # Resize to 384x384 for compatibility
        ToTensor(),   # Convert image to tensor
        Normalize(mean=[0.5], std=[0.5])  # Normalize to range [-1, 1]
    ])

    # Set device to CUDA if available, otherwise fallback to CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    midas.to(device)

    return midas, midas_transforms, device

# Process a frame and return the depth map
def process_frame_with_depth(frame, midas, midas_transforms, device):
    # Convert the frame to RGB and create a PIL Image
    input_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Apply the transformation pipeline
    input_tensor = midas_transforms(input_image).unsqueeze(0).to(device)

    # Perform depth estimation using MiDaS
    with torch.no_grad():
        depth_map = midas(input_tensor)

    # Resize the depth map back to the original frame's resolution
    depth_map = torch.nn.functional.interpolate(
        depth_map.unsqueeze(1),
        size=frame.shape[:2],
        mode="bicubic",
        align_corners=False,
    ).squeeze().cpu().numpy()

    # Normalize the depth map for visualization
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return depth_map_normalized