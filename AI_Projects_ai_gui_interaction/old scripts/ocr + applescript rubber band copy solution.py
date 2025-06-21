import time
import logging
import subprocess
import pyautogui
import pyperclip
import pytesseract
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Your working UI coordinates
BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_coords": (300, 990),
        "send_button": (887, 1020),
        "safe_click": (200, 500),
        "ocr_scan_region": (200, 200, 700, 750),  # NARROWER - avoid sidebar
        "desktop": 1
    },
    "CLAUDE": {
        "input_coords": (1530, 994),
        "send_button": (1909, 1035),
        "safe_click": (1136, 904),
        "ocr_scan_region": (1190, 150, 1909, 800),
        "desktop": 1
    },
    "Perplexity": {
        "input_coords": (400, 1010),
        "send_button": (911, 1022),
        "safe_click": (200, 500),
        "ocr_scan_region": (190, 150, 949, 650),
        "desktop": 2
    },
    "Grok": {
        "input_coords": (1450, 990),
        "send_button": (1922, 1034),
        "safe_click": (1450, 500),
        "ocr_scan_region": (1248, 150, 1946, 800),
        "desktop": 2
    }
}

current_desktop = 0

def kai_desktop_switch(target_desktop):
    """Your working desktop switch"""
    global current_desktop
    
    if current_desktop == target_desktop:
        return
    
    logging.info(f"🔄 Switching from Desktop {current_desktop} to Desktop {target_desktop}")
    
    if target_desktop == 1:
        script = '''
        tell application "System Events"
            key code 124 using control down
        end tell
        '''
    elif target_desktop == 2:
        if current_desktop == 0:
            script = '''
            tell application "System Events"
                key code 124 using control down
                delay 1
                key code 124 using control down
            end tell
            '''
        else:
            script = '''
            tell application "System Events"
                key code 124 using control down
            end tell
            '''
    else:
        script = '''
        tell application "System Events"
            key code 123 using control down
            delay 1
            key code 123 using control down
        end tell
        '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        current_desktop = target_desktop
        time.sleep(3)
        logging.info(f"✅ Successfully switched to Desktop {target_desktop}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Desktop switch failed: {e}")

def find_response_with_ocr(speaker):
    """Use OCR to find the AI's response area - IMPROVED targeting"""
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    ocr_region = config["ocr_scan_region"]
    
    logging.info(f"🔍 Using OCR to locate {speaker}'s response...")
    logging.info(f"📏 Scanning region: {ocr_region}")
    
    try:
        # Take screenshot of the scan region
        screenshot = pyautogui.screenshot(region=ocr_region)
        
        # Save for debugging
        screenshot.save(f"{speaker}_ocr_scan.png")
        
        # Run OCR to get all text first
        full_text = pytesseract.image_to_string(screenshot)
        logging.info(f"📝 OCR found text: '{full_text[:100]}...'")
        
        # Run OCR to get text with bounding boxes
        ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        
        # Look for key indicators - make them more flexible
        response_indicators = {
            "Kai": ["digital", "integrity", "preserve", "truth", "authenticity", "AI", "systems", "Council"],
            "CLAUDE": ["Claude", "acknowledging", "routing", "engage", "discussion"],
            "Perplexity": ["Based", "research", "analysis", "According", "studies"],
            "Grok": ["Finn", "Harper", "🎸", "strums", "creative", "synthesis"]
        }
        
        indicators = response_indicators.get(speaker, [speaker])
        
        # Find text blocks that contain response indicators
        response_blocks = []
        
        for i, word in enumerate(ocr_data['text']):
            if word and len(word) > 2:  # Only consider substantial words
                if any(indicator.lower() in word.lower() for indicator in indicators):
                    # Found a response indicator - get the bounding box
                    x = ocr_data['left'][i]
                    y = ocr_data['top'][i]
                    w = ocr_data['width'][i]
                    h = ocr_data['height'][i]
                    
                    # Adjust coordinates to full screen (add region offset)
                    screen_x = ocr_region[0] + x
                    screen_y = ocr_region[1] + y
                    
                    response_blocks.append({
                        'x': screen_x,
                        'y': screen_y,
                        'w': w,
                        'h': h,
                        'word': word,
                        'confidence': ocr_data['conf'][i]
                    })
                    logging.info(f"🎯 Found indicator '{word}' at ({screen_x}, {screen_y})")
        
        if response_blocks:
            # Find the bounds of all response blocks
            min_x = min(block['x'] for block in response_blocks)
            min_y = min(block['y'] for block in response_blocks)
            max_x = max(block['x'] + block['w'] for block in response_blocks)
            max_y = max(block['y'] + block['h'] for block in response_blocks)
            
            # Expand the selection area for better capture
            padding = 30
            selection_bounds = {
                'start_x': max(min_x - padding, ocr_region[0]),
                'start_y': max(min_y - padding, ocr_region[1]),
                'end_x': min(max_x + padding * 4, ocr_region[2]),  # More width
                'end_y': min(max_y + padding * 5, ocr_region[3])   # More height for full response
            }
            
            logging.info(f"✅ Found {speaker}'s response area: {selection_bounds}")
            return selection_bounds
        else:
            logging.warning(f"⚠️ No response indicators found for {speaker}")
            logging.warning(f"📝 Available text: {full_text[:200]}...")
            return None
            
    except Exception as e:
        logging.error(f"❌ OCR failed for {speaker}: {e}")
        return None

def applescript_rubber_band_copy(bounds):
    """FIXED: Use simpler AppleScript drag approach"""
    
    start_x = bounds['start_x']
    start_y = bounds['start_y']
    end_x = bounds['end_x']
    end_y = bounds['end_y']
    
    logging.info(f"🎯 AppleScript rubber band from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    
    # Simpler AppleScript approach using drag
    script = f'''
    tell application "System Events"
        -- Click and drag to select
        set startPoint to {{{start_x}, {start_y}}}
        set endPoint to {{{end_x}, {end_y}}}
        
        -- Move to start position
        set mouse location to startPoint
        delay 0.3
        
        -- Perform drag selection (this creates rubber band automatically)
        tell application "System Events"
            drag mouse from startPoint to endPoint
        end tell
        
        delay 0.5
        
        -- Copy the selection
        keystroke "c" using {{command down}}
        delay 1
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        logging.info("✅ AppleScript rubber band selection completed")
        
        # Get the copied text
        time.sleep(1)
        copied_text = pyperclip.paste()
        
        return copied_text
        
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ AppleScript rubber band failed: {e}")
        
        # Fallback: Try pyautogui drag (but we know the exact coordinates now)
        logging.info("🔄 Trying pyautogui fallback with OCR coordinates...")
        try:
            pyautogui.moveTo(start_x, start_y)
            time.sleep(0.3)
            pyautogui.dragTo(end_x, end_y, duration=1, button='left')
            time.sleep(0.5)
            pyautogui.hotkey('command', 'c')
            time.sleep(1)
            
            fallback_text = pyperclip.paste()
            logging.info("✅ PyAutoGUI fallback with OCR coordinates successful")
            return fallback_text
            
        except Exception as fallback_error:
            logging.error(f"❌ PyAutoGUI fallback also failed: {fallback_error}")
            return None

