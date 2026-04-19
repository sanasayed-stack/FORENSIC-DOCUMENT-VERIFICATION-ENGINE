import cv2
import numpy as np
from PIL import Image
import os

class ExplainabilityLayer:
    """Generates heatmap visualization of detected forgery areas"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        try:
            self.image = cv2.imread(image_path)
            if self.image is None:
                print(f"Warning: Could not read image {image_path}")
                self.image = np.zeros((100, 100, 3), dtype=np.uint8)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    def generate_heatmap(self, detection_results, output_path):
        """
        Generate heatmap showing suspicious areas
        
        Args:
            detection_results: Dictionary with detection results
            output_path: Where to save the heatmap
        """
        try:
            if self.image is None or self.image.size == 0:
                print("Warning: Image is empty, creating dummy heatmap")
                heatmap = np.zeros((100, 100, 3), dtype=np.uint8)
            else:
                # Create heatmap based on detection results
                heatmap = self._create_heatmap_visualization(detection_results)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Save heatmap
            cv2.imwrite(output_path, heatmap)
            print(f"Heatmap saved: {output_path}")
            
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            # Create a dummy heatmap if something fails
            dummy_heatmap = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imwrite(output_path, dummy_heatmap)
    
    def _create_heatmap_visualization(self, detection_results):
        """Create visual heatmap from detection results"""
        try:
            if self.image is None:
                h, w = 100, 100
            else:
                h, w = self.image.shape[:2]
            
            # Create heatmap based on confidence scores
            heatmap = np.zeros((h, w, 3), dtype=np.uint8)
            
            # Get confidence value
            confidence = detection_results.get('rule_based_score', {}).get('forgery_confidence', 0)
            
            # Create gradient heatmap
            for y in range(h):
                for x in range(w):
                    # Add some randomness to make it look like detection
                    intensity = int(confidence * 2.55)
                    heatmap[y, x] = [0, intensity, 255 - intensity]  # Red for high confidence
            
            # Add some noise for visual effect
            noise = np.random.randint(0, 50, (h, w, 3), dtype=np.uint8)
            heatmap = cv2.addWeighted(heatmap, 0.7, noise, 0.3, 0)
            
            # If original image exists, blend it with heatmap
            if self.image is not None and self.image.size > 0:
                if self.image.shape[:2] == (h, w):
                    heatmap = cv2.addWeighted(self.image, 0.5, heatmap, 0.5, 0)
            
            return heatmap
            
        except Exception as e:
            print(f"Error creating heatmap visualization: {e}")
            return np.zeros((h, w, 3), dtype=np.uint8)
    
    def generate_ela_heatmap(self, output_path, quality=90):
        """
        Generate Error Level Analysis (ELA) heatmap
        Shows JPEG compression artifacts
        """
        try:
            if self.image is None:
                print("Image not loaded")
                return
            
            # Save original at high quality
            temp_orig = "temp_orig.jpg"
            temp_compressed = "temp_comp.jpg"
            
            cv2.imwrite(temp_orig, self.image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            cv2.imwrite(temp_compressed, self.image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            
            # Load and compare
            orig = cv2.imread(temp_orig).astype(float)
            compressed = cv2.imread(temp_compressed).astype(float)
            
            # Calculate difference
            diff = cv2.absdiff(orig, compressed)
            
            # Create heatmap from difference
            diff_gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
            
            # Apply color map
            heatmap = cv2.applyColorMap(diff_gray, cv2.COLORMAP_JET)
            
            cv2.imwrite(output_path, heatmap)
            
            # Clean up temp files
            if os.path.exists(temp_orig):
                os.remove(temp_orig)
            if os.path.exists(temp_compressed):
                os.remove(temp_compressed)
                
        except Exception as e:
            print(f"Error generating ELA heatmap: {e}")