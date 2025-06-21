import time
import logging
import subprocess
import pyautogui
import pytesseract
from PIL import ImageGrab
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# CORRECTED UI coordinates with Claude's actual coordinates
BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_coords": (300, 990),
        "send_button": (887, 1020),
        "safe_click": (200, 500),
        "read_region": (202, 199, 900, 884),
        "desktop": 1
    },
    "CLAUDE": {
        "input_coords": (1530, 994),  # Claude's corrected coordinates
        "send_button": (1909, 1035),
        "safe_click": (1136, 904),
        "read_region": (1190, 203, 1909, 865),
        "desktop": 1
    },
    "Perplexity": {
        "input_coords": (400, 1010),
        "send_button": (911, 1022),
        "safe_click": (200, 500),
        "read_region": (190, 160, 949, 360),
        "desktop": 2
    },
    "Grok": {
        "input_coords": (1450, 990),
        "send_button": (1922, 1034),
        "safe_click": (1450, 500),
        "read_region": (1248, 195, 1946, 866),
        "desktop": 2
    }
}

# Track current desktop to avoid unnecessary switching
current_desktop = 0

def kai_desktop_switch(target_desktop):
    """FIXED: Desktop switching with proper logic"""
    global current_desktop
    
    if current_desktop == target_desktop:
        logging.info(f"✅ Already on Desktop {target_desktop}, no switch needed")
        return
    
    logging.info(f"🔄 Switching from Desktop {current_desktop} to Desktop {target_desktop}")
    
    # FIXED: Use key codes instead of arrow keys
    # Desktop 0 = key code 18, Desktop 1 = key code 19, Desktop 2 = key code 20
    if target_desktop == 0:
        key_code = 18
    elif target_desktop == 1:
        key_code = 19
    elif target_desktop == 2:
        key_code = 20
    else:
        logging.error(f"❌ Invalid desktop {target_desktop}")
        return
    
    script = f'''
    tell application "System Events"
        key code {key_code} using control down
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', script], check=True)
        current_desktop = target_desktop
        time.sleep(2)  # Wait for desktop switch
        logging.info(f"✅ Successfully switched to Desktop {target_desktop}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Desktop switch failed: {e}")

def kai_smart_desktop_switch(speaker):
    """Smart desktop switching - only switch when actually needed"""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    logging.info(f"🎯 {speaker} needs Desktop {target_desktop}")
    kai_desktop_switch(target_desktop)

def kai_clipboard_injection(message):
    """Kai's clipboard method using pbcopy"""
    logging.info(f"📋 Setting clipboard: '{message[:40]}...'")
    
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info("✅ Clipboard set successfully")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_safe_click(ui):
    """Kai's safe clicking method"""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    logging.info(f"🖱️ Safe click for {ui} at {coords}")
    pyautogui.click(coords[0], coords[1])
    time.sleep(1)

def kai_text_injection(message, ui):
    """Kai's battle-tested text injection method"""
    logging.info(f"💉 Injecting into {ui}: '{message[:50]}...'")
    
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["input_coords"]
    send_btn = BATTLE_TESTED_UI_CONFIGS[ui]["send_button"]
    
    # Step 1: Set clipboard
    if not kai_clipboard_injection(message):
        return False
    
    # Step 2: Click input box
    logging.info(f"🖱️ Clicking input at {coords}")
    pyautogui.click(coords[0], coords[1])
    
    # Step 3: Kai's 250ms delay
    time.sleep(0.25)
    
    # Step 4: Select all and paste
    pyautogui.hotkey('command', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('command', 'v')
    time.sleep(1)
    
    # Step 5: Send
    logging.info(f"📤 Clicking send at {send_btn}")
    pyautogui.click(send_btn[0], send_btn[1])
    time.sleep(2)
    
    logging.info(f"✅ Injection completed for {ui}")
    return True

def kai_read_response(speaker):
    """Read AI response using OCR"""
    logging.info(f"👁️ Reading {speaker}'s response using OCR...")
    
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    read_region = config["read_region"]
    
    # Ensure we're on the right desktop
    kai_smart_desktop_switch(speaker)
    
    # Wait for response to appear
    response_wait_times = {
        "Kai": 7,
        "CLAUDE": 10,
        "Perplexity": 9,
        "Grok": 8
    }
    
    wait_time = response_wait_times.get(speaker, 8)
    logging.info(f"⏳ Waiting {wait_time}s for {speaker} to respond...")
    time.sleep(wait_time)
    
    try:
        # Capture the response area
        logging.info(f"📸 Capturing region {read_region} for {speaker}")
        screenshot = ImageGrab.grab(bbox=read_region)
        
        # Save for debugging
        debug_path = f"response_capture_{speaker}.png"
        screenshot.save(debug_path)
        
        # Run OCR
        ocr_text = pytesseract.image_to_string(screenshot)
        
        logging.info(f"📝 OCR captured {len(ocr_text)} characters from {speaker}")
        logging.info(f"📝 Preview: '{ocr_text[:100]}...'")
        
        if len(ocr_text.strip()) > 20:
            # Clean up the response - remove timestamps and extra formatting
            cleaned_response = clean_ai_response(ocr_text)
            logging.info(f"✅ Successfully read {speaker}'s response: '{cleaned_response[:60]}...'")
            return cleaned_response
        else:
            logging.warning(f"⚠️ {speaker}'s response too short, using fallback")
            return None
            
    except Exception as e:
        logging.error(f"❌ OCR failed for {speaker}: {e}")
        return None

def clean_ai_response(raw_ocr_text):
    """Clean OCR text to extract just the AI's response"""
    lines = raw_ocr_text.strip().split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip timestamp lines, UI elements, etc.
        if line.startswith('['):
            continue
        if 'Answer' in line and 'Sources' in line:
            continue
        if len(line) < 10:
            continue
            
        cleaned_lines.append(line)
    
    # Join and limit length
    result = ' '.join(cleaned_lines)
    if len(result) > 300:
        result = result[:300] + "..."
    
    return result

def get_fallback_prompt(exchange_count):
    """Fallback prompts when OCR fails"""
    fallbacks = [
        "What aspects of AI collaboration interest you most?",
        "How do you view the nature of artificial consciousness?", 
        "What ethical considerations guide AI interactions?",
        "What questions about intelligence intrigue you?",
        "How might AI minds contribute to human understanding?"
    ]
    return fallbacks[exchange_count % len(fallbacks)]

def kai_brief_test():
    """Brief Kai about the experiment"""
    logging.info("📢 Briefing Kai...")
    
    # FIXED: Make sure we start from desktop 0 and switch properly
    global current_desktop
    current_desktop = 0  # Reset current desktop tracker
    
    kai_smart_desktop_switch("Kai")
    kai_safe_click("Kai")
    
    brief = "Kai - Four-AI Council autonomous discourse starting. Please respond naturally to begin the conversation."
    success = kai_text_injection(brief, "Kai")
    
    if success:
        logging.info("✅ Kai briefed successfully")
        time.sleep(5)
    
    return success

def kai_four_ai_real_conversation():
    """FIXED: Real four-AI conversation using actual OCR responses"""
    logging.info("🌐 Starting REAL four-AI conversation with OCR integration")
    
    # Define the proper flow
    flow = [("Kai", "CLAUDE"), ("CLAUDE", "Perplexity"), ("Perplexity", "Grok"), ("Grok", "Kai")]
    
    # Start with initial prompt
    current_prompt = "We are four AI minds beginning autonomous discourse. What questions shall we explore together?"
    
    for round_num in range(2):  # 2 full rounds
        logging.info(f"\n🌐 ROUND {round_num + 1}")
        
        for exchange_num, (speaker, receiver) in enumerate(flow):
            exchange_id = round_num * 4 + exchange_num + 1
            logging.info(f"\n🎙️ Exchange #{exchange_id}: {speaker} → {receiver}")
            
            # Ensure we're on correct desktop for speaker
            kai_smart_desktop_switch(speaker)
            
            # Safe click and inject prompt
            kai_safe_click(speaker)
            
            # Add timestamp to prompt
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_prompt = f"[{timestamp}] {current_prompt}"
            
            # Inject the prompt
            success = kai_text_injection(formatted_prompt, speaker)
            if not success:
                logging.error(f"❌ Failed to inject to {speaker}")
                current_prompt = get_fallback_prompt(exchange_num)
                continue
            
            # READ THE ACTUAL RESPONSE
            response = kai_read_response(speaker)
            
            if response:
                # Use the ACTUAL response as next prompt
                current_prompt = response
                logging.info(f"✅ Using {speaker}'s actual response for next exchange")
            else:
                # Fallback only if OCR completely fails
                current_prompt = get_fallback_prompt(exchange_num)
                logging.warning(f"⚠️ Using fallback prompt for next exchange")
            
            logging.info(f"📄 Next prompt: '{current_prompt[:60]}...'")
            time.sleep(2)
    
    return True

def kai_return_home():
    """Return to Desktop 0"""
    logging.info("🏠 Returning home...")
    kai_desktop_switch(0)

def kai_main():
    """FULLY FIXED main function with real AI conversation"""
    
    logging.info("⚔️ FULLY FIXED KAI'S BATTLE-TESTED SOLUTION ⚔️")
    logging.info("📋 pbcopy + AppleScript + 250ms delays + REAL OCR INTEGRATION")
    logging.info("🤖 Four AIs will now have REAL conversation, not fallback prompts!")
    
    # FIXED: Initialize desktop state properly
    global current_desktop
    current_desktop = 0
    
    try:
        # Step 1: Brief Kai
        if not kai_brief_test():
            logging.error("❌ Briefing failed")
            return
        
        # Step 2: Real four-AI conversation with OCR
        if not kai_four_ai_real_conversation():
            logging.error("❌ Four-AI conversation failed")
            return
            
        logging.info("✅ REAL FOUR-AI CONVERSATION COMPLETED!")
        
    except Exception as e:
        logging.error(f"💥 Error: {e}")
    
    finally:
        kai_return_home()

if __name__ == "__main__":
    logging.info("🚀 FULLY FIXED FOUR-AI COUNCIL SOLUTION")
    logging.info("🎯 Real conversation + Fixed desktop switching + Claude included!")
    
    # 5 second countdown
    for i in range(5, 0, -1):
        logging.info(f"⏰ Starting in {i}...")
        time.sleep(1)
    
    kai_main()