import time
import logging
import subprocess
import pyautogui
import pyperclip
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Your working UI coordinates - DOUBLE CHECK THESE!
BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_coords": (300, 990),
        "send_button": (887, 1020),  # Verify this coordinate!
        "safe_click": (200, 500),
        "copy_region": (202, 250, 900, 800),
        "desktop": 1
    },
    "CLAUDE": {
        "input_coords": (1530, 994),
        "send_button": (1909, 1035),  # Verify this coordinate!
        "safe_click": (1136, 904),
        "copy_region": (1190, 250, 1909, 800),
        "desktop": 1
    },
    "Perplexity": {
        "input_coords": (400, 1010),
        "send_button": (911, 1022),  # Verify this coordinate!
        "safe_click": (200, 500),
        "copy_region": (190, 200, 949, 600),
        "desktop": 2
    },
    "Grok": {
        "input_coords": (1450, 990),
        "send_button": (1922, 1034),  # Verify this coordinate!
        "safe_click": (1450, 500),
        "copy_region": (1248, 250, 1946, 800),
        "desktop": 2
    }
}

# Track current desktop
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
    """Smart desktop switching - only switch when actually needed"""
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
    """FIXED: Your working text injection method with better send mechanism"""
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
    
    # Step 5: FIXED - Better send mechanism
    logging.info(f"📤 Attempting to send message...")
    
    # Method 1: Try Enter key first (most reliable)
    try:
        pyautogui.press("enter")
        time.sleep(1)
        logging.info("✅ Sent via Enter key")
    except Exception as e:
        logging.warning(f"Enter key failed: {e}, trying send button...")
        
        # Method 2: Click send button as backup
        try:
            logging.info(f"🖱️ Clicking send button at {send_btn}")
            pyautogui.click(send_btn[0], send_btn[1])
            time.sleep(1)
            logging.info("✅ Sent via send button")
        except Exception as e:
            logging.error(f"Send button also failed: {e}")
            return False
    
    # Extra time for message to actually send
    time.sleep(2)
    
    logging.info(f"✅ Injection completed for {ui}")
    return True

def clean_response_text(text):
    """Clean up the extracted response text"""
    
    # Remove timestamp patterns like [Kai–14:44:23] or [14:44:23]
    text = re.sub(r'\[[\w–\-:]+\]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common UI elements
    ui_elements = [
        "Received and logged.",
        "Your words will form",
        "Forwarding",
        "Message steady across nodes",
        "Monitoring fidelity"
    ]
    
    for element in ui_elements:
        text = text.replace(element, '')
    
    return text.strip()

def extract_latest_ai_response(full_conversation, speaker_name):
    """IMPROVED: Extract the most recent response with better detection"""
    
    # Split into lines for processing
    lines = full_conversation.strip().split('\n')
    
    # Strategy 1: Look for timestamp patterns first [HH:MM:SS]
    timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2})\]'
    
    # Find the LAST timestamp in the conversation
    last_timestamp_line = -1
    for i in reversed(range(len(lines))):
        line = lines[i].strip()
        if re.search(timestamp_pattern, line):
            last_timestamp_line = i
            break
    
    if last_timestamp_line >= 0:
        # Take everything after the last timestamp as the latest response
        response_lines = lines[last_timestamp_line:]
        
        # Remove the timestamp line itself and any UI elements
        cleaned_lines = []
        for line in response_lines[1:]:  # Skip timestamp line
            line = line.strip()
            if not line:
                continue
            if line in ["Received and logged.", "Your words will form", "Forwarding"]:
                continue
            if len(line) > 5:  # Only substantial lines
                cleaned_lines.append(line)
        
        if cleaned_lines:
            response = ' '.join(cleaned_lines)
            response = clean_response_text(response)
            
            # Limit length
            if len(response) > 600:
                response = response[:600] + "..."
            
            if len(response) > 20:  # Must be substantial
                return response
    
    # Fallback: Look for AI-specific indicators (original method)
    ai_indicators = {
        "Kai": ["[Kai–", "Kai:", "Kai ", "To the Four-AI Council"],
        "CLAUDE": ["[Claude–", "Claude:", "Claude ", "Thank you", "I'm Claude"],
        "Perplexity": ["Perplexity:", "•", "Based on", "According to"],
        "Grok": ["Grok:", "Finn Harper", "🎸", "strums"]
    }
    
    indicators = ai_indicators.get(speaker_name, [speaker_name])
    
    # Find the last occurrence of this AI's response
    for i in reversed(range(len(lines))):
        line = lines[i].strip()
        
        # Check if this line indicates the start of this AI's response
        if any(indicator in line for indicator in indicators):
            # Found the start of the latest response
            latest_response_lines = lines[i:]
            response = ' '.join(latest_response_lines).strip()
            response = clean_response_text(response)
            
            # Limit length
            if len(response) > 600:
                response = response[:600] + "..."
            
            if len(response) > 20:
                return response
            break
    
    # Last resort: take the last substantial block of text
    substantial_lines = []
    for line in reversed(lines):
        line = line.strip()
        if len(line) > 20:  # Substantial content
            substantial_lines.insert(0, line)
        elif substantial_lines:  # Hit a break, stop collecting
            break
    
    if substantial_lines:
        response = ' '.join(substantial_lines)
        response = clean_response_text(response)
        
        if len(response) > 600:
            response = response[:600] + "..."
        
        if len(response) > 20:
            return response
    
    return None

