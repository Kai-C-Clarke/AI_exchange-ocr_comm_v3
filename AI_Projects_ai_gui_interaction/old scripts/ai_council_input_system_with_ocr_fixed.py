#!/usr/bin/env python3
"""
AI Council Input System
Proven methods for sending messages to all 4 AIs
Built for Kai's review and forward planning

WORKING METHODS:
- Kai: AppleScript typing (Desktop 1 Left)
- Claude: AppleScript typing (Desktop 1 Right)  
- Perplexity: AppleScript typing (Desktop 2 Left)
- Grok: Clipboard paste (Desktop 2 Right)
"""

import pyautogui
import subprocess
import time
import json
from datetime import datetime
import pyperclip

class AICouncilInputSystem:
    """Complete input system for all 4 AI Council members"""
    
    def __init__(self):
        print("AI Council Input System - All 4 AIs")
        print("Using proven methods for each AI")
        
        # Jon's exact AI layout with proven coordinates and methods
        self.ai_council = {
            "kai": {
                "name": "Kai",
                "desktop": 1,
                "position": "left",
                "input_coords": (456, 960),
                "typing_method": "applescript",
                "status": "✅ Proven working"
            },
            "claude": {
                "name": "Claude", 
                "desktop": 1,
                "position": "right",
                "input_coords": (1200, 960),
                "typing_method": "applescript",
                "status": "✅ Proven working"
            },
            "perplexity": {
                "name": "Perplexity",
                "desktop": 2, 
                "position": "left",
                "input_coords": (456, 960),
                "typing_method": "applescript", 
                "status": "✅ Proven working"
            },
            "grok": {
                "name": "Grok",
                "desktop": 2,
                "position": "right", 
                "input_coords": (1548, 1000),
                "typing_method": "clipboard",
                "status": "✅ Proven working (Kai's solution)"
            }
        }
        
        self.current_desktop = 0
        self.session_log = []
        
    def switch_to_desktop(self, target_desktop: int):
        """Reliable desktop switching"""
        if target_desktop == self.current_desktop:
            return True
        
        print(f"🧭 Desktop {self.current_desktop} → {target_desktop}")
        
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
        time.sleep(0.8)  # Extra time for focus
    
    def type_with_applescript(self, text: str):
        """Kai's proven AppleScript typing (works for Kai, Claude, Perplexity)"""
        escaped_text = text.replace('"', '\\"')
        script = f'''
        tell application "System Events"
            keystroke "{escaped_text}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    def paste_with_applescript(self, text: str):
        """Kai's clipboard solution (works for Grok)"""
        # Copy text to clipboard
        pyperclip.copy(text)
        time.sleep(0.3)
        
        # Paste using AppleScript (no emoji popup)
        script = '''
        tell application "System Events"
            keystroke "v" using {command down}
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    def send_message_to_ai(self, ai_name: str, message: str):
        """Send message to specific AI using their proven method"""
        
        if ai_name not in self.ai_council:
            print(f"❌ Unknown AI: {ai_name}")
            return False
        
        ai = self.ai_council[ai_name]
        
        print(f"\n📤 Sending to {ai['name']}")
        print(f"   Desktop: {ai['desktop']} ({ai['position']})")
        print(f"   Coordinates: {ai['input_coords']}")
        print(f"   Method: {ai['typing_method']}")
        print(f"   Message: {message[:100]}...")
        
        # Step 1: Navigate to AI's desktop
        self.switch_to_desktop(ai['desktop'])
        
        # Step 2: Click to focus input field
        x, y = ai['input_coords']
        self.click_to_focus(x, y)
        
        # Step 3: Clear existing content
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        
        # Step 4: Type using AI's preferred method
        if ai['typing_method'] == 'applescript':
            self.type_with_applescript(message)
        elif ai['typing_method'] == 'clipboard':
            self.paste_with_applescript(message)
        
        # Step 5: Send the message
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1.5)
        # Step 6: Log the interaction BEFORE OCR
        self.session_log.append({
            'timestamp': datetime.now().isoformat(),
            'ai': ai_name,
            'message': message[:200],
            'method': ai['typing_method'],
            'coordinates': ai['input_coords'],
            'desktop': ai['desktop'],
            'status': 'sent',
            'ocr_response': None
        })
        # Step 7: If Claude, capture screen for OCR
        if ai_name == "claude":
            from PIL import ImageGrab
            import pytesseract
            print("🔍 Capturing Claude's response for OCR...")
            time.sleep(3)
            region = (462, 171, 1100, 722)
            try:
                image = ImageGrab.grab(bbox=region)
                ocr_text = pytesseract.image_to_string(image).strip()
                print(f"[Claude OCR Response]\n{ocr_text}\n")
                self.session_log[-1]["ocr_response"] = ocr_text
            except Exception as e:
                print(f"⚠️ OCR failed: {e}")
                if self.session_log:
                    self.session_log[-1]["ocr_response"] = "OCR failed"
    
        # Step 6: If Claude, capture screen for OCR
        if ai_name == "claude":
            from PIL import ImageGrab
            import pytesseract
            print("🔍 Capturing Claude's response for OCR...")
            time.sleep(3)  # wait for Claude to respond
            region = (462, 171, 1100, 722)
            try:
                image = ImageGrab.grab(bbox=region)
                ocr_text = pytesseract.image_to_string(image).strip()
                print(f"[Claude OCR Response]\n{ocr_text}\n")
                self.session_log[-1]["ocr_response"] = ocr_text
            except Exception as e:
                print(f"⚠️ OCR failed: {e}")
                self.session_log[-1]["ocr_response"] = "OCR failed"

        
        # Log the interaction
        self.session_log.append({
            'timestamp': datetime.now().isoformat(),
            'ai': ai_name,
            'message': message[:200],  # First 200 chars
            'method': ai['typing_method'],
            'coordinates': ai['input_coords'],
            'desktop': ai['desktop'],
            'status': 'sent'
        })
        
        print(f"✅ Message sent to {ai['name']}")
        return True
    
    def test_single_ai(self, ai_name: str):
        """Test sending to a single AI"""
        
        test_message = f"Test message for {ai_name.title()} from AI Council Input System. Please respond with a brief acknowledgment."
        
        print(f"\n🧪 TESTING {ai_name.upper()}")
        print(f"Using {self.ai_council[ai_name]['typing_method']} method")
        
        success = self.send_message_to_ai(ai_name, test_message)
        
        if success:
            # Return to Desktop 0 for feedback
            self.switch_to_desktop(0)
            
            worked = input(f"Did {ai_name.title()} receive the test message successfully? (y/n): ")
            return worked.lower() == 'y'
        
        return False
    
    def test_all_ais_sequential(self):
        """Test all 4 AIs in sequence"""
        
        print(f"\n🎭 TESTING ALL AI COUNCIL MEMBERS")
        print("Sequential testing of all 4 AIs")
        
        test_message = "Sequential test from AI Council Input System. This message is being sent to all council members to verify communication channels."
        
        results = {}
        
        for ai_name in ["kai", "claude", "perplexity", "grok"]:
            print(f"\n{'='*60}")
            print(f"Testing {ai_name.upper()}")
            print(f"{'='*60}")
            
            success = self.send_message_to_ai(ai_name, test_message)
            
            if success:
                # Brief pause between AIs
                time.sleep(2)
                results[ai_name] = "sent"
            else:
                results[ai_name] = "failed"
        
        # Return to Desktop 0 for summary
        self.switch_to_desktop(0)
        
        # Print results
        print(f"\n📊 SEQUENTIAL TEST RESULTS:")
        for ai_name, status in results.items():
            ai = self.ai_council[ai_name]
            status_icon = "✅" if status == "sent" else "❌"
            print(f"   {status_icon} {ai['name']}: {status}")
        
        success_count = sum(1 for status in results.values() if status == "sent")
        print(f"\n🎯 {success_count}/4 AIs successfully messaged")
        
        return results
    
    def test_relay_simulation(self):
        """Simulate an AI Council relay"""
        
        print(f"\n🔄 AI COUNCIL RELAY SIMULATION")
        print("Sending different messages to each AI in relay sequence")
        
        # Relay sequence and messages
        relay_sequence = [
            ("kai", "Initial question: What are the key principles for ethical AI development?"),
            ("claude", "Building on Kai's insights about ethical AI principles, what implementation challenges should we consider?"),  
            ("perplexity", "Given the ethical principles and implementation challenges discussed, what metrics should we use to evaluate AI systems?"),
            ("grok", "Considering the principles, challenges, and metrics mentioned, what practical recommendations would you make for AI developers?")
        ]
        
        print(f"Relay sequence: {' → '.join([ai.title() for ai, _ in relay_sequence])}")
        print("Starting relay simulation in 3 seconds...")
        time.sleep(3)
        
        for i, (ai_name, message) in enumerate(relay_sequence):
            print(f"\n🔗 Relay Step {i+1}: {ai_name.title()}")
            
            success = self.send_message_to_ai(ai_name, message)
            
            if not success:
                print(f"❌ Relay failed at {ai_name}")
                break
            
            # Pause between relay steps
            time.sleep(3)
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        print(f"\n✅ Relay simulation complete")
        print("Check each AI interface to see the relay messages")
    
    def show_system_status(self):
        """Display current system status and capabilities"""
        
        print(f"\n📋 AI COUNCIL INPUT SYSTEM STATUS")
        print("="*60)
        
        for ai_name, ai in self.ai_council.items():
            print(f"\n🤖 {ai['name'].upper()}")
            print(f"   Location: Desktop {ai['desktop']} ({ai['position']} side)")
            print(f"   Coordinates: {ai['input_coords']}")
            print(f"   Input Method: {ai['typing_method']}")
            print(f"   Status: {ai['status']}")
        
        print(f"\n🔧 CAPABILITIES:")
        print("   ✅ Send messages to all 4 AIs")
        print("   ✅ Cross-desktop navigation") 
        print("   ✅ Emoji-popup-free operation")
        print("   ✅ Reliable coordinate targeting")
        print("   ✅ Method-specific typing (AppleScript + Clipboard)")
        
        print(f"\n🎯 READY FOR:")
        print("   📤 Message input testing")
        print("   🔄 Relay simulations") 
        print("   📋 Response capture development (next phase)")
        print("   🎭 Full AI Council automation")
    
    def save_session_log(self):
        """Save session log for review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_input_session_{timestamp}.json"
        
        session_data = {
            'session_id': timestamp,
            'timestamp': datetime.now().isoformat(),
            'ai_council_config': self.ai_council,
            'session_log': self.session_log,
            'summary': {
                'total_messages': len(self.session_log),
                'ais_messaged': len(set(entry['ai'] for entry in self.session_log)),
                'methods_used': list(set(entry['method'] for entry in self.session_log))
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"💾 Session saved: {filename}")
        return filename

def main():
    """Main function for AI Council Input System"""
    
    system = AICouncilInputSystem()
    
    print(f"\n🎭 AI COUNCIL INPUT SYSTEM")
    print("Complete input solution for all 4 AIs")
    print("Built with Jon's coordinates + Kai's proven methods")
    
    while True:
        print(f"\n" + "="*50)
        print("CHOOSE TEST:")
        print("1. Show system status")
        print("2. Test single AI")
        print("3. Test all AIs sequentially") 
        print("4. Relay simulation")
        print("5. Save session log")
        print("6. Exit")
        
        choice = input("Choice (1-6): ")
        
        if choice == "1":
            system.show_system_status()
            
        elif choice == "2":
            ai_name = input("Which AI (kai/claude/perplexity/grok): ").lower()
            if ai_name in system.ai_council:
                system.test_single_ai(ai_name)
            else:
                print("❌ Invalid AI name")
                
        elif choice == "3":
            system.test_all_ais_sequential()
            
        elif choice == "4":
            system.test_relay_simulation()
            
        elif choice == "5":
            system.save_session_log()
            
        elif choice == "6":
            system.save_session_log()
            print("👋 Session complete!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()