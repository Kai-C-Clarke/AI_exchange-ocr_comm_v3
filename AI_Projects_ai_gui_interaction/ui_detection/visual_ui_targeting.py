import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui

def find_input_field_visual():
    """Find input field using visual patterns instead of text"""
    
    # Capture screen
    screenshot = ImageGrab.grab()
    img_array = np.array(screenshot)
    
    # Convert to OpenCV format
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Find rectangular shapes (likely input fields)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter for input-field-like rectangles
    potential_inputs = []
    
    screen_height, screen_width = gray.shape
    bottom_half_y = screen_height // 2
    
    for contour in contours:
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter criteria for input fields:
        # 1. In bottom half of screen
        # 2. Wide but not too tall (aspect ratio)
        # 3. Reasonable size
        
        if (y > bottom_half_y and  # Bottom half
            w > 200 and w < screen_width * 0.8 and  # Wide but not full screen
            h > 30 and h < 100 and  # Not too tall
            w/h > 3):  # Wide aspect ratio
            
            potential_inputs.append({
                'bbox': (x, y, w, h),
                'center': (x + w//2, y + h//2),
                'area': w * h,
                'y_position': y  # For sorting by vertical position
            })
    
    # Sort by y position (lowest = most likely input)
    potential_inputs.sort(key=lambda x: x['y_position'], reverse=True)
    
    print(f"🔍 Found {len(potential_inputs)} potential input fields:")
    for i, field in enumerate(potential_inputs[:3]):  # Show top 3
        x, y, w, h = field['bbox']
        print(f"  {i+1}. Rectangle at ({x},{y}) size {w}x{h}, center: {field['center']}")
    
    return potential_inputs[0]['center'] if potential_inputs else None

def find_send_button_visual():
    """Find send button using visual patterns"""
    
    # This would look for button-like shapes near input fields
    # Often circular or rounded rectangle, possibly with an icon
    
    screenshot = ImageGrab.grab()
    img_array = np.array(screenshot)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Look for circular shapes (send buttons are often circular)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Use HoughCircles to find circular buttons
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
                              param1=50, param2=30, minRadius=15, maxRadius=50)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Filter circles in bottom area (where send buttons usually are)
        screen_height, screen_width = gray.shape
        bottom_third = screen_height * 2 // 3
        
        for (x, y, r) in circles:
            if y > bottom_third:
                print(f"🎯 Potential send button (circle) at ({x},{y}) radius {r}")
                return (x, y)
    
    return None

# Add this to your UIIntelligence class
def enhanced_input_detection(self):
    """Try multiple detection methods"""
    
    # Method 1: Text-based (your current approach)
    text_coords = self.fuzzy_locate_text("Ask anything", threshold=0.6)
    if text_coords:
        print("✅ Found via text detection")
        return text_coords
    
    # Method 2: Visual pattern detection
    visual_coords = find_input_field_visual()
    if visual_coords:
        print("✅ Found via visual pattern detection")
        return visual_coords
    
    # Method 3: Position-based guess (fallback)
    screenshot = ImageGrab.grab()
    screen_width, screen_height = screenshot.size
    
    # ChatGPT input is typically bottom-center
    fallback_coords = (screen_width // 2, int(screen_height * 0.85))
    print(f"🟡 Using fallback position: {fallback_coords}")
    return fallback_coords