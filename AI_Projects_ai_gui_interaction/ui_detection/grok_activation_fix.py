#!/usr/bin/env python3
"""
Grok Activation Fix
Handle dynamic input box that doubles in size when activated
"""

import pyautogui
import subprocess
import time

class GrokActivationFix:
    """Fix Grok's dynamic input box activation"""
    
    def __init__(self):
        print("Grok Activation Fix")
        print("Handling dynamic input box that doubles when activated")
        
        # Grok coordinates - we know mouse gets to the area
        self.grok_coords = (1548, 1000)  # Adjust based on your successful positioning
        
    def switch_to_grok_desktop(self):
        """Navigate to Desktop 2"""
        print("🧭 Switching to Desktop 2...")
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "right") 
        time.sleep(1.5)
    
    def return_to_base(self):
        """Return to Desktop 0"""
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
    
    def test_activation_methods(self):
        """Test different ways to activate Grok's input box"""
        
        print("\n🎯 TESTING GROK ACTIVATION METHODS")
        print("Trying different ways to activate the dynamic input box")
        
        x, y = self.grok_coords
        
        # Method 1: Single click
        print(f"\n--- Method 1: Single Click ---")
        self.switch_to_grok_desktop()
        
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(1)  # Wait for activation
        
        activated = input(f"Method 1: Did the input box double in size and get activated? (y/n): ")
        
        if activated.lower() == 'y':
            print("✅ Single click works! Testing typing...")
            self.test_typing()
            self.return_to_base()
            worked = input("Did typing work with single click? (y/n): ")
            if worked.lower() == 'y':
                return "single_click"
        
        self.return_to_base()
        
        # Method 2: Double click
        print(f"\n--- Method 2: Double Click ---")
        self.switch_to_grok_desktop()
        
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.doubleClick(x, y)
        time.sleep(1)
        
        activated = input(f"Method 2: Did double click activate the input box? (y/n): ")
        
        if activated.lower() == 'y':
            print("✅ Double click works! Testing typing...")
            self.test_typing()
            self.return_to_base()
            worked = input("Did typing work with double click? (y/n): ")
            if worked.lower() == 'y':
                return "double_click"
        
        self.return_to_base()
        
        # Method 3: Click and wait longer
        print(f"\n--- Method 3: Click + Extended Wait ---")
        self.switch_to_grok_desktop()
        
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        print("Waiting 3 seconds for delayed activation...")
        time.sleep(3)  # Extended wait
        
        activated = input(f"Method 3: Did extended wait activate the box? (y/n): ")
        
        if activated.lower() == 'y':
            print("✅ Extended wait works! Testing typing...")
            self.test_typing()
            self.return_to_base()
            worked = input("Did typing work with extended wait? (y/n): ")
            if worked.lower() == 'y':
                return "click_extended_wait"
        
        self.return_to_base()
        
        # Method 4: Multiple clicks
        print(f"\n--- Method 4: Multiple Clicks ---")
        self.switch_to_grok_desktop()
        
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        
        # Try multiple clicks to force activation
        for i in range(3):
            pyautogui.click(x, y)
            time.sleep(0.3)
        
        time.sleep(1)
        
        activated = input(f"Method 4: Did multiple clicks activate the box? (y/n): ")
        
        if activated.lower() == 'y':
            print("✅ Multiple clicks work! Testing typing...")
            self.test_typing()
            self.return_to_base()
            worked = input("Did typing work with multiple clicks? (y/n): ")
            if worked.lower() == 'y':
                return "multiple_clicks"
        
        self.return_to_base()
        
        # Method 5: Tab to focus
        print(f"\n--- Method 5: Tab Key Focus ---")
        self.switch_to_grok_desktop()
        
        pyautogui.click(x, y)  # Click first
        time.sleep(0.5)
        pyautogui.press('tab')  # Then tab to focus
        time.sleep(1)
        
        activated = input(f"Method 5: Did Tab key activate the input box? (y/n): ")
        
        if activated.lower() == 'y':
            print("✅ Tab focus works! Testing typing...")
            self.test_typing()
            self.return_to_base()
            worked = input("Did typing work with Tab focus? (y/n): ")
            if worked.lower() == 'y':
                return "click_tab"
        
        self.return_to_base()
        
        print("❌ No activation method worked")
        return None
    
    def test_typing(self):
        """Test typing once box is activated"""
        print("Testing typing with AppleScript...")
        test_message = "Grok activation test - dynamic input box"
        self.type_with_applescript(test_message)
        time.sleep(0.5)
        
        print("Testing Enter key...")
        pyautogui.press("enter")
        time.sleep(1)
    
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
    
    def manual_activation_test(self):
        """Manual test - you activate the box"""
        
        print("\n🖱️ MANUAL ACTIVATION TEST")
        print("You'll manually activate Grok's input box")
        
        self.switch_to_grok_desktop()
        
        print("\nInstructions:")
        print("1. Look at Grok's interface")
        print("2. Manually click the input box to activate it")
        print("3. Watch it double in size")
        print("4. Come back to Terminal without typing anything")
        
        input("Manually activate Grok's input box, then press Enter...")
        
        print("Now testing if our script can type into the manually activated box...")
        
        # Test typing into the manually activated box
        self.test_typing()
        
        self.return_to_base()
        
        worked = input("Did the script type into the manually activated box? (y/n): ")
        
        if worked.lower() == 'y':
            print("✅ Script can type once box is manually activated")
            print("Problem is activation, not typing!")
        else:
            print("❌ Even manual activation doesn't help")
    
    def coordinate_refinement_test(self):
        """Test coordinates within the expanded box area"""
        
        print("\n📐 COORDINATE REFINEMENT TEST")
        print("Testing coordinates after box doubles in size")
        
        # If box doubles vertically, test coordinates in the expanded area
        base_x = 1548
        
        # Test Y coordinates assuming box expands downward
        expanded_y_coords = [
            990,   # Original area
            1000,  # Slightly down
            1010,  # Further down (expanded area)
            1020,  # Lower expanded area
            1030,  # Bottom of expanded area
        ]
        
        for y in expanded_y_coords:
            print(f"\nTesting expanded box coordinate: ({base_x}, {y})")
            
            self.switch_to_grok_desktop()
            
            # First, manually activate the box
            print("Please manually click Grok's input box to activate it...")
            input("Box activated? Press Enter...")
            
            # Now test this coordinate
            pyautogui.moveTo(base_x, y, duration=1)
            time.sleep(0.5)
            pyautogui.click(base_x, y)
            time.sleep(0.5)
            
            self.test_typing()
            
            self.return_to_base()
            
            worked = input(f"Did coordinate ({base_x}, {y}) work in expanded box? (y/n): ")
            if worked.lower() == 'y':
                print(f"✅ Found working expanded box coordinate: ({base_x}, {y})")
                return (base_x, y)
        
        return None

def main():
    """Test Grok activation methods"""
    
    grok = GrokActivationFix()
    
    print("\n🎯 GROK ACTIVATION TESTING")
    print("Solving the dynamic input box activation problem")
    
    choice = input(f"\nChoose test method:\n1. Test activation methods\n2. Manual activation test\n3. Coordinate refinement test\nChoice: ")
    
    if choice == "1":
        working_method = grok.test_activation_methods()
        if working_method:
            print(f"\n✅ WORKING METHOD: {working_method}")
        else:
            print("\n❌ No activation method worked")
    
    elif choice == "2":
        grok.manual_activation_test()
    
    elif choice == "3":
        working_coords = grok.coordinate_refinement_test()
        if working_coords:
            print(f"\n✅ WORKING EXPANDED COORDINATES: {working_coords}")
    
    print("\nGrok activation testing complete!")

if __name__ == "__main__":
    main()