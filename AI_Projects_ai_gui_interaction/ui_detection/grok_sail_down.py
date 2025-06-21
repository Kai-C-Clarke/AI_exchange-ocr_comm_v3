#!/usr/bin/env python3
"""
Grok Sail Down Targeting
Mouse needs to go DOWN into the input box
"""

import pyautogui
import subprocess
import time

class GrokSailDown:
    """Navigate the mouse DOWN into Grok's input waters"""
    
    def __init__(self):
        # Grok's input area: (1255, 970) to (1841, 1006)
        # Mouse is getting close but needs to sail DOWN
        
        self.grok_area = {
            'left': 1255,
            'right': 1841,
            'top': 970,      # Top edge - probably where mouse is hitting
            'bottom': 1006,  # Bottom edge - need to get closer to here
            'width': 586,    # 1841 - 1255
            'height': 36     # 1006 - 970 (very narrow!)
        }
        
        print("Grok Sail Down Targeting")
        print(f"Input box height: {self.grok_area['height']} pixels (very narrow!)")
        print("Strategy: Keep X coordinate, sail mouse DOWN")
    
    def switch_to_grok_desktop(self):
        """Navigate to Grok's waters (Desktop 2)"""
        print("🧭 Sailing to Desktop 2...")
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1.5)
    
    def sail_down_test(self):
        """Test Y coordinates sailing DOWN into the input box"""
        
        # Keep X coordinate centered, but test Y coordinates going DOWN
        center_x = 1548  # Keep this - it was close
        
        # Test Y coordinates from TOP to BOTTOM of the input area
        # With extra coordinates BELOW the detected area in case it's slightly off
        
        test_y_coordinates = [
            970,   # Very top of area
            975,   # Quarter down
            980,   # Halfway down  
            985,   # Three-quarters down
            990,   # Near bottom
            995,   # Bottom area
            1000,  # Near very bottom
            1006,  # Bottom edge of your area
            1010,  # Just below your area (in case measurement was off)
            1015,  # Further below
            1020,  # Even further below
        ]
        
        print(f"\n⬇️ SAILING MOUSE DOWN - Testing {len(test_y_coordinates)} Y coordinates")
        print(f"Keeping X at {center_x}, varying Y from {min(test_y_coordinates)} to {max(test_y_coordinates)}")
        
        for i, test_y in enumerate(test_y_coordinates):
            print(f"\n--- Sail Down Test {i+1}: ({center_x}, {test_y}) ---")
            
            # Navigate to Grok's desktop
            self.switch_to_grok_desktop()
            
            # Sail the mouse down to this coordinate
            print(f"🧭 Sailing mouse DOWN to ({center_x}, {test_y})")
            pyautogui.moveTo(center_x, test_y, duration=2)
            time.sleep(1)
            
            # Visual check
            position_good = input(f"Mouse at ({center_x}, {test_y}) - Is this INSIDE Grok's input box? (y/n): ")
            
            if position_good.lower() == 'y':
                print("🎯 Good position! Testing click and type...")
                
                # Test the full sequence
                pyautogui.click(center_x, test_y)
                time.sleep(0.5)
                
                test_message = f"Sail down test {i+1} - Y coordinate {test_y}"
                self.type_with_applescript(test_message)
                time.sleep(0.5)
                
                pyautogui.press("enter")
                time.sleep(1)
                
                # Return to base for status report
                self.return_to_base()
                
                success = input(f"🎉 Did test {i+1} work? Did Grok receive the message? (y/n): ")
                
                if success.lower() == 'y':
                    print(f"⚓ ANCHORED! Success coordinates: ({center_x}, {test_y})")
                    return (center_x, test_y)
                else:
                    print(f"❌ Test {i+1} failed, sailing to next coordinate...")
            else:
                print(f"🌊 Still not in the right waters, sailing further down...")
                # Return to base and try next coordinate
                self.return_to_base()
        
        print("🌊 All coordinates tested - no safe harbor found")
        return None
    
    def type_with_applescript(self, text: str):
        """Kai's proven typing method"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.3)
    
    def return_to_base(self):
        """Return to Desktop 0 (home port)"""
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
    
    def precision_down_adjustment(self):
        """Fine-tune the Y coordinate with precision"""
        
        print("\n🎯 PRECISION DOWN ADJUSTMENT")
        print("Fine-tuning Y coordinate with small adjustments")
        
        base_x = 1548
        base_y = 988  # Current coordinate that gets close
        
        # Test small adjustments DOWN from the current position
        adjustments = [
            0,    # Current position
            +2,   # 2 pixels down
            +4,   # 4 pixels down
            +6,   # 6 pixels down  
            +8,   # 8 pixels down
            +10,  # 10 pixels down
            +12,  # 12 pixels down
            +15,  # 15 pixels down
            +18,  # 18 pixels down
            +20,  # 20 pixels down
        ]
        
        print(f"Testing small DOWN adjustments from base position ({base_x}, {base_y})")
        
        for i, adjustment in enumerate(adjustments):
            test_y = base_y + adjustment
            
            print(f"\n--- Precision Test {i+1}: DOWN +{adjustment} pixels to ({base_x}, {test_y}) ---")
            
            self.switch_to_grok_desktop()
            
            pyautogui.moveTo(base_x, test_y, duration=1.5)
            time.sleep(0.5)
            
            looks_good = input(f"Position ({base_x}, {test_y}) - Does this look right? (y/n): ")
            
            if looks_good.lower() == 'y':
                # Test it
                pyautogui.click(base_x, test_y)
                time.sleep(0.5)
                
                self.type_with_applescript(f"Precision test DOWN +{adjustment} pixels")
                time.sleep(0.5)
                pyautogui.press("enter")
                
                self.return_to_base()
                
                worked = input(f"Did precision adjustment +{adjustment} work? (y/n): ")
                if worked.lower() == 'y':
                    print(f"🎯 PRECISION SUCCESS! Coordinates: ({base_x}, {test_y})")
                    return (base_x, test_y)
            
            self.return_to_base()
        
        print("🎯 Precision adjustment complete")
        return None

def main():
    """Sail the mouse down into Grok's input waters"""
    
    grok = GrokSailDown()
    
    print("\n⛵ GROK SAIL DOWN TARGETING")
    print("Navigate the mouse DOWN into Grok's narrow input waters")
    
    choice = input(f"\nChoose navigation method:\n1. Sail down test (broad Y coordinate range)\n2. Precision down adjustment (fine-tuning)\nChoice: ")
    
    if choice == "1":
        success_coords = grok.sail_down_test()
        if success_coords:
            print(f"\n⚓ HARBOR FOUND! Use these Grok coordinates: {success_coords}")
        else:
            print("\n🌊 No safe harbor found - try precision method")
    
    elif choice == "2":
        success_coords = grok.precision_down_adjustment()
        if success_coords:
            print(f"\n🎯 PRECISION ANCHORED! Use these coordinates: {success_coords}")
    
    print(f"\n⛵ Navigation complete - ready to set sail for success!")

if __name__ == "__main__":
    main()