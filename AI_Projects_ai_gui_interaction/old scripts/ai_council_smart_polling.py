#!/usr/bin/env python3
"""
AI Council Smart Polling System
Jon's workflow: Send → Poll for changes → Copy response → Forward
Built on proven input methods + smart response capture
"""

import pyautogui
import subprocess
import time
import json
from datetime import datetime
import pyperclip

class AICouncilSmartPolling:
    """AI Council with smart polling for response capture"""
    
    def __init__(self):
        print("AI Council Smart Polling System")
        print("Send → Poll → Copy → Forward workflow")
        
        # Jon's AI Council layout
        self.ai_council = {
            "kai": {
                "name": "Kai",
                "desktop": 1,
                "position": "left",
                "input_coords": (456, 960),
                "response_coords": (456, 500),  # Response area above input
                "typing_method": "applescript"
            },
            "claude": {
                "name": "Claude",
                "desktop": 1,
                "position": "right", 
                "input_coords": (1200, 960),
                "response_coords": (1200, 500),
                "typing_method": "applescript"
            },
            "perplexity": {
                "name": "Perplexity",
                "desktop": 2,
                "position": "left",
                "input_coords": (456, 960),
                "response_coords": (456, 500),
                "typing_method": "applescript"
            },
            "grok": {
                "name": "Grok",
                "desktop": 2,
                "position": "right",
                "input_coords": (1548, 1000),
                "response_coords": (1548, 600),
                "typing_method": "clipboard"
            }
        }
        
        self.current_desktop = 0
        self.conversation_log = []
        
        # Polling settings (user configurable)
        self.poll_interval = 10  # Default: check every 10 seconds
        self.wait_interval = 5   # Default: wait 5 seconds if changes detected
        
    def switch_to_desktop(self, target_desktop: int):
        """Reliable desktop switching"""
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
    
    def click_to_focus(self, x: int, y: int):
        """Kai's proven click-to-focus method"""
        pyautogui.moveTo(x, y, duration=1)
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(0.8)
    
    def type_with_applescript(self, text: str):
        """Kai's proven AppleScript typing"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    def paste_with_applescript(self, text: str):
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
    
    def send_message_to_ai(self, ai_name: str, message: str):
        """Send message using proven methods"""
        
        ai = self.ai_council[ai_name]
        
        print(f"\n📤 Sending to {ai['name']}")
        print(f"   Desktop: {ai['desktop']} ({ai['position']})")
        print(f"   Message: {message[:100]}...")
        
        # Navigate and send
        self.switch_to_desktop(ai['desktop'])
        
        x, y = ai['input_coords']
        self.click_to_focus(x, y)
        
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        
        if ai['typing_method'] == 'applescript':
            self.type_with_applescript(message)
        elif ai['typing_method'] == 'clipboard':
            self.paste_with_applescript(message)
        
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1)
        
        print(f"✅ Message sent to {ai['name']}")
        return True
    
    def smart_poll_for_response(self, ai_name: str):
        """Jon's smart polling system for response detection"""
        
        ai = self.ai_council[ai_name]
        
        print(f"\n🔄 Smart polling for {ai['name']} response...")
        print(f"Will check every {self.poll_interval} seconds")
        
        # Return to Desktop 0 for polling questions
        self.switch_to_desktop(0)
        
        poll_count = 1
        max_polls = 6  # Maximum 6 polls = 60 seconds total
        
        while poll_count <= max_polls:
            print(f"\n📊 Poll {poll_count}/{max_polls} for {ai['name']}")
            
            # Ask user about changes
            changes = input(f"Any changes in {ai['name']}'s interface in the last {self.poll_interval} seconds? (y/n): ")
            
            if changes.lower() == 'n':
                print(f"✅ No changes - {ai['name']} response ready")
                return self.capture_response(ai_name)
            
            elif changes.lower() == 'y':
                print(f"🔄 Changes detected - waiting {self.wait_interval} more seconds...")
                time.sleep(self.wait_interval)
                poll_count += 1
                
            else:
                print("Please answer 'y' or 'n'")
                continue
        
        print(f"⏰ Maximum polls reached for {ai['name']} - capturing current state")
        return self.capture_response(ai_name)
    
    def capture_response(self, ai_name: str):
        """Capture AI's response using copy method"""
        
        ai = self.ai_council[ai_name]
        
        print(f"📋 Capturing response from {ai['name']}...")
        
        # Go to AI's desktop
        self.switch_to_desktop(ai['desktop'])
        
        # Click in response area
        resp_x, resp_y = ai['response_coords']
        self.click_to_focus(resp_x, resp_y)
        
        # Try to select recent response content
        # Method 1: Triple-click to select paragraph
        pyautogui.click(resp_x, resp_y, clicks=3, interval=0.2)
        time.sleep(0.5)
        
        # Copy selection
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        # Get clipboard content
        try:
            response = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            
            if len(response) > 20:  # Valid response
                print(f"✅ Captured {len(response)} characters from {ai['name']}")
                print(f"Preview: {response[:150]}...")
                
                # Log the response
                self.conversation_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'ai': ai_name,
                    'action': 'response_captured',
                    'content': response[:500],  # First 500 chars for log
                    'full_length': len(response)
                })
                
                return response
            else:
                print(f"⚠️ Captured content too short from {ai['name']}")
                return None
                
        except Exception as e:
            print(f"❌ Failed to capture from {ai['name']}: {e}")
            return None
    
    def run_smart_conversation_step(self, sender_ai: str, recipient_ai: str, message: str):
        """Single conversation step with smart polling"""
        
        print(f"\n{'='*70}")
        print(f"CONVERSATION STEP: {sender_ai.title()} → {recipient_ai.title()}")
        print(f"{'='*70}")
        
        # Step 1: Send message to recipient
        success = self.send_message_to_ai(recipient_ai, message)
        if not success:
            return None
        
        # Step 2: Smart poll for response
        response = self.smart_poll_for_response(recipient_ai)
        
        if response:
            print(f"✅ Successfully captured response from {recipient_ai}")
            return response
        else:
            print(f"⚠️ No valid response captured from {recipient_ai}")
            return None
    
    def run_full_smart_conversation(self, initial_topic: str, rounds: int = 1):
        """Complete conversation with smart polling"""
        
        print(f"\n🎭 AI COUNCIL SMART CONVERSATION")
        print(f"Topic: {initial_topic}")
        print(f"Rounds: {rounds}")
        print(f"Polling: Every {self.poll_interval}s, Wait: {self.wait_interval}s")
        
        relay_sequence = ["kai", "claude", "perplexity", "grok"]
        current_message = initial_topic
        
        for round_num in range(rounds):
            print(f"\n🔄 === ROUND {round_num + 1} ===")
            
            for i in range(len(relay_sequence)):
                sender = relay_sequence[i] if i > 0 else "human"
                recipient = relay_sequence[i]
                
                response = self.run_smart_conversation_step(sender, recipient, current_message)
                
                if response:
                    current_message = response  # Use response for next AI
                    print(f"🔗 Forwarding to next AI...")
                else:
                    print(f"⚠️ Using original message for next AI")
                
                # Brief pause between AIs
                time.sleep(2)
            
            print(f"✅ Round {round_num + 1} completed")
        
        # Return to Desktop 0 and save log
        self.switch_to_desktop(0)
        self.save_conversation_log()
        
        print(f"\n🎉 Smart conversation complete!")
    
    def configure_polling_settings(self):
        """Configure polling intervals"""
        
        print(f"\n⚙️ CONFIGURE POLLING SETTINGS")
        print(f"Current settings:")
        print(f"  Poll interval: {self.poll_interval} seconds")
        print(f"  Wait interval: {self.wait_interval} seconds")
        
        try:
            new_poll = input(f"New poll interval (current: {self.poll_interval}s): ")
            if new_poll:
                self.poll_interval = int(new_poll)
            
            new_wait = input(f"New wait interval (current: {self.wait_interval}s): ")
            if new_wait:
                self.wait_interval = int(new_wait)
            
            print(f"✅ Settings updated:")
            print(f"  Poll interval: {self.poll_interval} seconds")
            print(f"  Wait interval: {self.wait_interval} seconds")
            
        except ValueError:
            print("❌ Invalid input - keeping current settings")
    
    def test_single_smart_step(self):
        """Test single conversation step with polling"""
        
        ai_name = input("Which AI to test (kai/claude/perplexity/grok): ").lower()
        if ai_name not in self.ai_council:
            print("❌ Invalid AI name")
            return
        
        test_message = f"Smart polling test for {ai_name.title()}. Please respond with a few sentences so we can test the response capture system."
        
        response = self.run_smart_conversation_step("human", ai_name, test_message)
        
        if response:
            print(f"\n🎉 SUCCESS! Smart polling captured response:")
            print(f"{response[:300]}...")
        else:
            print(f"\n❌ Smart polling failed to capture response")
    
    def save_conversation_log(self):
        """Save conversation log"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"smart_conversation_{timestamp}.json"
        
        log_data = {
            'session_id': timestamp,
            'timestamp': datetime.now().isoformat(),
            'polling_settings': {
                'poll_interval': self.poll_interval,
                'wait_interval': self.wait_interval
            },
            'conversation_log': self.conversation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"💾 Conversation saved: {filename}")
        return filename

def main():
    """Main function for smart polling system"""
    
    system = AICouncilSmartPolling()
    
    print(f"\n🎭 AI COUNCIL SMART POLLING SYSTEM")
    print("Jon's workflow: Send → Poll → Copy → Forward")
    
    while True:
        print(f"\n" + "="*50)
        print("CHOOSE ACTION:")
        print("1. Test single smart step")
        print("2. Configure polling settings")
        print("3. Run full smart conversation")
        print("4. Save conversation log")
        print("5. Exit")
        
        choice = input("Choice (1-5): ")
        
        if choice == "1":
            system.test_single_smart_step()
            
        elif choice == "2":
            system.configure_polling_settings()
            
        elif choice == "3":
            topic = input("Conversation topic: ") or "What makes effective teamwork in AI development?"
            rounds = int(input("Number of rounds (1-3): ") or "1")
            system.run_full_smart_conversation(topic, rounds)
            
        elif choice == "4":
            system.save_conversation_log()
            
        elif choice == "5":
            system.save_conversation_log()
            print("👋 Smart polling session complete!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()