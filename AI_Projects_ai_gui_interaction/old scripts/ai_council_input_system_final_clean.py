#!/usr/bin/env python3
"""
AI Council Input System – Final Version with OCR Watch, Scroll, and Safe Logging
FIXED VERSION - Syntax errors corrected
"""

import time
import pyautogui
import pytesseract
import subprocess
import pyperclip

class AICouncilInputSystem:
    def __init__(self):
        self.session_log = []
        self.current_desktop = 0
        
        # Jon's proven AI layout
        self.ai_council = {
            "kai": {
                "desktop": 1,
                "input_coords": (456, 960),
                "typing_method": "applescript"
            },
            "claude": {
                "desktop": 1,
                "input_coords": (1200, 960),
                "typing_method": "applescript"
            },
            "perplexity": {
                "desktop": 2,
                "input_coords": (456, 960),
                "typing_method": "applescript"
            },
            "grok": {
                "desktop": 2,
                "input_coords": (1548, 1000),
                "typing_method": "clipboard"
            }
        }

    def switch_to_desktop(self, target_desktop):
        """Switch desktop using proven method"""
        if target_desktop == self.current_desktop:
            return True
        
        if target_desktop > self.current_desktop:
            moves = target_desktop - self.current_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "right")
                time.sleep(1.5)
        else:
            moves = self.current_desktop - target_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "left")
                time.sleep(1.5)
        
        self.current_desktop = target_desktop
        time.sleep(1)
        return True

    def type_with_applescript(self, text):
        """Kai's proven AppleScript typing"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)

    def paste_with_applescript(self, text):
        """Kai's clipboard solution for Grok"""
        pyperclip.copy(text)
        time.sleep(0.3)
        
        script = '''
        tell application "System Events"
            keystroke "v" using {command down}
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)

    def send_message_to_ai(self, ai_name, message):
        """Send message with OCR response watching"""
        
        if ai_name not in self.ai_council:
            print(f"❌ Unknown AI: {ai_name}")
            return False
        
        ai = self.ai_council[ai_name]
        
        # Pre-log session entry
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "ai": ai_name,
            "message": message[:200],  # Truncate for logging
            "method": ai["typing_method"],
            "coordinates": ai["input_coords"],
            "desktop": ai["desktop"],
            "status": "sent",
            "ocr_response": None
        }
        self.session_log.append(log_entry)

        print(f"📤 Sending to {ai_name}")
        print(f"   Desktop: {ai['desktop']}")
        print(f"   Method: {ai['typing_method']}")
        print(f"   Message: {message[:100]}...")

        # Switch to AI's desktop
        self.switch_to_desktop(ai["desktop"])

        # Click to focus
        coords = ai["input_coords"]
        pyautogui.moveTo(coords[0], coords[1], duration=1)
        time.sleep(0.5)
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.8)

        # Clear and type message
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        
        if ai["typing_method"] == "applescript":
            self.type_with_applescript(message)
        elif ai["typing_method"] == "clipboard":
            self.paste_with_applescript(message)

        # Send message
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1.5)

        # Add scroll step for verbose AIs
        if ai_name in ["perplexity"]:
            print(f"📜 Scrolling for {ai_name} response area...")
            scroll_coords = (coords[0], coords[1] - 200)
            pyautogui.moveTo(scroll_coords[0], scroll_coords[1])
            pyautogui.scroll(-5)  # Scroll down to see response
            time.sleep(1)

        # OCR Response watching
        print("⏳ Watching for OCR-detectable response...")
        last_text = ""
        
        # Define OCR region (adjust these coordinates as needed)
        ocr_region = (462, 171, 638, 551)
        
        for attempt in range(30):  # 30 second timeout
            try:
                screenshot = pyautogui.screenshot(region=ocr_region)
                text = pytesseract.image_to_string(screenshot).strip()
                
                if text and text != last_text and len(text) > 20:
                    print(f"📜 OCR Detected new content:")
                    print(f"{text[:200]}...")  # FIXED: Proper f-string formatting
                    
                    self.session_log[-1]["ocr_response"] = text
                    print(f"✅ Response captured from {ai_name}")
                    return text
                
                last_text = text
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ OCR error: {e}")
                continue
        
        print("⏰ OCR timeout: No new response detected.")
        self.session_log[-1]["ocr_response"] = "No response within time window."
        return None

    def test_single_ai_with_ocr(self, ai_name):
        """Test single AI with OCR response capture"""
        
        test_message = f"OCR test for {ai_name}: Please respond with a few sentences so we can test the OCR response capture system."
        
        print(f"\n🧪 TESTING {ai_name.upper()} WITH OCR")
        
        response = self.send_message_to_ai(ai_name, test_message)
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        
        if response:
            print(f"\n✅ OCR SUCCESS for {ai_name}!")
            print(f"Captured: {response[:300]}...")
            return True
        else:
            print(f"\n❌ OCR failed for {ai_name}")
            return False

    def save_session_log(self):
        """Save session log to file"""
        import json
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_ocr_session_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        
        print(f"💾 Session saved: {filename}")
        return filename

def main():
    """Main function with testing options"""
    
    system = AICouncilInputSystem()
    
    print("\n🎭 AI COUNCIL OCR SYSTEM - FIXED")
    print("Send messages + OCR response capture")
    
    while True:
        print(f"\n" + "="*50)
        print("CHOOSE ACTION:")
        print("1. Test single AI with OCR")
        print("2. Save session log")
        print("3. Exit")
        
        choice = input("Choice (1-3): ")
        
        if choice == "1":
            ai_name = input("Which AI (kai/claude/perplexity/grok): ").lower()
            if ai_name in system.ai_council:
                system.test_single_ai_with_ocr(ai_name)
            else:
                print("❌ Invalid AI name")
                
        elif choice == "2":
            system.save_session_log()
            
        elif choice == "3":
            system.save_session_log()
            print("👋 OCR session complete!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()