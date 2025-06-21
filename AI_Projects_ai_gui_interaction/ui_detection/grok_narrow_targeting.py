#!/usr/bin/env python3
"""
Grok Narrow Input Box Targeting
Testing coordinates specifically for narrow input fields
"""

import pyautogui
import subprocess
import time

class GrokNarrowTargeting:
    """Target Grok's narrow input box precisely"""
    
    def __init__(self):
        # Grok's input area: (1255, 970) to (1841, 1006)
        # Height = 36 pixels, Width = 586 pixels
        
        self.grok_area = {
            'left': 1255,
            'right': 1841, 
            'top': 970,
            'bottom': 1006,
            'center_x': 1548,
            'center_y': 988
        }
        
        print("Grok Narrow Input Box Targeting")
        print(f"Area: {self.grok_area['left']},{self.grok_area['top']} to {self.grok_area['right']},{self.grok_area['bottom']}")
        print(f"Size: {self.grok_area['right'] - self.grok_area['left']}w x {self.grok_area['bottom'] - self.grok_area['top']}h pixels")
    
    def switch_to_grok_desktop(self):
        """Switch to Desktop 2 (Grok's desktop)"""
        print("Switching to Desktop 2...")
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1.5)
    
    def test_narrow_coordinates(self):
        """Test coordinates specifically for narrow input box"""
        
        # Test multiple points within the narrow box
        # Stay well inside the boundaries to ensure we hit the input area
        
        test_coords = [
            # Center area - but adjusted for narrow box
            (1548, 988),  # Original center
            
            # Slightly left of center (in case center hits a border)
            (1500, 988),
            (1450, 988),
            (1400, 988),
            
            # Slightly right of center
            (1600, 988),
            (1650, 988),
            (1700, 988),
            
            # Adjust Y coordinate - maybe input is higher/lower
            (1548, 975),  # Higher in the box
            (1548, 980),
            (1548, 985),
            (1548, 990),
            (1548, 995),  # Lower in the box
            (1548, 1000),
            
            # Conservative coordinates - well inside the area
            (1350, 985),  # Left side but well inside
            (1750, 985),  # Right side but well inside
        ]
        
        print(f"\nTesting {len(test_coords)} coordinate positions in Grok's narrow input box")
        
        for i, (x, y) in enumerate(test_coords):
            print(f"\n--- Test {i+1}: ({x}, {y}) ---")
            
            # Switch to Grok's desktop
            self.switch_to_grok_desktop()
            
            # Move mouse slowly so you can see exactly where it goes
            print(f"Moving mouse to ({x}, {y})...")
            pyautogui.moveTo(x, y, duration=2)  # Slow movement
            time.sleep(1)
            
            # Check if position looks good
            position_ok = input(f"Is mouse over Grok's input box? (y/n): ")
            
            if position_ok.lower() == 'y':
                # Test clicking
                print("Testing click...")
                pyautogui.click(x, y)
                time.sleep(0.5)
                
                # Test typing
                print("Testing typing...")
                self.type_with_applescript(f"Test {i+1} for narrow input box")
                time.sleep(0.5)
                
                # Test sending
                print("Testing send...")
                pyautogui.press("enter")
                time.sleep(1)
                
                # Check if it worked
                worked = input(f"Did Test {i+1} work? Did Grok receive the message? (y/n): ")
                
                if worked.lower() == 'y':
                    print(f"🎉 SUCCESS! Working Grok coordinates: ({x}, {y})")
                    return (x, y)
                    
            else:
                print(f"Position {i+1} not over input box, trying next...")
                
            # Return to desktop 0 for next input
            pyautogui.hotkey("ctrl", "left")
            time.sleep(1)
            pyautogui.hotkey("ctrl", "left") 
            time.sleep(1)
        
        print("❌ No working coordinates found")
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
    
    def manual_coordinate_finder(self):
        """Manual method - you guide the mouse"""
        
        print("\n🎯 MANUAL COORDINATE FINDER")
        print("You'll manually position the mouse over Grok's input box")
        
        self.switch_to_grok_desktop()
        
        print("\nInstructions:")
        print("1. Manually move your mouse over Grok's input box")
        print("2. Make sure the cursor is clearly INSIDE the input area")
        print("3. Come back to Terminal and press Enter")
        
        input("Position mouse over Grok's input box, then press Enter...")
        
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        print(f"Mouse position: ({current_x}, {current_y})")
        
        # Test this position
        print("Testing this manual position...")
        pyautogui.click(current_x, current_y)
        time.sleep(0.5)
        
        self.type_with_applescript("Manual position test for Grok")
        time.sleep(0.5)
        pyautogui.press("enter")
        
        # Return to desktop 0
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        
        worked = input(f"Did manual position ({current_x}, {current_y}) work? (y/n): ")
        
        if worked.lower() == 'y':
            print(f"🎉 Manual success! Use coordinates: ({current_x}, {current_y})")
            return (current_x, current_y)
        else:
            print("Manual positioning didn't work either")
            return None

def main():
    """Test Grok's narrow input targeting"""
    
    grok = GrokNarrowTargeting()
    
    print("\nGROK NARROW INPUT BOX TARGETING")
    print("Special handling for Grok's very narrow input field")
    
    choice = input(f"\nChoose method:\n1. Test multiple coordinates automatically\n2. Manual coordinate finder\nChoice: ")
    
    if choice == "1":
        working_coords = grok.test_narrow_coordinates()
        if working_coords:
            print(f"\n✅ SUCCESS! Use these Grok coordinates: {working_coords}")
        else:
            print("\n❌ Automatic testing failed - try manual method")
    
    elif choice == "2":
        working_coords = grok.manual_coordinate_finder()
        if working_coords:
            print(f"\n✅ SUCCESS! Use these Grok coordinates: {working_coords}")
    
    print("\nGrok targeting test complete!")

if __name__ == "__main__":
    main()