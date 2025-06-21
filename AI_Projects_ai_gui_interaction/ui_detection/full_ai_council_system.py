#!/usr/bin/env python3
"""
Complete Working AI Council System
Fixes: Grok coordinates + Response capture + Scrolling
"""

import pyautogui
import subprocess
import time
import json
from datetime import datetime

class CompleteWorkingSystem:
    """Complete AI Council with response capture and proper coordination"""
    
    def __init__(self):
        # Jon's AI layout - with adjusted Grok coordinates
        self.ai_targets = {
            "kai": {
                "desktop": 1, 
                "input_coords": (456, 960),
                "response_coords": (456, 600)  # Higher up for response area
            },
            "claude": {
                "desktop": 1, 
                "input_coords": (1200, 960),
                "response_coords": (1200, 600)
            },
            "perplexity": {
                "desktop": 2, 
                "input_coords": (456, 960),
                "response_coords": (456, 600)
            },
            "grok": {
                "desktop": 2, 
                "input_coords": (1548, 988),  # Jon's exact Grok coordinates - center of input area
                "response_coords": (1548, 600)
            }
        }
        
        self.current_desktop = 0
        self.conversation_log = []
        
        print("Complete Working AI Council System")
        print("Message sending + Response capture + Scrolling")
    
    def switch_desktop(self, target_desktop: int):
        """Reliable desktop switching"""
        if target_desktop == self.current_desktop:
            return True
        
        print(f"Desktop {self.current_desktop} -> {target_desktop}")
        
        if target_desktop > self.current_desktop:
            moves = target_desktop - self.current_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "right")
                time.sleep(1)
        else:
            moves = self.current_desktop - target_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "left")
                time.sleep(1)
        
        self.current_desktop = target_desktop
        time.sleep(1.5)  # Extra time for desktop switch
        return True
    
    def click_to_focus(self, x: int, y: int):
        """Kai's click-to-focus method"""
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)
    
    def type_with_applescript(self, text: str):
        """Kai's AppleScript typing method"""
        escaped_text = text.replace('"', '\\"')
        
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    def send_message_to_ai(self, ai_name: str, message: str):
        """Send message using Kai's proven method"""
        
        target = self.ai_targets[ai_name]
        
        print(f"\nSending to {ai_name.upper()}")
        print(f"Desktop: {target['desktop']}, Coords: {target['input_coords']}")
        
        # Switch to AI's desktop
        self.switch_desktop(target['desktop'])
        
        # Click to focus
        x, y = target['input_coords']
        self.click_to_focus(x, y)
        
        # Clear existing content
        pyautogui.hotkey("command", "a")
        time.sleep(0.3)
        
        # Type with AppleScript
        self.type_with_applescript(message)
        
        # Send
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)  # Wait for message to send
        
        print(f"✅ Message sent to {ai_name}")
        return True
    
    def scroll_to_latest_response(self, ai_name: str):
        """Scroll to see the latest response"""
        
        target = self.ai_targets[ai_name]
        
        # Make sure we're on the right desktop
        self.switch_desktop(target['desktop'])
        
        # Click in response area
        resp_x, resp_y = target['response_coords']
        self.click_to_focus(resp_x, resp_y)
        
        # Scroll down to see latest response
        print(f"Scrolling to latest response in {ai_name}")
        for _ in range(5):  # Scroll down several times
            pyautogui.scroll(-3)  # Scroll down
            time.sleep(0.3)
        
        time.sleep(1)  # Let scrolling settle
    
    def capture_ai_response(self, ai_name: str, wait_time: int = 15):
        """Capture AI response with scrolling"""
        
        target = self.ai_targets[ai_name]
        
        print(f"Waiting {wait_time}s for {ai_name} to respond...")
        time.sleep(wait_time)
        
        # Make sure we're on the right desktop
        self.switch_desktop(target['desktop'])
        
        # Scroll to see latest content
        self.scroll_to_latest_response(ai_name)
        
        # Click in response area
        resp_x, resp_y = target['response_coords']
        self.click_to_focus(resp_x, resp_y)
        
        # Try to select the most recent response
        # Strategy: Select a reasonable amount of recent content
        pyautogui.hotkey("command", "shift", "end")  # Select from cursor to end
        time.sleep(0.5)
        
        # Copy selection
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        # Get clipboard content
        try:
            response = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            
            # Clean the response
            clean_response = self.clean_response(response)
            
            if len(clean_response) > 50:  # Valid response
                print(f"✅ Captured {len(clean_response)} chars from {ai_name}")
                return clean_response
            else:
                print(f"⚠️ No substantial response from {ai_name}")
                return None
                
        except Exception as e:
            print(f"❌ Failed to capture from {ai_name}: {e}")
            return None
    
    def clean_response(self, response: str):
        """Clean captured response to get just the AI's reply"""
        
        # Remove common UI junk
        junk_phrases = [
            "Skip to content", "Home", "Library", "Account", 
            "You said:", "Claude said:", "New chat",
            "import ", "def ", "class ", "#!/usr/bin/",
            "Last login:", "jonstiles@"
        ]
        
        lines = response.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines containing junk
            if any(junk in line for junk in junk_phrases):
                continue
            
            # Skip very short lines (likely UI elements)
            if len(line) < 15:
                continue
            
            clean_lines.append(line)
        
        # Join clean lines
        clean_response = ' '.join(clean_lines)
        
        # Limit length for next AI
        if len(clean_response) > 800:
            clean_response = clean_response[:800] + "..."
        
        return clean_response.strip()
    
    def test_grok_coordinates(self):
        """Test different coordinates for Grok"""
        
        print("\n🎯 TESTING GROK COORDINATES")
        print("Trying different positions for Grok")
        
        grok_candidates = [
            (1200, 960),  # Same as Claude but on Desktop 2
            (1400, 960),  # Further right
            (1300, 960),  # Middle right
            (1500, 960),  # Far right
        ]
        
        for i, coords in enumerate(grok_candidates):
            print(f"\nTesting Grok position {i+1}: {coords}")
            
            # Update Grok coordinates temporarily
            self.ai_targets["grok"]["input_coords"] = coords
            
            ready = input(f"Test coordinates {coords}? (y/n): ")
            if ready.lower() != 'y':
                continue
            
            success = self.send_message_to_ai("grok", f"Test message {i+1} for Grok coordinate testing")
            
            if success:
                worked = input(f"Did Grok receive the message at {coords}? (y/n): ")
                if worked.lower() == 'y':
                    print(f"✅ Found working Grok coordinates: {coords}")
                    return coords
        
        print("❌ No working coordinates found for Grok")
        return None
    
    def run_complete_relay(self, initial_message: str):
        """Complete relay with response capture and forwarding"""
        
        print(f"\n🔄 COMPLETE AI RELAY WITH RESPONSE CAPTURE")
        print("Each AI's response becomes input for the next AI")
        
        sequence = ["kai", "claude", "perplexity", "grok"]
        current_message = initial_message
        
        print(f"\nStarting complete relay in 5 seconds...")
        time.sleep(5)
        
        for i, ai_name in enumerate(sequence):
            print(f"\n{'='*60}")
            print(f"Step {i+1}: {ai_name.upper()}")
            print(f"{'='*60}")
            
            # Send current message
            print(f"Sending: {current_message[:100]}...")
            success = self.send_message_to_ai(ai_name, current_message)
            
            if not success:
                print(f"Failed to send to {ai_name} - stopping relay")
                break
            
            # Capture response
            response = self.capture_ai_response(ai_name)
            
            if response and len(response) > 50:
                print(f"Response: {response[:200]}...")
                current_message = response  # Use response for next AI
                
                # Log the interaction
                self.conversation_log.append({
                    'step': i+1,
                    'ai': ai_name,
                    'input': current_message[:200],
                    'response': response[:200],
                    'timestamp': datetime.now().isoformat()
                })
                
            else:
                print(f"No valid response from {ai_name} - using original message")
                # Continue with original message instead of stopping
            
            print(f"✅ {ai_name} step complete")
        
        # Return to Desktop 0
        self.switch_desktop(0)
        
        # Save conversation log
        self.save_conversation_log()
        
        print(f"\n🎉 Complete relay finished!")
        print("Check conversation log for full discussion thread")
    
    def save_conversation_log(self):
        """Save the complete conversation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_conversation_{timestamp}.json"
        
        conversation_data = {
            'session_id': timestamp,
            'timestamp': datetime.now().isoformat(),
            'ai_targets': self.ai_targets,
            'conversation_log': self.conversation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        print(f"💾 Conversation saved: {filename}")
        return filename

def main():
    """Main function for complete system"""
    
    system = CompleteWorkingSystem()
    
    print(f"\nCOMPLETE AI COUNCIL SYSTEM")
    print("Message sending + Response capture + Scrolling support")
    
    choice = input(f"\nChoose:\n1. Test Grok coordinates\n2. Test single AI\n3. Complete relay with response capture\nChoice: ")
    
    if choice == "1":
        working_coords = system.test_grok_coordinates()
        if working_coords:
            print(f"Update Grok coordinates to: {working_coords}")
    
    elif choice == "2":
        ai_name = input("Which AI (kai/claude/perplexity/grok): ").lower()
        if ai_name in system.ai_targets:
            system.send_message_to_ai(ai_name, "Test message with response capture")
            response = system.capture_ai_response(ai_name)
            if response:
                print(f"Captured response: {response[:300]}...")
    
    elif choice == "3":
        message = input("Initial message: ") or "What is the most important quality for effective teamwork?"
        system.run_complete_relay(message)
    
    print(f"\n✅ Complete system test finished!")

if __name__ == "__main__":
    main()