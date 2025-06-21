#!/usr/bin/env python3

import pyautogui
import subprocess
import json
import time
from PIL import ImageGrab
import cv2
import numpy as np

class WindowAwareTargeting:
    """Detect UI windows and target elements within them"""
    
    def __init__(self):
        self.screen_width, self.screen_height = ImageGrab.grab().size
        print(f"📐 Screen: {self.screen_width}x{self.screen_height}")
    
    def get_active_window_info(self):
        """Get information about the currently active window (macOS)"""
        try:
            # Use AppleScript to get active window info
            script = '''
            tell application "System Events"
                set frontApp to first application process whose frontmost is true
                set appName to name of frontApp
                
                tell frontApp
                    try
                        set winPos to position of front window
                        set winSize to size of front window
                        return appName & "|" & (item 1 of winPos) & "," & (item 2 of winPos) & "|" & (item 1 of winSize) & "," & (item 2 of winSize)
                    on error
                        return appName & "|unknown|unknown"
                    end try
                end tell
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                parts = result.stdout.strip().split('|')
                app_name = parts[0]
                
                if len(parts) == 3 and parts[1] != "unknown":
                    pos = list(map(int, parts[1].split(',')))
                    size = list(map(int, parts[2].split(',')))
                    
                    return {
                        'app_name': app_name,
                        'x': pos[0],
                        'y': pos[1], 
                        'width': size[0],
                        'height': size[1],
                        'right': pos[0] + size[0],
                        'bottom': pos[1] + size[1]
                    }
                else:
                    return {'app_name': app_name, 'bounds': 'unknown'}
            
        except Exception as e:
            print(f"❌ Window detection error: {e}")
        
        return None
    
    def detect_browser_window_bounds(self):
        """Detect browser window using visual recognition"""
        
        print("🔍 Detecting browser window visually...")
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        img_array = np.array(screenshot)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Look for window-like rectangles
        # Browser windows typically have:
        # 1. Large rectangular regions
        # 2. White/light backgrounds (for content area)
        # 3. Defined edges
        
        # Find edges
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Find contours (potential window boundaries)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter for window-like rectangles
        potential_windows = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter criteria for browser windows:
            # 1. Reasonable size (not tiny, not full screen)
            # 2. Aspect ratio suggesting a window
            # 3. Not at screen edges (windows have borders)
            
            if (w > 400 and h > 300 and           # Minimum reasonable size
                w < self.screen_width * 0.95 and  # Not full width
                h < self.screen_height * 0.95 and # Not full height  
                x > 10 and y > 10 and             # Not at screen edge
                w/h > 0.7 and w/h < 3):           # Reasonable aspect ratio
                
                potential_windows.append({
                    'x': x, 'y': y, 'width': w, 'height': h,
                    'right': x + w, 'bottom': y + h,
                    'area': w * h,
                    'center': (x + w//2, y + h//2)
                })
        
        # Sort by area (largest likely to be main window)
        potential_windows.sort(key=lambda w: w['area'], reverse=True)
        
        print(f"🔍 Found {len(potential_windows)} potential windows")
        for i, win in enumerate(potential_windows[:3]):
            print(f"  {i+1}. {win['width']}x{win['height']} at ({win['x']}, {win['y']})")
        
        return potential_windows[0] if potential_windows else None
    
    def get_input_coords_within_window(self, window_bounds, app_type="browser"):
        """Calculate input field coordinates within a specific window"""
        
        if not window_bounds:
            print("❌ No window bounds available")
            return None
        
        # Input field patterns relative to window, not screen
        patterns = {
            "browser": {
                "x_factor": 0.5,    # Center of window
                "y_factor": 0.9,    # Bottom 10% of window
                "description": "Browser chat interface"
            },
            "claude": {
                "x_factor": 0.5,    # Center
                "y_factor": 0.85,   # Bit higher in window
                "description": "Claude interface"
            }
        }
        
        pattern = patterns.get(app_type, patterns["browser"])
        
        # Calculate coordinates relative to window
        window_x = window_bounds['x']
        window_y = window_bounds['y'] 
        window_width = window_bounds['width']
        window_height = window_bounds['height']
        
        # Calculate input position within the window
        input_x = window_x + int(window_width * pattern['x_factor'])
        input_y = window_y + int(window_height * pattern['y_factor'])
        
        print(f"🎯 {pattern['description']}")
        print(f"   Window: {window_width}x{window_height} at ({window_x}, {window_y})")
        print(f"   Input coords: ({input_x}, {input_y})")
        print(f"   Relative position: {pattern['x_factor']*100}% across, {pattern['y_factor']*100}% down")
        
        return (input_x, input_y)
    
    def smart_ui_targeting(self, app_name_hint=None):
        """Complete window-aware UI targeting"""
        
        print("🎯 Smart UI Targeting with Window Detection")
        
        # Method 1: Try to get active window info
        window_info = self.get_active_window_info()
        
        if window_info and 'width' in window_info:
            print(f"✅ Active window: {window_info['app_name']}")
            print(f"   Bounds: {window_info['width']}x{window_info['height']} at ({window_info['x']}, {window_info['y']})")
            
            # Determine app type from window info
            app_name = window_info['app_name'].lower()
            if 'chrome' in app_name or 'firefox' in app_name or 'safari' in app_name:
                app_type = "browser"
            else:
                app_type = "claude"
            
            coords = self.get_input_coords_within_window(window_info, app_type)
            return coords, window_info
        
        # Method 2: Visual window detection
        print("🔄 Falling back to visual window detection...")
        visual_window = self.detect_browser_window_bounds()
        
        if visual_window:
            print(f"✅ Detected window visually: {visual_window['width']}x{visual_window['height']}")
            coords = self.get_input_coords_within_window(visual_window, "browser")
            return coords, visual_window
        
        print("❌ Could not detect any UI window")
        return None, None
    
    def test_window_targeting(self):
        """Test the complete window-aware targeting system"""
        
        coords, window_info = self.smart_ui_targeting()
        
        if not coords:
            print("❌ No target coordinates found")
            return False
        
        print(f"\n🎯 Testing coordinates: {coords}")
        print("Switch to your chat app - testing in 3 seconds...")
        time.sleep(3)
        
        # Visual feedback
        pyautogui.moveTo(coords[0], coords[1], duration=1)
        time.sleep(0.5)
        
        # Test click and type
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.5)
        
        test_message = "Window-aware targeting test!"
        pyautogui.typewrite(test_message)
        time.sleep(1)
        
        success = input("Did the text appear in the correct input field? (y/n): ")
        return success.lower() == 'y'

if __name__ == "__main__":
    print("🔍 Window-Aware UI Targeting")
    print("Solving the 'background clutter' problem!")
    
    detector = WindowAwareTargeting()
    
    # Test the system
    success = detector.test_window_targeting()
    
    if success:
        print("🎉 SUCCESS! Window-aware targeting working!")
        print("Now you can target UI elements within specific windows!")
    else:
        print("🔧 Needs refinement - but the approach is sound!")
    
    print(f"\n💡 Key insight: Always detect the WINDOW first, then target within it!")