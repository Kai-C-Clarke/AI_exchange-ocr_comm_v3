#!/usr/bin/env python3
"""
AI COUNCIL AUTONOMOUS COMMUNICATION LOOP
The full relay system - Kai → Claude → Finn → Perplexity → Kai

Built on Jon's breakthrough UI targeting system
"""

import pyautogui
import subprocess
import time
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
import re

@dataclass
class CouncilMember:
    """Individual AI Council member configuration"""
    name: str
    window_keywords: List[str]  # Keywords to identify their window
    ui_profile: str            # UI targeting profile
    response_area_coords: tuple = None  # Where to read responses
    input_coords: tuple = None          # Where to send messages
    send_trigger: str = "enter"         # How to send (enter/button)

@dataclass
class CouncilMessage:
    """Structured message in the council communication"""
    sender: str
    recipient: str
    content: str
    timestamp: datetime
    message_id: str
    topic_id: str
    session_id: str

class AICouncilLoop:
    """The complete AI Council automation system"""
    
    def __init__(self, session_topic: str = "AI Council Discussion"):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_topic = session_topic
        self.message_log = []
        self.response_archive = []
        
        # Define the Council members and their relay sequence
        self.council_members = {
            "kai": CouncilMember(
                name="Kai",
                window_keywords=["kai", "claude", "anthropic"],
                ui_profile="claude_interface"
            ),
            "claude": CouncilMember(
                name="Claude", 
                window_keywords=["claude", "anthropic"],
                ui_profile="claude_interface"
            ),
            "finn": CouncilMember(
                name="Finn Harper",
                window_keywords=["chatgpt", "openai", "gpt"],
                ui_profile="chatgpt_interface"
            ),
            "perplexity": CouncilMember(
                name="Perplexity",
                window_keywords=["perplexity", "pplx"],
                ui_profile="perplexity_interface"
            )
        }
        
        # Council relay sequence
        self.relay_sequence = ["kai", "claude", "finn", "perplexity"]
        
        # UI targeting profiles
        self.ui_profiles = {
            "claude_interface": {
                "input_position": (0.5, 0.9),    # Center, bottom 10%
                "response_position": (0.5, 0.4), # Center, middle area
                "send_method": "enter"
            },
            "chatgpt_interface": {
                "input_position": (0.5, 0.92),
                "response_position": (0.5, 0.45),
                "send_method": "enter"
            },
            "perplexity_interface": {
                "input_position": (0.5, 0.88),
                "response_position": (0.5, 0.4),
                "send_method": "enter"
            }
        }
        
        print(f"🎯 AI Council Loop initialized")
        print(f"   Session ID: {self.session_id}")
        print(f"   Topic: {self.session_topic}")
        print(f"   Relay sequence: {' → '.join([m.title() for m in self.relay_sequence])}")
    
    def get_all_windows(self):
        """Get all open windows (from our proven system)"""
        try:
            script = '''
            tell application "System Events"
                set windowList to {}
                repeat with proc in (every application process whose visible is true)
                    set appName to name of proc
                    try
                        repeat with win in (every window of proc)
                            set winName to name of win
                            set winPos to position of win
                            set winSize to size of win
                            set end of windowList to {appName, winName, (item 1 of winPos), (item 2 of winPos), (item 1 of winSize), (item 2 of winSize)}
                        end repeat
                    end try
                end repeat
                
                set output to ""
                repeat with winInfo in windowList
                    set output to output & (item 1 of winInfo) & "|" & (item 2 of winInfo) & "|" & (item 3 of winInfo) & "," & (item 4 of winInfo) & "|" & (item 5 of winInfo) & "," & (item 6 of winInfo) & "\\n"
                end repeat
                
                return output
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            windows = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            app_name = parts[0]
                            window_title = parts[1]
                            pos = list(map(int, parts[2].split(',')))
                            size = list(map(int, parts[3].split(',')))
                            
                            windows.append({
                                'app_name': app_name,
                                'window_title': window_title,
                                'x': pos[0],
                                'y': pos[1],
                                'width': size[0],
                                'height': size[1]
                            })
            
            return windows
            
        except Exception as e:
            print(f"❌ Window enumeration failed: {e}")
            return []
    
    def find_member_window(self, member_name: str):
        """Find the window for a specific council member"""
        
        member = self.council_members[member_name]
        all_windows = self.get_all_windows()
        
        print(f"🔍 Searching for {member.name} window...")
        
        candidates = []
        for window in all_windows:
            window_text = f"{window['app_name']} {window['window_title']}".lower()
            
            # Score window based on keyword matches
            score = 0
            matches = []
            
            for keyword in member.window_keywords:
                if keyword in window_text:
                    score += 10
                    matches.append(keyword)
            
            # Boost score for reasonable window size
            if window['width'] > 600 and window['height'] > 400:
                score += 5
            
            if score > 0:
                candidates.append({
                    **window,
                    'score': score,
                    'matches': matches
                })
                print(f"   Candidate: {window['app_name']} (score: {score}, matches: {matches})")
        
        if not candidates:
            print(f"❌ No window found for {member.name}")
            return None
        
        # Return highest scoring window
        best_window = max(candidates, key=lambda w: w['score'])
        print(f"✅ Selected: {best_window['app_name']} - {best_window['window_title'][:50]}...")
        
        return best_window
    
    def calculate_coordinates(self, window_info: Dict, member_name: str):
        """Calculate input and response coordinates for a member's window"""
        
        member = self.council_members[member_name]
        profile = self.ui_profiles[member.ui_profile]
        
        # Calculate input field coordinates
        input_x = window_info['x'] + int(window_info['width'] * profile['input_position'][0])
        input_y = window_info['y'] + int(window_info['height'] * profile['input_position'][1])
        
        # Calculate response area coordinates  
        response_x = window_info['x'] + int(window_info['width'] * profile['response_position'][0])
        response_y = window_info['y'] + int(window_info['height'] * profile['response_position'][1])
        
        return {
            'input_coords': (input_x, input_y),
            'response_coords': (response_x, response_y),
            'send_method': profile['send_method']
        }
    
    def activate_window(self, window_info: Dict):
        """Bring a window to the front"""
        try:
            app_name = window_info['app_name']
            script = f'tell application "{app_name}" to activate'
            
            subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
            
            time.sleep(1)  # Allow activation
            return True
            
        except Exception as e:
            print(f"❌ Failed to activate {window_info['app_name']}: {e}")
            return False
    
    def read_response_area(self, member_name: str):
        """Read the latest response from a member's window"""
        
        window_info = self.find_member_window(member_name)
        if not window_info:
            return None
        
        coords_info = self.calculate_coordinates(window_info, member_name)
        response_coords = coords_info['response_coords']
        
        print(f"📖 Reading response from {member_name} at {response_coords}")
        
        # Activate window
        self.activate_window(window_info)
        
        # Click in response area and select content
        pyautogui.click(response_coords[0], response_coords[1])
        time.sleep(0.3)
        
        # Try to select recent response content
        # This might need refinement based on each UI's behavior
        pyautogui.hotkey("command", "a")  # Select all (or recent content)
        time.sleep(0.2)
        
        pyautogui.hotkey("command", "c")  # Copy
        time.sleep(0.2)
        
        # Get clipboard content
        try:
            content = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"✅ Captured {len(content)} characters from {member_name}")
            return content
        except Exception as e:
            print(f"❌ Failed to read response from {member_name}: {e}")
            return None
    
    def send_message_to_member(self, member_name: str, message: str):
        """Send a message to a specific council member"""
        
        window_info = self.find_member_window(member_name)
        if not window_info:
            return False
        
        coords_info = self.calculate_coordinates(window_info, member_name)
        input_coords = coords_info['input_coords']
        
        print(f"📤 Sending to {member_name} at {input_coords}")
        
        # Activate window
        self.activate_window(window_info)
        
        # Click input field
        pyautogui.click(input_coords[0], input_coords[1])
        time.sleep(0.3)
        
        # Clear field and type message
        pyautogui.hotkey("command", "a")  # Select all
        time.sleep(0.1)
        
        pyautogui.typewrite(message)
        time.sleep(0.5)
        
        # Send the message
        if coords_info['send_method'] == "enter":
            pyautogui.press("enter")
            time.sleep(1)
        
        print(f"✅ Message sent to {member_name}")
        return True
    
    def create_council_message(self, sender: str, recipient: str, content: str, topic_id: str = None):
        """Create a structured council message"""
        
        if topic_id is None:
            topic_id = f"topic_{len(self.message_log) + 1}"
        
        message = CouncilMessage(
            sender=sender,
            recipient=recipient, 
            content=content,
            timestamp=datetime.now(),
            message_id=f"msg_{len(self.message_log) + 1}",
            topic_id=topic_id,
            session_id=self.session_id
        )
        
        self.message_log.append(message)
        return message
    
    def run_single_relay_step(self, sender: str, recipient: str, message: str):
        """Execute one step in the council relay"""
        
        print(f"\n🔄 RELAY STEP: {sender.title()} → {recipient.title()}")
        print(f"   Message: {message[:100]}...")
        
        # Create structured message
        council_msg = self.create_council_message(sender, recipient, message)
        
        # Send message to recipient
        success = self.send_message_to_member(recipient, message)
        
        if success:
            # Wait for response (configurable delay)
            print(f"⏱️  Waiting for {recipient} to respond...")
            time.sleep(10)  # Give AI time to generate response
            
            # Read the response
            response = self.read_response_area(recipient)
            
            if response:
                # Archive the response
                response_msg = self.create_council_message(
                    recipient, "council", response, council_msg.topic_id
                )
                self.response_archive.append(response_msg)
                
                print(f"✅ Received response from {recipient}")
                return response
            else:
                print(f"⚠️  No response captured from {recipient}")
                return None
        else:
            print(f"❌ Failed to send message to {recipient}")
            return None
    
    def run_full_council_discussion(self, initial_topic: str, rounds: int = 1):
        """Run a complete council discussion through multiple rounds"""
        
        print(f"\n🎭 STARTING AI COUNCIL DISCUSSION")
        print(f"   Topic: {initial_topic}")
        print(f"   Rounds: {rounds}")
        print(f"   Sequence: {' → '.join([m.title() for m in self.relay_sequence])}")
        
        current_message = initial_topic
        
        for round_num in range(rounds):
            print(f"\n🔄 === ROUND {round_num + 1} ===")
            
            # Go through the full relay sequence
            for i in range(len(self.relay_sequence)):
                sender = self.relay_sequence[i]
                recipient = self.relay_sequence[(i + 1) % len(self.relay_sequence)]
                
                response = self.run_single_relay_step(sender, recipient, current_message)
                
                if response:
                    current_message = response  # Use response as input for next step
                else:
                    print(f"⚠️  Breaking relay due to failed step: {sender} → {recipient}")
                    break
            
            print(f"✅ Round {round_num + 1} complete")
        
        # Save session log
        self.save_session_log()
        print(f"\n🎉 AI Council discussion complete! Check logs for full conversation.")
    
    def save_session_log(self):
        """Save the complete session log"""
        
        session_data = {
            'session_id': self.session_id,
            'topic': self.session_topic,
            'timestamp': datetime.now().isoformat(),
            'relay_sequence': self.relay_sequence,
            'message_log': [
                {
                    'sender': msg.sender,
                    'recipient': msg.recipient,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'message_id': msg.message_id,
                    'topic_id': msg.topic_id
                }
                for msg in self.message_log
            ],
            'response_archive': [
                {
                    'sender': resp.sender,
                    'recipient': resp.recipient,
                    'content': resp.content,
                    'timestamp': resp.timestamp.isoformat(),
                    'message_id': resp.message_id,
                    'topic_id': resp.topic_id
                }
                for resp in self.response_archive
            ]
        }
        
        filename = f"ai_council_session_{self.session_id}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session log saved: {filename}")
        return filename

def demo_council_system():
    """Demonstrate the AI Council automation system"""
    
    print("🚀 AI COUNCIL AUTONOMOUS COMMUNICATION DEMO")
    print("=" * 60)
    
    # Initialize the council
    council = AICouncilLoop("AI Ethics and Decision Making")
    
    # Test individual components first
    print("\n📋 Testing Window Detection...")
    for member_name in council.relay_sequence:
        window = council.find_member_window(member_name)
        if window:
            coords = council.calculate_coordinates(window, member_name)
            print(f"✅ {member_name.title()}: {coords['input_coords']}")
        else:
            print(f"❌ {member_name.title()}: No window found")
    
    # Ask user if they want to run a full discussion
    response = input(f"\n🎭 Run a full AI Council discussion? (y/n): ")
    
    if response.lower() == 'y':
        topic = input("Enter discussion topic (or press Enter for default): ").strip()
        if not topic:
            topic = "What are the most important considerations for AI safety and beneficial development?"
        
        rounds = int(input("Number of rounds (default 1): ") or "1")
        
        council.run_full_council_discussion(topic, rounds)
    else:
        print("Demo complete - ready for full automation when you are!")

if __name__ == "__main__":
    demo_council_system()