#!/usr/bin/env python3
"""
Grok Typing Fix
Grok activates but doesn't accept AppleScript typing
Try different typing methods
"""

import pyautogui
import subprocess
import time

class GrokTypingFix:
    """Fix Grok's typing input method"""
    
    def __init__(self):
        print("Grok Typing Fix")
        print("Grok activates but doesn't accept AppleScript typing")
        
        self.grok_coords = (1548, 1000)
        
    def switch_to_grok_desktop(self):
        """Navigate to Desktop 2"""
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1.5)
    
    def activate_grok_input(self):
        """Activate Grok's input box (we know this works)"""
        x, y = self.grok_coords
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(1)  # Wait for activation and doubling
        print("✅ Grok input box activated")
    
    def test_typing_methods(self):
        """Test different typing methods for Grok"""
        
        print("\n🎯 TESTING GROK TYPING METHODS")
        print("Trying different ways to type into activated Grok box")
        
        typing_methods = [
            ("pyautogui.typewrite", self.type_with_pyautogui),
            ("pyautogui.write", self.type_with_pyautogui_write),
            ("AppleScript keystroke", self.type_with_applescript),
            ("pyautogui character by character", self.type_char_by_char),
            ("Clipboard + Paste", self.type_with_clipboard),
        ]
        
        for i, (method_name, method_func) in enumerate(typing_methods):
            print(f"\n--- Method {i+1}: {method_name} ---")
            
            self.switch_to_grok_desktop()
            self.activate_grok_input()
            
            test_message = f"Grok test {i+1} using {method_name}"
            print(f"Testing: {test_message}")
            
            try:
                method_func(test_message)
                time.sleep(0.5)
                
                # Test sending
                pyautogui.press("enter")
                time.sleep(1)
                
                # Return for feedback
                self.return_to_base()
                
                worked = input(f"Did method {i+1} ({method_name}) work? (y/n): ")
                
                if worked.lower() == 'y':
                    print(f"🎉 SUCCESS! {method_name} works for Grok!")
                    return method_name, method_func
                else:
                    print(f"❌ {method_name} failed")
                    
            except Exception as e:
                print(f"❌ {method_name} error: {e}")
                self.return_to_base()
        
        print("❌ No typing method worked for Grok")
        return None, None
    
    def type_with_pyautogui(self, text: str):
        """Method 1: Standard pyautogui.typewrite"""
        pyautogui.typewrite(text, interval=0.05)  # Slow typing
    
    def type_with_pyautogui_write(self, text: str):
        """Method 2: pyautogui.write (if different from typewrite)"""
        pyautogui.write(text)
    
    def type_with_applescript(self, text: str):
        """Method 3: AppleScript (we know this fails)"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
    
    def type_char_by_char(self, text: str):
        """Method 4: Character by character with pyautogui"""
        for char in text:
            if char == ' ':
                pyautogui.press('space')
            else:
                pyautogui.typewrite(char)
            time.sleep(0.1)  # Very slow
    
    def type_with_clipboard(self, text: str):
        """Method 5: Copy to clipboard then paste"""
        # Copy text to clipboard
        subprocess.run(['pbcopy'], input=text.encode())
        time.sleep(0.2)
        
        # Paste from clipboard
        pyautogui.hotkey("command", "v")
    
    def return_to_base(self):
        """Return to Desktop 0"""
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
    
    def test_grok_special_chars(self):
        """Test if Grok has issues with special characters"""
        
        print("\n🔤 TESTING GROK SPECIAL CHARACTER HANDLING")
        
        test_texts = [
            "Hello",                    # Simple text
            "Hello World",              # With space
            "Test123",                  # With numbers
            "Hello, World!",            # With punctuation
            "Test-message_here",        # With hyphens/underscores
        ]
        
        self.switch_to_grok_desktop()
        self.activate_grok_input()
        
        for i, test_text in enumerate(test_texts):
            print(f"\nTesting text {i+1}: '{test_text}'")
            
            # Clear field first
            pyautogui.hotkey("command", "a")
            time.sleep(0.2)
            pyautogui.key("delete")
            time.sleep(0.2)
            
            # Try typing
            try:
                pyautogui.typewrite(test_text, interval=0.05)
                time.sleep(0.5)
                
                appeared = input(f"Did '{test_text}' appear in Grok's input? (y/n): ")
                if appeared.lower() == 'y':
                    print(f"✅ '{test_text}' works")
                else:
                    print(f"❌ '{test_text}' failed")
                    
            except Exception as e:
                print(f"❌ Error with '{test_text}': {e}")
        
        self.return_to_base()
    
    def debug_grok_focus(self):
        """Debug if Grok loses focus during typing"""
        
        print("\n🔍 DEBUGGING GROK FOCUS")
        print("Testing if Grok loses focus during typing attempts")
        
        self.switch_to_grok_desktop()
        
        print("Step 1: Activate Grok input...")
        self.activate_grok_input()
        
        input("Is Grok input activated with cursor blinking? Press Enter...")
        
        print("Step 2: Test typing single character...")
        pyautogui.typewrite("H")
        time.sleep(1)
        
        still_focused = input("Did 'H' appear? Is cursor still in Grok input? (y/n): ")
        
        if still_focused.lower() == 'y':
            print("✅ Grok maintains focus - trying longer text...")
            pyautogui.typewrite("ello World")
            time.sleep(1)
            
            full_text = input("Did full 'Hello World' appear? (y/n): ")
            if full_text.lower() == 'y':
                print("✅ pyautogui typing works for Grok!")
            else:
                print("❌ Grok loses focus during longer typing")
        else:
            print("❌ Grok doesn't accept pyautogui typing at all")
        
        self.return_to_base()

def main():
    """Test Grok typing methods"""
    
    grok = GrokTypingFix()
    
    print("\n🎯 GROK TYPING METHOD TESTING")
    print("Find the right way to type into Grok's activated input box")
    
    choice = input(f"\nChoose test:\n1. Test all typing methods\n2. Test special character handling\n3. Debug focus issues\nChoice: ")
    
    if choice == "1":
        working_method, method_func = grok.test_typing_methods()
        if working_method:
            print(f"\n✅ WORKING TYPING METHOD: {working_method}")
        else:
            print("\n❌ No typing method worked")
    
    elif choice == "2":
        grok.test_grok_special_chars()
    
    elif choice == "3":
        grok.debug_grok_focus()
    
    print("\nGrok typing testing complete!")

if __name__ == "__main__":
    main()