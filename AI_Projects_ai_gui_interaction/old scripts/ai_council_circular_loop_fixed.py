#!/usr/bin/env python3
"""
AI Council Circular Loop – PROPERLY INDENTED VERSION
Based on Perplexity's second code review
Kai → Claude → Perplexity → Grok → Kai ...
"""

import time
import pyautogui
import pytesseract
import subprocess
import pyperclip
import logging
import json

# Configure logging as suggested by Perplexity
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define each AI and its settings - FIXED closing bracket
AI_ORDER = [
    {"name": "kai", "desktop": 1, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "claude", "desktop": 1, "coords": (1200, 960), "read_region": (900, 150, 1400, 600), "typing_method": "applescript"},
    {"name": "perplexity", "desktop": 2, "coords": (456, 960), "read_region": (400, 150, 700, 600), "typing_method": "applescript"},
    {"name": "grok", "desktop": 2, "coords": (1548, 1000), "read_region": (1200, 150, 1800, 600), "typing_method": "clipboard"}
]

# Configuration constants
WAIT_SECONDS = 12
MAX_RETRIES = 20
LOOP_PAUSE = 15

class CircularCouncil:
    def __init__(self):
        self.log = []
        self.last_message = "Hello, this is the AI Council. Please begin the discussion."
        self.current_desktop = 0
        logging.info("CircularCouncil initialized")

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
            escaped_text = text.replace('"', '\\"').replace('\\', '\\\\')
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
        """Clipboard paste with error handling"""
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
        """Clear field with verification - added delete as suggested"""
        try:
            pyautogui.hotkey("command", "a")
            time.sleep(0.2)
            pyautogui.press("delete")  # Added as suggested by Perplexity
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

    def wait_for_response(self, ai):
        """Wait for response with wall-clock timeout as suggested"""
        logging.info(f"Waiting for {ai['name']}'s reply on desktop {ai['desktop']}")
        logging.info(f"OCR region: {ai['read_region']}")
        
        last_text = ""
        stable_text = ""
        stable_count = 0
        ocr_failures = 0  # Counter for consecutive OCR failures
        
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
        
        # Wall-clock timeout as suggested by Perplexity
        start_time = time.time()
        max_wall_time = 60  # 60 seconds maximum
        
        for attempt in range(MAX_RETRIES):
            # Check wall-clock timeout
            if time.time() - start_time > max_wall_time:
                logging.warning(f"Wall-clock timeout reached for {ai['name']}")
                break
                
            logging.info(f"OCR attempt {attempt + 1}/{MAX_RETRIES}")
            
            # Scroll if needed for long responses
            if ai['name'] in ["perplexity"]:
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
                ocr_failures = 0  # Reset failure counter on success
                
                # Debug: Show what we're seeing periodically
                if attempt % 5 == 0:
                    logging.info(f"Current OCR text: '{text[:50]}...'")
                
                # Check for significant change from initial
                if text and text != initial_text and len(text) > len(initial_text) + 10:
                    logging.info(f"Text growth detected! From {len(initial_text)} to {len(text)} chars")
                    
                    # Check if text is stable (response finished)
                    if text == stable_text:
                        stable_count += 1
                        logging.info(f"Stable count: {stable_count}/3")
                        if stable_count >= 3:
                            logging.info(f"Response complete from {ai['name']}!")
                            logging.info(f"Full response ({len(text)} chars): {text[:200]}...")
                            time.sleep(3)
                            return text
                    else:
                        stable_text = text
                        stable_count = 0
                        logging.info(f"Response updating... ({len(text)} chars)")
                
                last_text = text
                time.sleep(2)
                
            except Exception as e:
                ocr_failures += 1
                logging.error(f"OCR error on attempt {attempt + 1}: {e}")
                
                # Early abort on consecutive OCR failures as suggested
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
        """Print summary of last loop as suggested by Perplexity"""
        if not self.log:
            return
            
        recent_entries = self.log[-len(AI_ORDER):]
        successes = sum(1 for entry in recent_entries if entry.get('success', False))
        
        logging.info(f"LOOP SUMMARY: {successes}/{len(AI_ORDER)} AIs responded successfully")
        for entry in recent_entries:
            status = "✅" if entry.get('success', False) else "❌"
            logging.info(f"  {status} {entry['ai']}: {'Success' if entry.get('success', False) else 'Failed'}")

    def loop_once(self):
        """Execute one complete loop with failure recovery"""
        logging.info("Starting new circular loop")
        
        for i in range(len(AI_ORDER)):
            ai = AI_ORDER[i]
            logging.info(f"Step {i+1}/{len(AI_ORDER)}: {ai['name'].upper()}")
            
            # Send message with retry on failure
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
                # Truncate very long responses
                self.last_message = response[:1000] if len(response) > 1000 else response
                log_entry = {
                    "step": i+1,
                    "ai": ai["name"], 
                    "desktop": ai["desktop"],
                    "message": response,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": True
                }
            else:
                self.last_message = "(No clear reply)"
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
        
        # Return to desktop 0 after loop
        self.switch_to_desktop(0)
        
        # Print summary as suggested
        self.print_loop_summary()
        logging.info("Loop complete, returned to desktop 0")

    def save_log(self):
        """Save conversation log to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ai_council_circular_log_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.log, f, indent=2)
            
            logging.info(f"Log saved: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Failed to save log: {e}")
            return None

def main():
    """Main function with improved error handling"""
    logging.info("Starting AI Council Circular Loop")
    
    council = CircularCouncil()
    
    try:
        while True:
            council.loop_once()
            # Save log after each loop as suggested by Perplexity
            council.save_log()
            logging.info(f"Council loop complete. Restarting in {LOOP_PAUSE} seconds")
            time.sleep(LOOP_PAUSE)
    except KeyboardInterrupt:
        logging.info("Stopping circular council...")
        council.save_log()
        logging.info("Session ended!")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        council.save_log()

if __name__ == "__main__":
    main()