#!/usr/bin/env python3

import pyautogui
import time
from subprocess import check_output

def test_exact_coordinates():
    """Test the manually measured coordinates"""
    
    # Input field boundaries: (456, 960) to (1035, 1011)
    input_bounds = {
        'left': 456,
        'right': 1035, 
        'top': 960,
        'bottom': 1011
    }
    
    # Calculate center point
    center_x = (input_bounds['left'] + input_bounds['right']) // 2
    center_y = (input_bounds['top'] + input_bounds['bottom']) // 2
    coords = (center_x, center_y)
    
    print("🎯 Testing Exact Coordinates")
    print(f"Input field bounds: {input_bounds}")
    print(f"Calculated center: {coords}")
    print("Switch to Kai's UI - testing in 3 seconds...")
    time.sleep(3)
    
    # Visual confirmation - move mouse to show the click point
    print("🖱️ Moving to target...")
    pyautogui.moveTo(coords[0], coords[1], duration=1)
    time.sleep(1)
    
    # Click the input field
    print("🖱️ Clicking input field...")
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    
    # Type test message
    test_message = "Phase 1 coordinate targeting successful!"
    print(f"⌨️ Typing: {test_message}")
    pyautogui.typewrite(test_message)
    time.sleep(1)
    
    # Select all and copy
    print("📋 Copying content...")
    pyautogui.hotkey("command", "a")
    time.sleep(0.2)
    pyautogui.hotkey("command", "c")
    time.sleep(0.2)
    
    # Verify clipboard
    try:
        clipboard_content = check_output("pbpaste", universal_newlines=True).strip()
        print(f"✅ Clipboard: '{clipboard_content}'")
        
        if test_message in clipboard_content:
            print("🎉 PERFECT! Exact coordinates working!")
            return True, coords
        else:
            print("⚠️ Clipboard mismatch - may have clicked wrong area")
            return False, coords
            
    except Exception as e:
        print(f"❌ Clipboard error: {e}")
        return False, coords

def update_ui_intelligence_class():
    """Generate the updated UIIntelligence class with exact coordinates"""
    
    updated_code = '''
# Updated UIIntelligence with exact Kai coordinates

class UIIntelligence:
    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Exact coordinates for Kai's input field
        self.kai_input_bounds = {
            'left': 456,
            'right': 1035,
            'top': 960, 
            'bottom': 1011,
            'center': (745, 985)  # Pre-calculated center
        }

    def click_kai_input(self):
        """Click Kai's input field using exact coordinates"""
        coords = self.kai_input_bounds['center']
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)  # Allow focus to register
        return coords

    def capture_kai_input(self):
        """Complete capture workflow for Kai's input field"""
        # Click to focus
        coords = self.click_kai_input()
        
        # Select all content
        pyautogui.hotkey("command", "a")
        time.sleep(0.1)
        
        # Copy to clipboard  
        pyautogui.hotkey("command", "c")
        time.sleep(0.1)
        
        # Get clipboard content
        content = self.get_clipboard_text()
        
        return {
            'coords': coords,
            'content': content,
            'success': len(content.strip()) > 0
        }
'''
    
    print("\n📝 Updated UIIntelligence class:")
    print(updated_code)
    return updated_code

if __name__ == "__main__":
    success, coords = test_exact_coordinates()
    
    if success:
        print(f"\n🎉 PHASE 1 COMPLETE!")
        print(f"✅ Working coordinates: {coords}")
        print("✅ Click targeting: SUCCESS")
        print("✅ Text input: SUCCESS") 
        print("✅ Clipboard capture: SUCCESS")
        
        print(f"\n📋 Add this to your ui_intelligence.py:")
        print(f"self.kai_input_coords = {coords}")
        
        update_ui_intelligence_class()
        
    else:
        print(f"\n🔧 Coordinates {coords} need adjustment")
        print("Try clicking slightly different points within the input field")