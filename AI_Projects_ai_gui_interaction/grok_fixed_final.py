#!/usr/bin/env python3
"""
Grok Fixed Final Version
Fix desktop switching and typing issues
"""

import pyautogui
import subprocess
import time

class GrokFixedFinal:
    """Final working Grok system"""
    
    def __init__(self):
        print("Grok Fixed Final System")
        
        self.grok_coords = (1548, 1000)
        self.current_desktop = 0
        
    def switch_to_grok_desktop(self):
        """Reliable desktop switching to Desktop 2"""
        print("🧭 Switching to Desktop 2 (Grok)...")
        
        # From Desktop 0 to Desktop 2 requires 2 right moves
        if self.current_desktop == 0:
            print("Moving Desktop 0 -> 1...")
            pyautogui.hotkey("ctrl", "right")
            time.sleep(1.5)  # Extra time for desktop switch
            
            print("Moving Desktop 1 -> 2...")
            pyautogui.hotkey("ctrl", "right")
            time.sleep(1.5)  # Extra time for desktop switch
            
            self.current_desktop = 2
            print("✅ Now on Desktop 2")
        
        elif self.current_desktop == 1:
            print("Moving Desktop 1 -> 2...")
            pyautogui.hotkey("ctrl", "right")
            time.sleep(1.5)
            self.current_desktop = 2
            print("✅ Now on Desktop 2")
        
        elif self.current_desktop == 2:
            print("✅ Already on Desktop 2")
        
        # Extra pause to ensure desktop switch is complete
        time.sleep(1)
    
    def return_to_base(self):
        """Return to Desktop 0"""
        print("🏠 Returning to Desktop 0...")
        
        if self.current_desktop == 2:
            print("Moving Desktop 2 -> 1...")
            pyautogui.hotkey("ctrl", "left")
            time.sleep(1.5)
            
            print("Moving Desktop 1 -> 0...")
            pyautogui.hotkey("ctrl", "left")
            time.sleep(1.5)
            
            self.current_desktop = 0
            print("✅ Back on Desktop 0")
        
        elif self.current_desktop == 1:
            print("Moving Desktop 1 -> 0...")
            pyautogui.hotkey("ctrl", "left")
            time.sleep(1.5)
            self.current_desktop = 0
            print("✅ Back on Desktop 0")
    
    def activate_grok_input(self):
        """Activate Grok's input box"""
        print("🎯 Activating Grok input box...")
        
        x, y = self.grok_coords
        
        # Move mouse to coordinates
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        
        # Click to activate
        pyautogui.click(x, y)
        time.sleep(1.5)  # Wait for activation and doubling
        
        print("✅ Grok input should be activated")
    
    def test_grok_typing_methods(self):
        """Test different typing methods for Grok"""
        
        print("\n🔤 TESTING GROK TYPING METHODS")
        
        # Go to Grok first
        self.switch_to_grok_desktop()
        self.activate_grok_input()
        
        # Confirm activation manually
        activated = input("Is Grok's input box activated and doubled in size? (y/n): ")
        
        if activated.lower() != 'y':
            print("❌ Grok input not activated - check coordinates")
            self.return_to_base()
            return None
        
        # Test Method 1: Basic pyautogui.typewrite
        print("\n--- Method 1: Basic pyautogui.typewrite ---")
        test_text1 = "Method 1 test"
        
        try:
            pyautogui.typewrite(test_text1)
            time.sleep(1)
            
            method1_worked = input(f"Did '{test_text1}' appear in Grok? (y/n): ")
            
            if method1_worked.lower() == 'y':
                print("✅ Method 1 works!")
                self.return_to_base()
                return "basic_typewrite"
        except Exception as e:
            print(f"❌ Method 1 error: {e}")
        
        # Clear field for next test
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        pyautogui.press("delete")
        time.sleep(0.5)
        
        # Test Method 2: Slow typing
        print("\n--- Method 2: Slow character typing ---")
        test_text2 = "Method 2"
        
        try:
            for char in test_text2:
                if char == ' ':
                    pyautogui.press('space')
                else:
                    pyautogui.typewrite(char)
                time.sleep(0.1)  # Small delay between characters
            
            time.sleep(1)
            method2_worked = input(f"Did '{test_text2}' appear in Grok? (y/n): ")
            
            if method2_worked.lower() == 'y':
                print("✅ Method 2 works!")
                self.return_to_base()
                return "slow_typing"
        except Exception as e:
            print(f"❌ Method 2 error: {e}")
        
        # Clear field for next test
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        pyautogui.press("delete")
        time.sleep(0.5)
        
        # Test Method 3: Clipboard paste
        print("\n--- Method 3: Clipboard paste ---")
        test_text3 = "Method 3 clipboard test"
        
        try:
            # Copy to clipboard
            subprocess.run(['pbcopy'], input=test_text3.encode())
            time.sleep(0.3)
            
            # Paste
            pyautogui.hotkey("command", "v")
            time.sleep(1)
            
            method3_worked = input(f"Did '{test_text3}' appear in Grok? (y/n): ")
            
            if method3_worked.lower() == 'y':
                print("✅ Method 3 works!")
                self.return_to_base()
                return "clipboard_paste"
        except Exception as e:
            print(f"❌ Method 3 error: {e}")
        
        print("❌ No typing method worked")
        self.return_to_base()
        return None
    
    def test_complete_grok_workflow(self, typing_method):
        """Test complete Grok workflow with working typing method"""
        
        print(f"\n🎯 TESTING COMPLETE GROK WORKFLOW")
        print(f"Using typing method: {typing_method}")
        
        test_message = "Complete workflow test for Grok integration"
        
        print(f"Test message: {test_message}")
        print("Starting complete workflow in 3 seconds...")
        time.sleep(3)
        
        # Step 1: Navigate to Grok
        self.switch_to_grok_desktop()
        
        # Step 2: Activate input
        self.activate_grok_input()
        
        # Step 3: Type using working method
        print(f"Typing with method: {typing_method}")
        
        if typing_method == "basic_typewrite":
            pyautogui.typewrite(test_message)
            
        elif typing_method == "slow_typing":
            for char in test_message:
                if char == ' ':
                    pyautogui.press('space')
                else:
                    pyautogui.typewrite(char)
                time.sleep(0.05)
                
        elif typing_method == "clipboard_paste":
            subprocess.run(['pbcopy'], input=test_message.encode())
            time.sleep(0.3)
            pyautogui.hotkey("command", "v")
        
        time.sleep(1)
        
        # Step 4: Send message
        print("Sending message...")
        pyautogui.press("enter")
        time.sleep(2)
        
        # Step 5: Return to base
        self.return_to_base()
        
        # Step 6: Verify success
        success = input("Did Grok receive and process the complete message? (y/n): ")
        
        if success.lower() == 'y':
            print("🎉 COMPLETE GROK WORKFLOW SUCCESS!")
            print(f"Working method: {typing_method}")
            return True
        else:
            print("❌ Workflow failed")
            return False
    
    def debug_desktop_switching(self):
        """Debug desktop switching specifically"""
        
        print("\n🧭 DEBUGGING DESKTOP SWITCHING")
        
        print(f"Current desktop: {self.current_desktop}")
        
        input("Press Enter to switch to Desktop 2...")
        self.switch_to_grok_desktop()
        
        on_grok_desktop = input("Are you now on Desktop 2 with Grok visible? (y/n): ")
        
        if on_grok_desktop.lower() == 'y':
            print("✅ Desktop switching works!")
            
            input("Press Enter to return to Desktop 0...")
            self.return_to_base()
            
            back_home = input("Are you back on Desktop 0? (y/n): ")
            if back_home.lower() == 'y':
                print("✅ Desktop switching both ways works!")
                return True
        
        print("❌ Desktop switching issues")
        return False

