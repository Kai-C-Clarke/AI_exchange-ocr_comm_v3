#!/usr/bin/env python3
"""
AI Council Sequential Messaging System - FIXED VERSION
Loop: Kai → Claude → Perplexity → Grok → Kai
Fixed desktop switching + correct coordinates + proven methods
"""

import pyautogui
import subprocess
import time
import json
import pyperclip
from datetime import datetime

class AICouncilLoop:
    def __init__(self):
        self.ai_order = ["kai", "claude", "perplexity", "grok"]
        self.current_desktop = 0
        
        # FIXED: Jon's actual AI layout with correct desktops and coordinates
        self.ai_council = {
            "kai": {
                "desktop": 1,
                "input_coords": (456, 960),     # Jon's proven coordinates
                "response_coords": (456, 500),
                "typing_method": "applescript"   # Proven method
            },
            "claude": {
                "desktop": 1,
                "input_coords": (1200, 960),    # Jon's proven coordinates
                "response_coords": (1200, 500),
                "typing_method": "applescript"   # Proven method
            },
            "perplexity": {
                "desktop": 2,                    # FIXED: Perplexity is on Desktop 2
                "input_coords": (456, 960),     # Jon's proven coordinates
                "response_coords": (456, 500),
                "typing_method": "applescript"   # Proven method
            },
            "grok": {
                "desktop": 2,                    # FIXED: Grok is on Desktop 2
                "input_coords": (1548, 1000),   # Jon's proven coordinates
                "response_coords": (1548, 600),
                "typing_method": "clipboard"     # FIXED: Grok needs clipboard method
            }
        }

    def switch_to_desktop(self, target_desktop):
        """FIXED: Use proven desktop switching method"""
        if target_desktop == self.current_desktop:
            return True
        
        print(f"🧭 Switching Desktop {self.current_desktop} → {target_desktop}")
        
        if target_desktop > self.current_desktop:
            moves = target_desktop - self.current_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "right")  # FIXED: Use Ctrl+Right
                time.sleep(1.5)
        else:
            moves = self.current_desktop - target_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "left")   # FIXED: Use Ctrl+Left
                time.sleep(1.5)
        
        self.current_desktop = target_desktop
        time.sleep(1)
        return True

    def click_and_focus(self, coords):
        """FIXED: Use proven click-to-focus method"""
        pyautogui.moveTo(coords[0], coords[1], duration=1)
        time.sleep(0.5)
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.8)  # Extra time for focus

    def type_with_applescript(self, text):
        """FIXED: Use proven AppleScript typing method"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)

    def paste_with_applescript(self, text):
        """FIXED: Use proven clipboard method for Grok"""
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
        """FIXED: Use proven sending methods for each AI"""
        config = self.ai_council[ai_name]
        
        print(f"\n📤 [{datetime.now().strftime('%H:%M:%S')}] Sending to: {ai_name}")
        print(f"   Desktop: {config['desktop']}")
        print(f"   Coords: {config['input_coords']}")
        print(f"   Method: {config['typing_method']}")
        
        # Switch to AI's desktop
        self.switch_to_desktop(config['desktop'])
        
        # Click to focus
        self.click_and_focus(config['input_coords'])
        
        # Clear existing content
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        
        # Type using AI's proven method
        if config['typing_method'] == 'applescript':
            self.type_with_applescript(message)
        elif config['typing_method'] == 'clipboard':
            self.paste_with_applescript(message)
        
        # Send message
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1.5)
        
        print(f"✅ Message sent to {ai_name}")

    def wait_for_response(self, ai_name, timeout=30):
        """FIXED: Smart waiting with user confirmation"""
        config = self.ai_council[ai_name]
        
        # Return to Desktop 0 for user interaction
        self.switch_to_desktop(0)
        
        print(f"🕒 Waiting for {ai_name} to respond...")
        print(f"   Check {ai_name}'s interface on Desktop {config['desktop']}")
        
        # Simple timeout or user confirmation
        response = input(f"Has {ai_name} finished responding? (y/n): ")
        
        if response.lower() == 'y':
            return True
        else:
            print(f"⏳ Waiting {timeout} seconds for {ai_name}...")
            time.sleep(timeout)
            return True

    def copy_response(self, ai_name):
        """FIXED: Copy response using proven methods"""
        config = self.ai_council[ai_name]
        
        print(f"📋 Copying response from {ai_name}...")
        
        # Switch to AI's desktop
        self.switch_to_desktop(config['desktop'])
        
        # Click in response area
        self.click_and_focus(config['response_coords'])
        
        # Try to select content (triple-click method)
        pyautogui.click(config['response_coords'][0], config['response_coords'][1], clicks=3, interval=0.2)
        time.sleep(0.5)
        
        # Copy selection
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        # Get clipboard content
        try:
            response = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            
            if len(response) > 20:  # Valid response
                print(f"✅ Copied {len(response)} characters from {ai_name}")
                print(f"Preview: {response[:100]}...")
                return response
            else:
                print(f"⚠️ Response too short from {ai_name}, using fallback")
                return f"Response from {ai_name} (content capture failed)"
                
        except Exception as e:
            print(f"❌ Failed to copy from {ai_name}: {e}")
            return f"Response from {ai_name} (copy failed)"

    def run_loop(self, initial_message, rounds=1):
        """FIXED: Complete loop with proper desktop handling"""
        print(f"\n🎭 AI COUNCIL SEQUENTIAL LOOP")
        print(f"Initial message: {initial_message}")
        print(f"Rounds: {rounds}")
        print(f"Sequence: {' → '.join([ai.title() for ai in self.ai_order])}")
        
        message = initial_message
        
        for round_num in range(rounds):
            print(f"\n🔄 === ROUND {round_num + 1} ===")
            
            for ai in self.ai_order:
                print(f"\n{'='*60}")
                print(f"Processing: {ai.upper()}")
                print(f"{'='*60}")
                
                # Send message to current AI
                self.send_message_to_ai(ai, message)
                
                # Wait for response
                self.wait_for_response(ai)
                
                # Copy response for next AI
                response = self.copy_response(ai)
                
                # Use response as input for next AI
                message = response
                
                # Brief pause between AIs
                time.sleep(2)
            
            print(f"✅ Round {round_num + 1} completed")
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        print(f"\n🎉 Sequential loop complete!")

    def test_desktop_switching(self):
        """Test desktop switching functionality"""
        print("\n🧭 TESTING DESKTOP SWITCHING")
        
        for desktop in [1, 2, 0]:
            print(f"Switching to Desktop {desktop}...")
            self.switch_to_desktop(desktop)
            
            on_correct_desktop = input(f"Are you on Desktop {desktop}? (y/n): ")
            if on_correct_desktop.lower() != 'y':
                print(f"❌ Desktop switching to {desktop} failed")
                return False
        
        print("✅ Desktop switching working correctly")
        return True

    def test_single_ai(self, ai_name):
        """Test single AI interaction"""
        if ai_name not in self.ai_council:
            print(f"❌ Unknown AI: {ai_name}")
            return
        
        test_message = f"Test message for {ai_name} from fixed sequential system"
        
        self.send_message_to_ai(ai_name, test_message)
        self.wait_for_response(ai_name)
        response = self.copy_response(ai_name)
        
        self.switch_to_desktop(0)
        print(f"\n📝 Response from {ai_name}:")
        print(f"{response[:200]}...")

def main():
    """Main function with testing options"""
    council = AICouncilLoop()
    
    print("\n🎭 AI COUNCIL SEQUENTIAL SYSTEM - FIXED")
    print("Fixed desktop switching + coordinates + methods")
    
    while True:
        print(f"\n" + "="*50)
        print("CHOOSE ACTION:")
        print("1. Test desktop switching")
        print("2. Test single AI")
        print("3. Run sequential loop")
        print("4. Exit")
        
        choice = input("Choice (1-4): ")
        
        if choice == "1":
            council.test_desktop_switching()
            
        elif choice == "2":
            ai_name = input("Which AI (kai/claude/perplexity/grok): ").lower()
            council.test_single_ai(ai_name)
            
        elif choice == "3":
            message = input("Initial message: ") or "Sequential test from fixed AI Council system"
            rounds = int(input("Number of rounds (1-3): ") or "1")
            council.run_loop(message, rounds)
            
        elif choice == "4":
            print("👋 Fixed sequential system complete!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()