import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2


class BoneCancerDetector:
    """YOLO-based bone cancer detector"""
    
    def __init__(self, model_path):
        """Initialize the detector with the fine-tuned model"""
        self.model = YOLO(model_path)
        self.class_names = ['cancer', 'normal']
        
    def predict(self, image_path):
        """
        Predict if the X-ray shows cancer or normal bone
        
        Args:
            image_path: Path to the X-ray image
            
        Returns:
            dict: Prediction results with class and confidences
        """
        # Run prediction
        results = self.model(image_path, verbose=False)
        
        # Extract results
        result = results[0]
        probs = result.probs.data.cpu().numpy()
        
        # Get class names (ensure correct mapping)
        # probs[0] = cancer confidence, probs[1] = normal confidence
        confidence_cancer = float(probs[0])
        confidence_normal = float(probs[1])
        
        # Determine predicted class
        predicted_class = self.class_names[np.argmax(probs)]
        
        return {
            'prediction_class': predicted_class,
            'confidence_cancer': confidence_cancer,
            'confidence_normal': confidence_normal,
            'max_confidence': max(confidence_cancer, confidence_normal)
        }
    
    def get_feature_maps(self, image_path):
        """
        Extract feature maps for GradCAM visualization
        
        Args:
            image_path: Path to the X-ray image
            
        Returns:
            tuple: (feature_maps, model_output)
        """
        # Load and preprocess image
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Run prediction with feature extraction
        results = self.model(image_path, verbose=False)
        
        return results[0]
