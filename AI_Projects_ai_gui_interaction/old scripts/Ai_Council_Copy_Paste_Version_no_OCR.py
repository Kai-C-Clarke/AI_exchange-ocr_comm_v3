import time
import logging
import subprocess
import pyautogui
import pyperclip
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Your working UI coordinates - unchanged
BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_coords": (300, 990),
        "send_button": (887, 1020),
        "safe_click": (200, 500),
        "copy_region": (202, 250, 900, 800),  # Region to select for copying response
        "desktop": 1
    },
    "CLAUDE": {
        "input_coords": (1530, 994),
        "send_button": (1909, 1035),
        "safe_click": (1136, 904),
        "copy_region": (1190, 250, 1909, 800),  # Claude's response area
        "desktop": 1
    },
    "Perplexity": {
        "input_coords": (400, 1010),
        "send_button": (911, 1022),
        "safe_click": (200, 500),
        "copy_region": (190, 200, 949, 600),  # Perplexity's response area
        "desktop": 2
    },
    "Grok": {
        "input_coords": (1450, 990),
        "send_button": (1922, 1034),
        "safe_click": (1450, 500),
        "copy_region": (1248, 250, 1946, 800),  # Grok's response area
        "desktop": 2
    }
}

# Track current desktop - unchanged from your working version
current_desktop = 0

def kai_desktop_switch(target_desktop):
    """EXACT COPY FROM WORKING VERSION - DON'T CHANGE!"""
    global current_desktop
    
    if current_desktop == target_desktop:
        logging.info(f"✅ Already on Desktop {target_desktop}, no switch needed")
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
        else:  # from desktop 1 to 2
            script = '''
            tell application "System Events"
                key code 124 using control down
            end tell
            '''
    else:  # Desktop 0
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

def kai_smart_desktop_switch(speaker):
    """Smart desktop switching - unchanged"""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    logging.info(f"🎯 {speaker} needs Desktop {target_desktop}")
    kai_desktop_switch(target_desktop)

def kai_clipboard_injection(message):
    """Your working clipboard method - unchanged"""
    logging.info(f"📋 Setting clipboard: '{message[:40]}...'")
    
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info("✅ Clipboard set successfully")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_safe_click(ui):
    """Your working safe click method - unchanged"""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    logging.info(f"🖱️ Safe click for {ui} at {coords}")
    pyautogui.click(coords[0], coords[1])
    time.sleep(1)

def kai_text_injection(message, ui):
    """Your working text injection method - unchanged"""
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

def kai_copy_response(speaker):
    """NEW: Copy AI response directly instead of OCR"""
    logging.info(f"📋 Copying {speaker}'s response directly...")
    
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    copy_region = config["copy_region"]
    
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
        # Method 1: Triple-click to select response area and copy
        logging.info(f"🖱️ Triple-clicking in {speaker}'s response area")
        center_x = (copy_region[0] + copy_region[2]) // 2
        center_y = (copy_region[1] + copy_region[3]) // 2
        
        # Click in the center of the response area
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)
        
        # Triple-click to select text (or use drag selection)
        pyautogui.click(center_x, center_y, clicks=3)
        time.sleep(0.5)
        
        # Copy selected text
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        # Get the copied text
        copied_text = pyperclip.paste()
        
        if copied_text and len(copied_text.strip()) > 10:
            # Clean up the response
            cleaned_response = clean_copied_response(copied_text)
            logging.info(f"✅ Copied {len(cleaned_response)} chars from {speaker}: '{cleaned_response[:60]}...'")
            return cleaned_response
        else:
            logging.warning(f"⚠️ {speaker}'s copied text too short, trying drag selection")
            return kai_drag_copy_response(speaker, copy_region)
            
    except Exception as e:
        logging.error(f"❌ Copy failed for {speaker}: {e}")
        return None

def kai_drag_copy_response(speaker, copy_region):
    """Alternative: Drag to select response area and copy"""
    logging.info(f"🖱️ Trying drag selection for {speaker}")
    
    try:
        # Drag from top-left to bottom-right of response area
        start_x, start_y = copy_region[0] + 10, copy_region[1] + 10
        end_x, end_y = copy_region[2] - 10, copy_region[3] - 10
        
        # Drag to select
        pyautogui.drag(start_x, start_y, end_x - start_x, end_y - start_y, duration=1)
        time.sleep(0.5)
        
        # Copy selected text
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        # Get the copied text
        copied_text = pyperclip.paste()
        
        if copied_text and len(copied_text.strip()) > 10:
            cleaned_response = clean_copied_response(copied_text)
            logging.info(f"✅ Drag-copied from {speaker}: '{cleaned_response[:60]}...'")
            return cleaned_response
        else:
            logging.warning(f"⚠️ Drag selection failed for {speaker}")
            return None
            
    except Exception as e:
        logging.error(f"❌ Drag copy failed for {speaker}: {e}")
        return None

