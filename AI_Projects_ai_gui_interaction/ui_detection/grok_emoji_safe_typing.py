#!/usr/bin/env python3
"""
Grok Emoji-Safe Typing
pyautogui typing that avoids emoji popup triggers
"""

import pyautogui
import subprocess
import time

class GrokEmojiSafeTyping:
    """Type into Grok without triggering emoji popup"""
    
    def __init__(self):
        print("Grok Emoji-Safe Typing System")
        print("pyautogui typing + emoji popup prevention")
        
        self.grok_coords = (1548, 1000)
        
    def switch_to_grok_desktop(self):
        """Navigate to Desktop 2"""
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "right")
        time.sleep(1.5)
    
    def activate_grok_input(self):
        """Activate Grok's input box"""
        x, y = self.grok_coords
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(1)  # Wait for activation and doubling
        print("✅ Grok input activated")
    
    def safe_type_for_grok(self, text: str):
        """Type into Grok safely without emoji popup"""
        
        # Method 1: Ultra-clean text first
        clean_text = self.ultra_clean_text(text)
        print(f"Cleaned text: '{clean_text}'")
        
        try:
            # Method A: Very slow typing to avoid emoji triggers
            print("Using very slow pyautogui typing...")
            
            for char in clean_text:
                # Type each character individually with delay
                if char == ' ':
                    pyautogui.press('space')
                elif char.isalnum() or char in '.,!?':  # Only safe characters
                    pyautogui.typewrite(char)
                time.sleep(0.2)  # Long delay between characters
            
            print("✅ Safe typing complete")
            return True
            
        except Exception as e:
            print(f"❌ Safe typing failed: {e}")
            return False
    
    def clipboard_type_for_grok(self, text: str):
        """Alternative: Use clipboard to avoid typing altogether"""
        
        clean_text = self.ultra_clean_text(text)
        print(f"Using clipboard method for: '{clean_text}'")
        
        try:
            # Copy to clipboard
            subprocess.run(['pbcopy'], input=clean_text.encode())
            time.sleep(0.3)
            
            # Paste into Grok
            pyautogui.hotkey("command", "v")
            time.sleep(0.5)
            
            print("✅ Clipboard typing complete")
            return True
            
        except Exception as e:
            print(f"❌ Clipboard typing failed: {e}")
            return False
    
    def ultra_clean_text(self, text: str):
        """Ultra-aggressive text cleaning to prevent emoji popup"""
        
        # Remove ALL special characters that might trigger emoji
        safe_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?')
        
        clean = ""
        for char in text:
            if char in safe_chars:
                clean += char
            else:
                clean += " "  # Replace problem chars with space
        
        # Remove multiple spaces
        while "  " in clean:
            clean = clean.replace("  ", " ")
        
        # Limit length
        clean = clean[:300].strip()
        
        return clean
    
    def test_grok_complete_workflow(self):
        """Test complete Grok workflow: activate + type + send"""
        
        print("\n🎯 TESTING COMPLETE GROK WORKFLOW")
        
        test_message = "Hello Grok, this is a test message from the AI Council system using safe typing methods"
        
        print(f"Test message: {test_message}")
        
        # Step 1: Navigate and activate
        print("\nStep 1: Navigate to Grok and activate input...")
        self.switch_to_grok_desktop()
        self.activate_grok_input()
        
        input("Is Grok input activated and doubled? Press Enter...")
        
        # Step 2: Test safe typing
        print("\nStep 2: Testing safe typing method...")
        
        typing_method = input("Choose typing method:\n1. Safe character-by-character\n2. Clipboard paste\nChoice: ")
        
        if typing_method == "1":
            success = self.safe_type_for_grok(test_message)
        else:
            success = self.clipboard_type_for_grok(test_message)
        
        if not success:
            print("❌ Typing failed")
            return False
        
        # Step 3: Send the message
        print("\nStep 3: Sending message...")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)
        
        # Step 4: Return and verify
        self.return_to_base()
        
        worked = input("Did Grok receive and process the complete message? (y/n): ")
        
        if worked.lower() == 'y':
            print("🎉 COMPLETE GROK WORKFLOW SUCCESS!")
            return True
        else:
            print("❌ Workflow failed")
            return False
    
    def return_to_base(self):
        """Return to Desktop 0"""
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "left")
        time.sleep(1)
    
    def disable_emoji_popup_settings(self):
        """Instructions to disable emoji popup system-wide"""
        
        print("\n🚫 EMOJI POPUP PREVENTION")
        print("To permanently disable emoji popup:")
        print()
        print("1. System Preferences > Keyboard")
        print("2. Uncheck 'Show emoji & symbols in touch bar'")
        print("3. In 'Touch Bar shows' dropdown, select 'Expanded Control Strip'")
        print("4. Keyboard Shortcuts > Input Sources")
        print("5. Uncheck 'Select next source in Input menu'")
        print("6. Or change the shortcut away from Ctrl+Space/Cmd+Space")
        print()
        print("This should prevent accidental emoji popup triggers!")

def main():
    """Test emoji-safe Grok typing"""
    
    grok = GrokEmojiSafeTyping()
    
    print("\n🎯 GROK EMOJI-SAFE TYPING SYSTEM")
    print("Type into Grok without triggering emoji popup")
    
    choice = input(f"\nChoose test:\n1. Test complete Grok workflow\n2. Show emoji popup prevention tips\nChoice: ")
    
    if choice == "1":
        success = grok.test_grok_complete_workflow()
        if success:
            print("\n✅ GROK IS NOW FULLY WORKING!")
            print("Ready to add Grok to the AI Council system!")
        else:
            print("\n🔧 Still needs refinement")
    
    elif choice == "2":
        grok.disable_emoji_popup_settings()
    
    print("\nGrok emoji-safe typing test complete!")

if __name__ == "__main__":
    main()