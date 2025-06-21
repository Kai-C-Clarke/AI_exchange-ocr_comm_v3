#!/usr/bin/env python3
"""
AI Council Input System – Sequential Broadcast Version
Sends messages to all AIs in sequence: Kai→Claude→Claude→Perplexity→Perplexity→Grok→repeat
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
        
        # Sequential order: Kai→Claude→Claude→Perplexity→Perplexity→Grok→repeat
        self.broadcast_sequence = ["kai", "claude", "claude", "perplexity", "perplexity", "grok"]
        self.current_ai_index = 0

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

    def get_response_region(self, ai_name):
        """Get appropriate OCR region for each AI"""
        regions = {
            "kai": (400, 150, 700, 600),
            "claude": (900, 150, 1400, 600),
            "perplexity": (400, 150, 700, 600),
            "grok": (1200, 150, 1800, 600)
        }
        return regions.get(ai_name, (462, 171, 638, 551))

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
            "ocr_response": None,
            "sequence_position": self.current_ai_index
        }
        self.session_log.append(log_entry)

        print(f"📤 Sending to {ai_name} (#{self.current_ai_index + 1} in sequence)")
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
        
        # Use AI-specific OCR region
        ocr_region = self.get_response_region(ai_name)
        
        for attempt in range(30):  # 30 second timeout
            try:
                screenshot = pyautogui.screenshot(region=ocr_region)
                text = pytesseract.image_to_string(screenshot).strip()
                
                if text and text != last_text and len(text) > 20:
                    print(f"📜 OCR Detected new content:")
                    print(f"{text[:200]}...")
                    
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

    def get_next_ai(self):
        """Get next AI in sequence"""
        ai_name = self.broadcast_sequence[self.current_ai_index]
        self.current_ai_index = (self.current_ai_index + 1) % len(self.broadcast_sequence)
        return ai_name

    def broadcast_to_next_ai(self, message):
        """Send message to next AI in sequence"""
        ai_name = self.get_next_ai()
        print(f"\n🎯 Broadcasting to next AI: {ai_name.upper()}")
        return self.send_message_to_ai(ai_name, message)

    def broadcast_full_cycle(self, message):
        """Send message to all AIs in one complete cycle"""
        print(f"\n🚀 FULL CYCLE BROADCAST")
        print(f"Sequence: {' → '.join(self.broadcast_sequence)}")
        
        responses = {}
        
        for i, ai_name in enumerate(self.broadcast_sequence):
            print(f"\n📍 Step {i+1}/{len(self.broadcast_sequence)}: {ai_name.upper()}")
            response = self.send_message_to_ai(ai_name, message)
            responses[f"{ai_name}_{i+1}"] = response
            
            # Brief pause between AIs
            time.sleep(2)
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        
        print(f"\n✅ Full cycle complete!")
        return responses

    def continuous_broadcast_mode(self):
        """Interactive mode for continuous broadcasting"""
        print(f"\n🔄 CONTINUOUS BROADCAST MODE")
        print(f"Sequence: {' → '.join(self.broadcast_sequence)}")
        print(f"Type 'quit' to exit")
        
        while True:
            message = input(f"\nMessage for next AI ({self.broadcast_sequence[self.current_ai_index]}): ")
            
            if message.lower() == 'quit':
                break
            
            if message.strip():
                self.broadcast_to_next_ai(message)
                
                # Return to Desktop 0 after each message
                self.switch_to_desktop(0)
            
        print("🔄 Continuous mode ended")

    def save_session_log(self):
        """Save session log to file"""
        import json
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_sequential_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        
        print(f"💾 Session saved: {filename}")
        return filename

def main():
    """Main function with sequential broadcasting options"""
    
    system = AICouncilInputSystem()
    
    print("\n🎭 AI COUNCIL SEQUENTIAL BROADCAST SYSTEM")
    print(f"Sequence: {' → '.join(system.broadcast_sequence)}")
    
    while True:
        print(f"\n" + "="*60)
        print("CHOOSE ACTION:")
        print("1. Send to next AI in sequence")
        print("2. Full cycle broadcast (all AIs once)")
        print("3. Continuous broadcast mode")
        print("4. Reset sequence position")
        print("5. Save session log")
        print("6. Exit")
        
        choice = input("Choice (1-6): ")
        
        if choice == "1":
            message = input("Message: ")
            if message.strip():
                system.broadcast_to_next_ai(message)
                system.switch_to_desktop(0)
                
        elif choice == "2":
            message = input("Message for full cycle: ")
            if message.strip():
                system.broadcast_full_cycle(message)
                
        elif choice == "3":
            system.continuous_broadcast_mode()
            
        elif choice == "4":
            system.current_ai_index = 0
            print(f"🔄 Sequence reset to start: {system.broadcast_sequence[0]}")
            
        elif choice == "5":
            system.save_session_log()
            
        elif choice == "6":
            system.save_session_log()
            print("👋 Sequential broadcast session complete!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()