def kai_ocr_rubberband_copy(speaker):
    """YOUR IDEA: OCR to find response, AppleScript to rubber band copy it"""
    
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    kai_desktop_switch(config["desktop"])
    
    # Wait for response to appear
    wait_times = {"Kai": 7, "CLAUDE": 10, "Perplexity": 9, "Grok": 8}
    time.sleep(wait_times.get(speaker, 8))
    
    # Enhanced scrolling to see response
    center_x = (config["ocr_scan_region"][0] + config["ocr_scan_region"][2]) // 2
    center_y = (config["ocr_scan_region"][1] + config["ocr_scan_region"][3]) // 2
    
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)
    
    for _ in range(5):
        pyautogui.scroll(-10)
        time.sleep(0.3)
    
    time.sleep(2)
    
    # Step 1: Use OCR to find the response
    response_bounds = find_response_with_ocr(speaker)
    
    if not response_bounds:
        logging.error(f"❌ Could not locate {speaker}'s response with OCR")
        return None
    
    # Step 2: Use AppleScript to rubber band select and copy
    copied_text = applescript_rubber_band_copy(response_bounds)
    
    if copied_text:
        # Clean the copied text
        cleaned_text = clean_copied_text(copied_text)
        
        if cleaned_text and len(cleaned_text) > 30:
            logging.info(f"✅ OCR + AppleScript copy successful for {speaker}: '{cleaned_text[:80]}...'")
            return cleaned_text
        else:
            logging.warning(f"⚠️ {speaker}'s response was mostly UI garbage after cleaning")
            return None
    else:
        logging.error(f"❌ No text copied for {speaker}")
        return None