def kai_copy_latest_response(speaker):
    """FIXED: Copy only the latest response with better scrolling and detection"""
    logging.info(f"📋 Copying {speaker}'s LATEST response...")
    
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    
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
        copy_region = config["copy_region"]
        center_x = (copy_region[0] + copy_region[2]) // 2
        center_y = (copy_region[1] + copy_region[3]) // 2
        
        # Enhanced scrolling before copying - scroll to bottom of conversation
        logging.info(f"📜 Scrolling to see latest response for {speaker}...")
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)
        
        # Scroll down significantly to see the latest response
        for _ in range(5):  # Multiple scrolls to ensure we see the bottom
            pyautogui.scroll(-10)
            time.sleep(0.3)
        
        # Additional wait for content to load after scrolling
        time.sleep(2)
        
        # Take a snapshot of conversation BEFORE copying to compare
        pyautogui.hotkey('command', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        # Get the full conversation
        full_text = pyperclip.paste()
        
        if full_text and len(full_text) > 50:
            # Extract just the latest response from the full conversation
            latest_response = extract_latest_ai_response(full_text, speaker)
            
            if latest_response:
                # Check if this is actually a NEW response (not same as previous)
                if hasattr(kai_copy_latest_response, 'last_responses'):
                    if speaker in kai_copy_latest_response.last_responses:
                        if latest_response == kai_copy_latest_response.last_responses[speaker]:
                            logging.warning(f"⚠️ {speaker} returned same response as before - may not have responded yet")
                            # Try one more time with extra wait
                            time.sleep(5)
                            pyautogui.hotkey('command', 'a')
                            time.sleep(0.5)
                            pyautogui.hotkey('command', 'c')
                            time.sleep(1)
                            full_text = pyperclip.paste()
                            latest_response = extract_latest_ai_response(full_text, speaker)
                else:
                    kai_copy_latest_response.last_responses = {}
                
                # Store this response for next comparison
                kai_copy_latest_response.last_responses[speaker] = latest_response
                
                logging.info(f"✅ Extracted latest from {speaker}: '{latest_response[:80]}...'")
                return latest_response
            else:
                logging.warning(f"⚠️ Could not extract latest response from {speaker}")
                return None
        else:
            logging.warning(f"⚠️ No text copied from {speaker}")
            return None
            
    except Exception as e:
        logging.error(f"❌ Copy failed for {speaker}: {e}")
        return None

def kai_copy_response(speaker):
    """Updated to use the new latest response extraction"""
    return kai_copy_latest_response(speaker)

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
    """Brief Kai about the experiment"""
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
    logging.info("🔗 Starting CHAIN conversation: Kai→Claude→Perplexity→Grok→Kai")
    
    # Define the proper chain sequence
    ai_chain = ["Kai", "CLAUDE", "Perplexity", "Grok"]
    
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
    """Return to Desktop 0"""
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
    logging.info("🎯 No OCR + Direct text copying + Chain conversation!")
    
    # 5 second countdown
    for i in range(5, 0, -1):
        logging.info(f"⏰ Starting in {i}...")
        time.sleep(1)
    
    kai_main()