#!/usr/bin/env python3
"""
AI Council Circular Loop – APPLESCRIPT VERSION (FIXED)
Based on your proven working scripts
Kai → Claude → Perplexity → Grok → Kai ...
"""

import time
import pyautogui
import pytesseract
import subprocess
import pyperclip

# Define each AI and its settings with desktop locations - from your working script
AI_ORDER = [
    {"name": "kai", "desktop": 1, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "claude", "desktop": 1, "coords": (1200, 960), "read_region": (900, 150, 1400, 600), "typing_method": "applescript"},
    {"name": "perplexity", "desktop": 2, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "grok", "desktop": 2, "coords": (1548, 1000), "read_region": (1200, 150, 1800, 600), "typing_method": "clipboard"},
]

WAIT_SECONDS = 8
MAX_RETRIES = 3

class CircularCouncil:
    def __init__(self):
        self.log = []
        self.last_message = "Hello, this is the AI Council. Please begin the discussion."
        self.current_desktop = 0

    def switch_to_desktop(self, target_desktop):
        """Switch desktop using pyautogui hotkeys (from your working script)"""
        if target_desktop == self.current_desktop:
            return True
        
        print(f"🖥️ Switching from desktop {self.current_desktop} to {target_desktop}")
        
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

    def click_to_focus(self, x, y):
        """Your proven click-to-focus method"""
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(0.8)

    def type_with_applescript(self, text):
        """Your proven AppleScript typing"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)

    def paste_with_applescript(self, text):
        """Your proven clipboard solution for Grok"""
        pyperclip.copy(text)
        time.sleep(0.3)
        
        script = '''
        tell application "System Events"
            keystroke "v" using {command down}
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)

    def send_message(self, ai, message):
        print(f"📨 Sending to {ai['name']} on desktop {ai['desktop']}: {message[:100]}...")
        
        # Switch to correct desktop
        self.switch_to_desktop(ai['desktop'])
        
        # Click to focus using your proven method
        self.click_to_focus(ai["coords"][0], ai["coords"][1])
        
        # Clear field using your proven method
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        
        # Type message using appropriate method from your working script
        if ai["typing_method"] == "applescript":
            self.type_with_applescript(message)
        elif ai["typing_method"] == "clipboard":
            self.paste_with_applescript(message)
        
        # Send message using your proven method
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(WAIT_SECONDS)

    def wait_for_response(self, ai):
        print(f"🕵️ Waiting for {ai['name']}'s reply on desktop {ai['desktop']}...")
        last_text = ""
        
        # Ensure we're on the right desktop
        self.switch_to_desktop(ai['desktop'])
        
        for attempt in range(MAX_RETRIES):
            # Scroll if needed for long responses (from your working script)
            if ai['name'] in ["perplexity"]:
                print(f"📜 Scrolling for {ai['name']} response area...")
                scroll_coords = (ai["coords"][0], ai["coords"][1] - 200)
                pyautogui.moveTo(scroll_coords[0], scroll_coords[1])
                pyautogui.scroll(-5)
                time.sleep(1)
            
            try:
                screenshot = pyautogui.screenshot(region=ai["read_region"])
                text = pytesseract.image_to_string(screenshot).strip()
                
                if text and text != last_text and len(text) > 20:
                    print(f"📜 {ai['name']} said:\n{text[:300]}...")
                    return text
                
                time.sleep(3)
                last_text = text
            except Exception as e:
                print(f"⚠️ OCR error: {e}")
                time.sleep(3)
                continue
            
        print(f"⚠️ No clear reply from {ai['name']}")
        return None

    def loop_once(self):
        print(f"\n🔄 Starting new circular loop...")
        for i in range(len(AI_ORDER)):
            ai = AI_ORDER[i]
            print(f"\n📍 Step {i+1}/{len(AI_ORDER)}: {ai['name'].upper()}")
            
            self.send_message(ai, self.last_message)
            response = self.wait_for_response(ai)
            
            if response:
                # Truncate very long responses
                self.last_message = response[:1000] if len(response) > 1000 else response
                self.log.append({
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": response,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                self.last_message = "(No clear reply)"
                self.log.append({
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": None,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Return to desktop 0 after loop
        self.switch_to_desktop(0)
        print(f"\n✅ Loop complete, returned to desktop 0")

    def save_log(self):
        """Save conversation log to file"""
        import json
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_circular_log_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.log, f, indent=2)
        
        print(f"💾 Log saved: {filename}")
        return filename

def main():
    council = CircularCouncil()
    try:
        while True:
            council.loop_once()
            print("🔄 Council loop complete. Restarting in 10 seconds...\n")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Stopping circular council...")
        council.save_log()
        print("👋 Session ended!")

if __name__ == "__main__":
    main()