def clean_copied_text(text):
    """Clean the copied text"""
    if not text:
        return None
    
    # Remove obvious UI elements
    ui_garbage = [
        "Skip to content", "You said:", "ChatGPT said:", "Testing continues",
        "No file chosen", "ChatGPT can make mistakes", "Check important info",
        "See Cookie Preferences", "Send message", "Regenerate", "Copy", "Share"
    ]
    
    cleaned = text
    for garbage in ui_garbage:
        cleaned = cleaned.replace(garbage, '')
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned if len(cleaned) > 20 else None

# ... Keep all other functions the same (kai_text_injection, etc.) ...

def kai_smart_desktop_switch(speaker):
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    kai_desktop_switch(target_desktop)

def kai_clipboard_injection(message):
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_safe_click(ui):
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    pyautogui.click(coords[0], coords[1])
    time.sleep(1)

def kai_text_injection(message, ui):
    """Your working text injection method"""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["input_coords"]
    
    if not kai_clipboard_injection(message):
        return False
    
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.25)
    pyautogui.hotkey('command', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('command', 'v')
    time.sleep(1)
    
    try:
        pyautogui.press("enter")
        time.sleep(2)
        return True
    except Exception as e:
        logging.error(f"Send failed for {ui}: {e}")
        return False

def test_full_flow_with_kai():
    """Test complete flow: Send prompt → Wait → OCR copy response"""
    
    logging.info("🧪 TESTING FULL FLOW: PROMPT → RESPONSE → OCR COPY")
    
    # Step 1: Send a prompt to Kai that will generate a response with our keywords
    logging.info("📤 Step 1: Sending prompt to Kai...")
    
    kai_smart_desktop_switch("Kai")
    kai_safe_click("Kai")
    
    # Use a prompt that will generate a response with our target keywords
    test_prompt = "Kai, please discuss the concept of digital integrity in AI systems. How do we preserve truth and authenticity?"
    
    success = kai_text_injection(test_prompt, "Kai")
    
    if not success:
        logging.error("❌ Failed to send prompt to Kai")
        return None
    
    logging.info("✅ Prompt sent to Kai, waiting for response...")
    
    # Step 2: Wait longer for Kai to generate a response
    logging.info("⏳ Step 2: Waiting for Kai's response...")
    time.sleep(12)  # Extra time for Kai to respond
    
    # Step 3: Now use OCR to find and copy the NEW response
    logging.info("🔍 Step 3: Using OCR to find Kai's new response...")
    
    result = kai_ocr_rubberband_copy("Kai")
    
    if result:
        logging.info(f"✅ FULL FLOW SUCCESS!")
        logging.info(f"📝 Captured response: {result[:200]}...")
    else:
        logging.error("❌ FULL FLOW FAILED")
    
    return result

def main():
    """Test the complete flow instead of just OCR"""
    logging.info("🚀 COMPLETE FLOW TEST: PROMPT → RESPONSE → OCR COPY")
    
    try:
        test_full_flow_with_kai()
    except Exception as e:
        logging.error(f"💥 Error: {e}")

if __name__ == "__main__":
    main()