def main():
    """Test fixed Grok system"""
    
    grok = GrokFixedFinal()
    
    print("\n🎯 GROK FIXED FINAL SYSTEM")
    print("Fixed desktop switching + reliable typing")
    
    choice = input(f"\nChoose test:\n1. Debug desktop switching\n2. Test typing methods\n3. Complete workflow test\nChoice: ")
    
    if choice == "1":
        grok.debug_desktop_switching()
    
    elif choice == "2":
        working_method = grok.test_grok_typing_methods()
        if working_method:
            print(f"\n✅ WORKING METHOD FOUND: {working_method}")
            
            test_complete = input("Test complete workflow with this method? (y/n): ")
            if test_complete.lower() == 'y':
                grok.test_complete_grok_workflow(working_method)
        else:
            print("\n❌ No working typing method found")
    
    elif choice == "3":
        method = input("Which typing method to use?\n1. basic_typewrite\n2. slow_typing\n3. clipboard_paste\nChoice: ")
        
        method_map = {
            "1": "basic_typewrite",
            "2": "slow_typing", 
            "3": "clipboard_paste"
        }
        
        typing_method = method_map.get(method, "basic_typewrite")
        grok.test_complete_grok_workflow(typing_method)
    
    print("\nGrok fixed final testing complete!")

if __name__ == "__main__":
    main()