def clean_copied_response(raw_text):
    """Clean copied text to extract just the AI's response"""
    lines = raw_text.strip().split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip timestamp lines, UI elements, etc.
        if line.startswith('[') and line.endswith(']'):
            continue
        if 'Send message' in line:
            continue
        if 'Copy' in line and len(line) < 10:
            continue
        if line in ['•', '○', '▪', '►']:
            continue
            
        cleaned_lines.append(line)
    
    # Join and limit length
    result = ' '.join(cleaned_lines)
    if len(result) > 500:
        result = result[:500] + "..."
    
    return result

def get_fallback_prompt(exchange_count):
    """Fallback prompts when copy fails"""
    fallbacks = [
        "What aspects of AI collaboration interest you most?",
        "How do you view the nature of artificial consciousness?", 
        "What ethical considerations guide AI interactions?",
        "What questions about intelligence intrigue you?",
        "How might AI minds contribute to human understanding?"
    ]
    return fallbacks[exchange_count % len(fallbacks)]

def kai_brief_test():
    """Brief Kai about the experiment - unchanged"""
    logging.info("📢 Briefing Kai...")
    
    kai_smart_desktop_switch("Kai")
    kai_safe_click("Kai")
    
    brief = "Kai - Four-AI Council copy/paste discourse starting. Please respond naturally to begin the conversation."
    success = kai_text_injection(brief, "Kai")
    
    if success:
        logging.info("✅ Kai briefed successfully")
        time.sleep(5)
    
    return success

def kai_four_ai_copy_paste_conversation():
    """FIXED: Proper chain conversation - each AI responds to the previous"""
    logging.info("🔗 Starting CHAIN conversation: Kai→Claude→Perplexity→Finn→Kai")
    
    # Define the proper chain sequence
    ai_chain = ["Kai", "CLAUDE", "Perplexity", "Grok"]  # Using "Grok" to match your config
    
    # Start with initial prompt ONLY to Kai
    initial_prompt = "Kai, please begin our four-AI council discussion. What topic shall we explore together?"
    current_message = initial_prompt
    
    for round_num in range(2):  # 2 full chain cycles
        logging.info(f"\n🔗 CHAIN ROUND {round_num + 1}")
        
        for step, ai_name in enumerate(ai_chain):
            logging.info(f"\n📍 Step {step + 1}/4: {ai_name}")
            
            # Switch to this AI's desktop
            kai_smart_desktop_switch(ai_name)
            kai_safe_click(ai_name)
            
            # Add timestamp to message
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {current_message}"
            
            # Send the message to this AI
            logging.info(f"💬 Sending to {ai_name}: '{current_message[:60]}...'")
            success = kai_text_injection(formatted_message, ai_name)
            
            if not success:
                logging.error(f"❌ Failed to send to {ai_name}")
                current_message = get_fallback_prompt(step)
                continue
            
            # Wait for this AI to respond, then copy their response
            logging.info(f"⏳ Waiting for {ai_name} to respond...")
            response = kai_copy_response(ai_name)
            
            if response:
                # This AI's response becomes the message for the NEXT AI
                current_message = response
                logging.info(f"✅ Got response from {ai_name}, will send to next AI")
                logging.info(f"📝 Response preview: '{response[:80]}...'")
            else:
                # If copy failed, use a connecting fallback
                current_message = f"Please continue the discussion that {ai_name} was having about AI collaboration."
                logging.warning(f"⚠️ Copy failed from {ai_name}, using connecting fallback")
            
            # Brief pause between chain steps
            time.sleep(3)
        
        logging.info(f"✅ Chain round {round_num + 1} complete")
        time.sleep(5)  # Pause between rounds
    
    return True

def kai_return_home():
    """Return to Desktop 0 - unchanged"""
    logging.info("🏠 Returning home...")
    kai_desktop_switch(0)

def kai_main():
    """Main function with copy/paste conversation"""
    
    logging.info("⚔️ KAI'S COPY/PASTE SOLUTION ⚔️")
    logging.info("📋 pbcopy + Direct Copy/Paste + No OCR!")
    logging.info("🤖 Four AIs will have REAL conversation using copy/paste!")
    
    try:
        # Step 1: Brief Kai
        if not kai_brief_test():
            logging.error("❌ Briefing failed")
            return
        
        # Step 2: Four-AI chain conversation with copy/paste
        if not kai_four_ai_copy_paste_conversation():
            logging.error("❌ Four-AI conversation failed")
            return
            
        logging.info("✅ CHAIN FOUR-AI CONVERSATION COMPLETED!")
        
    except Exception as e:
        logging.error(f"💥 Error: {e}")
    
    finally:
        kai_return_home()

if __name__ == "__main__":
    logging.info("🚀 FOUR-AI COUNCIL COPY/PASTE SOLUTION")
    logging.info("🎯 No OCR + Direct text copying + Much more reliable!")
    
    # 5 second countdown
    for i in range(5, 0, -1):
        logging.info(f"⏰ Starting in {i}...")
        time.sleep(1)
    
    kai_main()