#!/usr/bin/env python3
"""
Debug System - Test Grok and Response Capture Issues
"""

import pyautogui
import subprocess
import time

class DebugSystem:
    """Debug the remaining issues step by step"""
    
    def __init__(self):
        self.ai_targets = {
            "kai": {"desktop": 1, "input_coords": (456, 960)},
            "claude": {"desktop": 1, "input_coords": (1200, 960)},
            "perplexity": {"desktop": 2, "input_coords": (456, 960)},
            "grok": {"desktop": 2, "input_coords": (1548, 988)}  # Jon's exact coords
        }
        self.current_desktop = 0
        
        print("DEBUG SYSTEM - Isolate and fix remaining issues")
    
    def switch_desktop(self, target: int):
        """Desktop switching"""
        if target == self.current_desktop:
            return
        
        print(f"Desktop {self.current_desktop} -> {target}")
        if target > self.current_desktop:
            for _ in range(target - self.current_desktop):
                pyautogui.hotkey("ctrl", "right")
                time.sleep(1)
        else:
            for _ in range(self.current_desktop - target):
                pyautogui.hotkey("ctrl", "left")
                time.sleep(1)
        
        self.current_desktop = target
        time.sleep(1.5)
    
    def click_to_focus(self, x: int, y: int):
        """Kai's click method"""
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)
    
    def type_with_applescript(self, text: str):
        """Kai's typing method"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    def debug_grok_targeting(self):
        """Debug why Grok isn't receiving messages"""
        
        print("\n🔍 DEBUGGING GROK TARGETING")
        print(f"Grok coordinates: {self.ai_targets['grok']['input_coords']}")
        
        # Step 1: Test desktop switching to Grok
        print("\nStep 1: Testing desktop switch to Grok (Desktop 2)")
        input("Press Enter to switch to Desktop 2...")
        
        self.switch_desktop(2)
        print("✅ On Desktop 2")
        
        # Step 2: Test mouse movement to Grok coordinates
        print(f"\nStep 2: Moving mouse to Grok coordinates")
        x, y = self.ai_targets['grok']['input_coords']
        print(f"Moving to ({x}, {y})")
        
        pyautogui.moveTo(x, y, duration=2)  # Slow movement so you can see
        print("✅ Mouse moved to Grok coordinates")
        
        input("Is the mouse over Grok's input field? Press Enter...")
        
        # Step 3: Test clicking
        print("\nStep 3: Testing click at Grok coordinates")
        pyautogui.click(x, y)
        time.sleep(1)
        print("✅ Clicked at Grok coordinates")
        
        input("Did Grok's input field get focus (cursor appear)? Press Enter...")
        
        # Step 4: Test typing
        print("\nStep 4: Testing typing with AppleScript")
        test_message = "Debug test for Grok targeting"
        self.type_with_applescript(test_message)
        print("✅ Typed test message")
        
        input("Did the text appear in Grok's input field? Press Enter...")
        
        # Step 5: Test sending
        print("\nStep 5: Testing Enter key")
        pyautogui.press("enter")
        print("✅ Pressed Enter")
        
        # Return to Desktop 0
        self.switch_desktop(0)
        
        worked = input("Did Grok receive and process the message? (y/n): ")
        return worked.lower() == 'y'
    
    def debug_response_capture(self):
        """Debug why response capture isn't working"""
        
        print("\n🔍 DEBUGGING RESPONSE CAPTURE")
        print("Testing different response capture methods")
        
        # Test with Kai first (known to work for sending)
        ai_name = "kai"
        target = self.ai_targets[ai_name]
        
        print(f"\nTesting response capture with {ai_name}")
        print("First, send a message and wait for response...")
        
        # Send a message that should get a short response
        self.switch_desktop(target['desktop'])
        x, y = target['input_coords']
        self.click_to_focus(x, y)
        
        pyautogui.hotkey("command", "a")
        time.sleep(0.3)
        
        test_question = "Please respond with just the word HELLO"
        self.type_with_applescript(test_question)
        time.sleep(0.5)
        pyautogui.press("enter")
        
        print("Message sent. Waiting for response...")
        time.sleep(10)
        
        # Now test different capture methods
        print("\nTesting capture methods...")
        
        # Method 1: Triple-click to select paragraph
        print("\nMethod 1: Triple-click")
        response_y = y - 200  # Above input area
        pyautogui.click(x, response_y, clicks=3, interval=0.2)
        time.sleep(0.5)
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        try:
            content1 = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"Triple-click captured: '{content1[:100]}...'")
        except:
            content1 = "FAILED"
        
        # Method 2: Select all in response area
        print("\nMethod 2: Click and Select All")
        pyautogui.click(x, response_y)
        time.sleep(0.5)
        pyautogui.hotkey("command", "a")
        time.sleep(0.5)
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        try:
            content2 = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"Select all captured: '{content2[:100]}...'")
        except:
            content2 = "FAILED"
        
        # Method 3: Drag selection
        print("\nMethod 3: Drag Selection")
        start_y = response_y - 50
        end_y = response_y + 50
        
        pyautogui.moveTo(x, start_y)
        pyautogui.dragTo(x, end_y, duration=1, button='left')
        time.sleep(0.5)
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        try:
            content3 = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"Drag selection captured: '{content3[:100]}...'")
        except:
            content3 = "FAILED"
        
        # Return to Desktop 0
        self.switch_desktop(0)
        
        print("\n📊 CAPTURE METHOD RESULTS:")
        print(f"1. Triple-click: {len(content1)} chars")
        print(f"2. Select all: {len(content2)} chars") 
        print(f"3. Drag selection: {len(content3)} chars")
        
        best_method = input("\nWhich method captured the AI's response best? (1/2/3): ")
        return best_method
    
    def test_alternative_grok_coords(self):
        """Test coordinates around the Grok area"""
        
        print("\n🎯 TESTING ALTERNATIVE GROK COORDINATES")
        print("Testing coordinates around your provided area")
        
        # Your area: (1255,970) to (1841, 1006)
        # Center: (1548, 988) - not working
        # Let's try other points in that rectangle
        
        candidates = [
            (1255, 970),  # Top-left of your area
            (1548, 970),  # Top-center
            (1841, 970),  # Top-right
            (1255, 988),  # Left-center
            (1841, 988),  # Right-center
            (1255, 1006), # Bottom-left
            (1548, 1006), # Bottom-center
            (1841, 1006), # Bottom-right
        ]
        
        print("Will test 8 different points in your Grok input area")
        
        for i, (x, y) in enumerate(candidates):
            print(f"\n--- Testing point {i+1}: ({x}, {y}) ---")
            
            self.switch_desktop(2)  # Grok's desktop
            
            # Move mouse to show the point
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(1)
            
            test_point = input(f"Point {i+1}: ({x}, {y}) - Test this point? (y/n): ")
            if test_point.lower() != 'y':
                continue
            
            # Test clicking and typing
            pyautogui.click(x, y)
            time.sleep(0.5)
            
            self.type_with_applescript(f"Test point {i+1}")
            time.sleep(0.5)
            
            worked = input(f"Did point {i+1} work for Grok? (y/n): ")
            if worked.lower() == 'y':
                print(f"✅ FOUND WORKING GROK COORDINATES: ({x}, {y})")
                return (x, y)
        
        print("❌ No working coordinates found in the area")
        return None

def main():
    """Debug main function"""
    
    debug = DebugSystem()
    
    print("\nDEBUG SYSTEM - Fix Remaining Issues")
    print("1. Debug Grok targeting")
    print("2. Debug response capture") 
    print("3. Test alternative Grok coordinates")
    
    choice = input("Choose debug task (1-3): ")
    
    if choice == "1":
        success = debug.debug_grok_targeting()
        if success:
            print("✅ Grok targeting working!")
        else:
            print("❌ Grok targeting still has issues")
    
    elif choice == "2":
        best_method = debug.debug_response_capture()
        print(f"Best capture method: {best_method}")
    
    elif choice == "3":
        working_coords = debug.test_alternative_grok_coords()
        if working_coords:
            print(f"Use these Grok coordinates: {working_coords}")
    
    print("\nDebug session complete")

if __name__ == "__main__":
    main()