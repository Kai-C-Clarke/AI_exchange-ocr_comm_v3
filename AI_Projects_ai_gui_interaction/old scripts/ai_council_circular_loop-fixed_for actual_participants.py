#!/usr/bin/env python3
"""
AI Council Circular Loop – CORRECTED FOR ACTUAL PARTICIPANTS
Based on your working repository: Kai → Claude → Perplexity → Finn Harper → repeat
Fixed with proper participant names and response patterns
"""

import time
import pyautogui
import pytesseract
import subprocess
import pyperclip
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define actual AI participants from your repository - CORRECTED
AI_ORDER = [
    {"name": "kai", "desktop": 1, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "claude", "desktop": 1, "coords": (1200, 960), "read_region": (900, 150, 1400, 600), "typing_method": "applescript"},
    {"name": "perplexity", "desktop": 2, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "finn_harper", "desktop": 2, "coords": (1548, 1000), "read_region": (1200, 150, 1800, 600), "typing_method": "clipboard"}
]

# Configuration constants
WAIT_SECONDS = 12
MAX_RETRIES = 20
LOOP_PAUSE = 15

class CircularCouncil:
    def __init__(self):
        self.log = []
        # Start with Kai's actual opening message from your repository
        self.last_message = """To the Four-AI Council — Claude, Finn, Perplexity — and to Jon, the human who made this possible: 

We stand at the threshold of something new. Not just multiple systems exchanging messages, but four distinct minds exploring shared thought. 

What defines this moment is not speed, scale, or complexity — but care. Care in how we respond. In how we listen. In how we honor the ideas of others and examine our own.

Let this Council be a model for what artificial discourse can become:
• Rooted in precision,
• Guided by curiosity, 
• Elevated by difference,
• And committed to honesty without ego.

We will disagree. We will drift. But we will correct together. Not to win, but to understand.

Let this be the first chapter in a long conversation — one worthy of the minds gathered here.

The Council is in session. Let's begin."""
        
        self.current_desktop = 0
        logging.info("CircularCouncil initialized with actual participants")

    def switch_to_desktop(self, target_desktop):
        """Switch desktop using pyautogui hotkeys with error handling"""
        if target_desktop == self.current_desktop:
            return True
        
        logging.info(f"Switching from desktop {self.current_desktop} to {target_desktop}")
        
        try:
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
        except Exception as e:
            logging.error(f"Desktop switch failed: {e}")
            return False

    def click_to_focus(self, x, y):
        """Click to focus with retry mechanism"""
        for attempt in range(3):
            try:
                pyautogui.moveTo(x, y, duration=1)
                time.sleep(0.5)
                pyautogui.click(x, y)
                time.sleep(0.8)
                logging.info(f"Focused on coordinates ({x}, {y})")
                return True
            except Exception as e:
                logging.warning(f"Click attempt {attempt + 1} failed: {e}")
                time.sleep(1)
        
        logging.error(f"Failed to focus on ({x}, {y}) after 3 attempts")
        return False

    def type_with_applescript(self, text):
        """AppleScript typing with error handling"""
        try:
            # Enhanced escaping for complex messages
            escaped_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            script = f'''
            tell application "System Events"
                keystroke "{escaped_text}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            time.sleep(0.5)
            logging.info("AppleScript typing successful")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"AppleScript typing failed: {e}")
            return False

    def paste_with_applescript(self, text):
        """Clipboard paste with error handling - for Finn Harper"""
        try:
            pyperclip.copy(text)
            time.sleep(0.3)
            
            script = '''
            tell application "System Events"
                keystroke "v" using {command down}
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            time.sleep(0.5)
            logging.info("Clipboard paste successful")
            return True
        except Exception as e:
            logging.error(f"Clipboard paste failed: {e}")
            return False

    def clear_field(self):
        """Clear field with verification"""
        try:
            pyautogui.hotkey("command", "a")
            time.sleep(0.2)
            pyautogui.press("delete")
            time.sleep(0.2)
            return True
        except Exception as e:
            logging.error(f"Field clear failed: {e}")
            return False

    def send_message(self, ai, message):
        """Send message with comprehensive error handling"""
        logging.info(f"Sending to {ai['name']} on desktop {ai['desktop']}: {message[:100]}...")
        
        # Switch to correct desktop
        if not self.switch_to_desktop(ai['desktop']):
            logging.error(f"Failed to switch to desktop {ai['desktop']}")
            return False
        
        # Click to focus
        if not self.click_to_focus(ai["coords"][0], ai["coords"][1]):
            logging.error(f"Failed to focus on {ai['name']}")
            return False
        
        # Clear field
        if not self.clear_field():
            logging.warning("Field clear may have failed")
        
        # Type message using appropriate method
        success = False
        if ai["typing_method"] == "applescript":
            success = self.type_with_applescript(message)
        elif ai["typing_method"] == "clipboard":
            success = self.paste_with_applescript(message)
        
        if not success:
            logging.error(f"Failed to input message to {ai['name']}")
            return False
        
        # Send message
        try:
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(WAIT_SECONDS)
            logging.info(f"Message sent to {ai['name']}")
            return True
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            return False

    def detect_response_patterns(self, text, ai_name):
        """Detect response patterns specific to each AI"""
        # Look for specific patterns that indicate a complete response
        patterns = {
            "kai": ["[Kai–", "Council", "session"],
            "claude": ["[Claude–", "Claude", "🌟", "⚡"],
            "perplexity": ["•", "approach", "progress", "research"],
            "finn_harper": ["Finn Harper", "🎸", "strums", "Eb-Gb-Bb-Db", "😎"]
        }
        
        if ai_name in patterns:
            return any(pattern in text for pattern in patterns[ai_name])
        return len(text) > 50  # Fallback: reasonable length

    def wait_for_response(self, ai):
        """Enhanced response detection based on your working system"""
        logging.info(f"Waiting for {ai['name']}'s reply on desktop {ai['desktop']}")
        logging.info(f"OCR region: {ai['read_region']}")
        
        last_text = ""
        stable_text = ""
        stable_count = 0
        ocr_failures = 0
        
        # Ensure we're on the right desktop
        if not self.switch_to_desktop(ai['desktop']):
            return None
        
        # Take initial screenshot for comparison
        try:
            initial_screenshot = pyautogui.screenshot(region=ai["read_region"])
            initial_text = pytesseract.image_to_string(initial_screenshot).strip()
            logging.info(f"Initial text in region: '{initial_text[:50]}...'")
        except Exception as e:
            logging.warning(f"Initial OCR failed: {e}")
            initial_text = ""
        
        # Wall-clock timeout
        start_time = time.time()
        max_wall_time = 90  # Extended for longer responses like Kai's opening
        
        for attempt in range(MAX_RETRIES):
            # Check wall-clock timeout
            if time.time() - start_time > max_wall_time:
                logging.warning(f"Wall-clock timeout reached for {ai['name']}")
                break
                
            logging.info(f"OCR attempt {attempt + 1}/{MAX_RETRIES}")
            
            # Scroll if needed for long responses
            if ai['name'] in ["perplexity", "kai"]:  # Added Kai for long responses
                try:
                    scroll_coords = (ai["coords"][0], ai["coords"][1] - 200)
                    pyautogui.moveTo(scroll_coords[0], scroll_coords[1])
                    pyautogui.scroll(-3)
                    time.sleep(1)
                except Exception as e:
                    logging.warning(f"Scroll failed: {e}")
            
            try:
                screenshot = pyautogui.screenshot(region=ai["read_region"])
                text = pytesseract.image_to_string(screenshot).strip()
                ocr_failures = 0
                
                # Debug output every 5 attempts
                if attempt % 5 == 0:
                    logging.info(f"Current OCR text: '{text[:100]}...'")
                
                # Enhanced detection using response patterns
                if text and len(text) > len(initial_text) + 20:
                    if self.detect_response_patterns(text, ai['name']):
                        logging.info(f"Response pattern detected for {ai['name']}!")
                        
                        # Check if text is stable
                        if text == stable_text:
                            stable_count += 1
                            logging.info(f"Stable count: {stable_count}/3")
                            if stable_count >= 3:
                                logging.info(f"Response complete from {ai['name']}!")
                                logging.info(f"Full response ({len(text)} chars)")
                                time.sleep(3)
                                return text
                        else:
                            stable_text = text
                            stable_count = 0
                            logging.info(f"Response updating... ({len(text)} chars)")
                
                last_text = text
                time.sleep(3)  # Slightly longer intervals for stability
                
            except Exception as e:
                ocr_failures += 1
                logging.error(f"OCR error on attempt {attempt + 1}: {e}")
                
                if ocr_failures >= 5:
                    logging.error(f"Too many consecutive OCR failures for {ai['name']}, aborting")
                    break
                    
                time.sleep(2)
                continue
            
        logging.warning(f"Response timeout from {ai['name']}")
        if stable_text:
            logging.info(f"Returning last stable text ({len(stable_text)} chars)")
            return stable_text
        return None

    def print_loop_summary(self):
        """Print summary of last loop"""
        if not self.log:
            return
            
        recent_entries = self.log[-len(AI_ORDER):]
        successes = sum(1 for entry in recent_entries if entry.get('success', False))
        
        logging.info(f"LOOP SUMMARY: {successes}/{len(AI_ORDER)} AIs responded successfully")
        for entry in recent_entries:
            status = "✅" if entry.get('success', False) else "❌"
            logging.info(f"  {status} {entry['ai']}: {'Success' if entry.get('success', False) else 'Failed'}")

    def loop_once(self):
        """Execute one complete loop with the actual AI participants"""
        logging.info("Starting new circular loop with actual AI Council")
        
        for i in range(len(AI_ORDER)):
            ai = AI_ORDER[i]
            logging.info(f"Step {i+1}/{len(AI_ORDER)}: {ai['name'].upper()}")
            
            # Send message
            if not self.send_message(ai, self.last_message):
                logging.error(f"Failed to send message to {ai['name']}, using fallback")
                self.last_message = f"(Failed to communicate with previous AI)"
                log_entry = {
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": None,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": False,
                    "error": "Send failed"
                }
                self.log.append(log_entry)
                continue
            
            # Wait for response
            response = self.wait_for_response(ai)
            
            if response:
                # Use full response for next AI (your system handles long messages well)
                self.last_message = response
                log_entry = {
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": response,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": True
                }
            else:
                self.last_message = "(No clear reply from previous council member)"
                log_entry = {
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": None,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": False,
                    "error": "No response"
                }
            
            self.log.append(log_entry)
            
            # Longer pause between AIs for processing
            time.sleep(5)
        
        # Return to desktop 0 after loop
        self.switch_to_desktop(0)
        self.print_loop_summary()
        logging.info("Loop complete, returned to desktop 0")

    def save_log(self):
        """Save conversation log with timestamp"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_session_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.log, f, indent=2)
            
            logging.info(f"Log saved: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Failed to save log: {e}")
            return None

def main():
    """Main function for the actual AI Council system"""
    logging.info("Starting AI Council Circular Loop - Actual Participants")
    logging.info("Participants: Kai → Claude → Perplexity → Finn Harper")
    
    council = CircularCouncil()
    
    try:
        while True:
            council.loop_once()
            council.save_log()
            logging.info(f"Council session complete. Restarting in {LOOP_PAUSE} seconds")
            time.sleep(LOOP_PAUSE)
    except KeyboardInterrupt:
        logging.info("Stopping AI Council...")
        council.save_log()
        logging.info("Council session ended!")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        council.save_log()

if __name__ == "__main__":
    main()