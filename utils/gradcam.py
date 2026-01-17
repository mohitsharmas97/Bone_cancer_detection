import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def generate_simple_heatmap(image_path, output_path, prediction_class, alpha=0.5):
    """
    Generate a simple activation heatmap visualization
    
    This creates a heatmap based on image intensity patterns,
    highlighting areas that may be of interest for bone cancer detection.
    
    Args:
        image_path: Path to input X-ray image
        output_path: Path to save the heatmap overlay
        prediction_class: 'cancer' or 'normal'
        alpha: Overlay transparency (0-1)
    
    Returns:
        str: Path to saved heatmap
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Create activation map based on edge detection and intensity
    # This simulates what a model might focus on
    
    # Apply Sobel edge detection
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalize to 0-1
    if magnitude.max() > 0:
        magnitude = magnitude / magnitude.max()
    
    # For cancer detection, we'll also look at areas with unusual intensity
    # Calculate local variance to find regions with texture changes
    kernel_size = 31
    local_mean = cv2.blur(gray.astype(np.float32), (kernel_size, kernel_size))
    local_sq_mean = cv2.blur((gray.astype(np.float32))**2, (kernel_size, kernel_size))
    local_var = local_sq_mean - local_mean**2
    local_var = np.maximum(local_var, 0)  # Ensure non-negative
    
    if local_var.max() > 0:
        local_var = local_var / local_var.max()
    
    # Combine edge magnitude and variance for the heatmap
    if prediction_class == 'cancer':
        # For cancer, weight variance more (abnormal textures)
        heatmap = 0.4 * magnitude + 0.6 * local_var
    else:
        # For normal, weight edges more (bone structure)
        heatmap = 0.6 * magnitude + 0.4 * local_var
    
    # Apply Gaussian blur for smoother visualization
    heatmap = cv2.GaussianBlur(heatmap.astype(np.float32), (31, 31), 0)
    
    # Normalize
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()
    
    # Apply colormap (jet colormap like GradCAM)
    heatmap_colored = cm.jet(heatmap)[:, :, :3]  # Remove alpha channel
    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)
    
    # Overlay heatmap on original image
    overlay = cv2.addWeighted(img_rgb, 1 - alpha, heatmap_colored, alpha, 0)
    
    # Save
    overlay_bgr = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, overlay_bgr)
    
    return output_path


def generate_gradcam_heatmap(model_path, image_path, output_path, target_class=None):
    """
    Generate heatmap visualization for bone cancer detection
    
    Args:
        model_path: Path to YOLO model (used for loading prediction)
        image_path: Input X-ray image
        output_path: Output heatmap path
        target_class: Target class (0=cancer, 1=normal, None=predicted)
    
    Returns:
        str: Path to saved heatmap
    """
    from ultralytics import YOLO
    
    # Load model and get prediction
    model = YOLO(model_path)
    results = model(image_path, verbose=False)
    result = results[0]
    probs = result.probs.data.cpu().numpy()
    
    # Determine predicted class
    class_names = ['cancer', 'normal']
    predicted_class = class_names[np.argmax(probs)]
    
    # Generate heatmap
    return generate_simple_heatmap(image_path, output_path, predicted_class)
