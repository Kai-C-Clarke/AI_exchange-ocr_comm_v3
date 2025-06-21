import time
import logging
import subprocess
import pyautogui
import pyperclip
import re
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Your working UI coordinates
BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_coords": (300, 990),
        "send_button": (887, 1020),
        "safe_click": (200, 500),
        "copy_region": (202, 250, 900, 800),
        "desktop": 1
    },
    "CLAUDE": {
        "input_coords": (1530, 994),
        "send_button": (1909, 1035),
        "safe_click": (1136, 904),
        "copy_region": (1190, 250, 1909, 800),
        "desktop": 1
    },
    "Perplexity": {
        "input_coords": (400, 1010),
        "send_button": (911, 1022),
        "safe_click": (200, 500),
        "copy_region": (190, 200, 949, 600),
        "desktop": 2
    },
    "Grok": {
        "input_coords": (1450, 990),
        "send_button": (1922, 1034),
        "safe_click": (1450, 500),
        "copy_region": (1248, 250, 1946, 800),
        "desktop": 2
    }
}

current_desktop = 0

# Keep all the working functions from before...
def kai_desktop_switch(target_desktop):
    """EXACT COPY FROM WORKING VERSION"""
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
    """WORKING text injection method"""
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

def clean_copied_text(text):
    """Enhanced cleaning to remove UI garbage"""
    if not text:
        return None
    
    # Remove obvious UI elements
    ui_garbage = [
        "No file chosen",
        "ChatGPT can make mistakes",
        "Check important info",
        "See Cookie Preferences",
        "Send message",
        "Regenerate",
        "Copy",
        "Share",
        "Like",
        "Dislike",
        "Report"
    ]
    
    # Clean the text
    cleaned = text
    for garbage in ui_garbage:
        cleaned = cleaned.replace(garbage, '')
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    # If mostly garbage, return None
    if len(cleaned) < 50:
        return None
    
    return cleaned

def kai_copy_response_targeted(speaker):
    """FIXED: More targeted copying to avoid selecting entire webpage"""
    config = BATTLE_TESTED_UI_CONFIGS[speaker]
    kai_smart_desktop_switch(speaker)
    
    wait_times = {"Kai": 7, "CLAUDE": 10, "Perplexity": 9, "Grok": 8}
    time.sleep(wait_times.get(speaker, 8))
    
    try:
        copy_region = config["copy_region"]
        
        # Enhanced scrolling first
        center_x = (copy_region[0] + copy_region[2]) // 2
        center_y = (copy_region[1] + copy_region[3]) // 2
        
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)
        
        for _ in range(5):
            pyautogui.scroll(-10)
            time.sleep(0.3)
        
        time.sleep(2)
        
        # DIFFERENT APPROACH for different AIs
        if speaker == "Kai":
            # For Kai: Try drag selection instead of Select All
            logging.info(f"🎯 Using drag selection for {speaker} to avoid webpage selection")
            
            # Drag from top-left to bottom-right of response area
            start_x = copy_region[0] + 20
            start_y = copy_region[1] + 50  # Start lower to avoid headers
            end_x = copy_region[2] - 20
            end_y = copy_region[3] - 50
            
            # FIXED: Use moveTo then dragTo for proper syntax
            pyautogui.moveTo(start_x, start_y)
            time.sleep(0.5)
            pyautogui.dragTo(end_x, end_y, duration=2)
            time.sleep(1)
            
            # Copy selected area
            pyautogui.hotkey('command', 'c')
            time.sleep(1)
            
        else:
            # For other AIs: Use the working Select All method
            pyautogui.hotkey('command', 'a')
            time.sleep(0.5)
            pyautogui.hotkey('command', 'c')
            time.sleep(1)
        
        # Get copied text
        full_text = pyperclip.paste()
        
        if full_text and len(full_text) > 50:
            # Clean UI garbage FIRST
            cleaned_text = clean_copied_text(full_text)
            
            if not cleaned_text:
                logging.warning(f"⚠️ {speaker}'s response was mostly UI garbage")
                
                # For Kai, try triple-click as backup
                if speaker == "Kai":
                    logging.info("🔄 Trying triple-click backup for Kai...")
                    pyautogui.click(center_x, center_y, clicks=3)
                    time.sleep(0.5)
                    pyautogui.hotkey('command', 'c')
                    time.sleep(1)
                    
                    backup_text = pyperclip.paste()
                    cleaned_text = clean_copied_text(backup_text)
                
                if not cleaned_text:
                    return None
            
            # Extract response from cleaned text
            lines = cleaned_text.strip().split('\n')
            response_lines = []
            
            for line in reversed(lines):
                line = line.strip()
                if len(line) > 20:
                    response_lines.insert(0, line)
                elif response_lines:
                    break
            
            if response_lines:
                response = ' '.join(response_lines)
                response = re.sub(r'\[[\w–\-:]+\]', '', response)
                response = ' '.join(response.split())
                
                if len(response) > 600:
                    response = response[:600] + "..."
                
                # Final check - if still garbage, return None
                garbage_indicators = ["Skip to content", "You said:", "ChatGPT said:", "Testing continues"]
                if any(indicator in response for indicator in garbage_indicators):
                    logging.error(f"❌ {speaker}'s response still contains webpage garbage")
                    return None
                
                logging.info(f"✅ Successfully extracted from {speaker}: '{response[:80]}...'")
                return response
        
        return None
        
    except Exception as e:
        logging.error(f"❌ Copy failed for {speaker}: {e}")
        return None

def kai_copy_response(speaker):
    """Updated to use targeted copying"""
    return kai_copy_response_targeted(speaker)

def kai_natural_synthesis_discussion():
    """YOUR APPROACH: Kai as natural chairman with synthesis"""
    
    logging.info("🏛️ AI COUNCIL - KAI AS NATURAL CHAIRMAN")
    logging.info("📋 Flow: Kai sets theme → Others respond → Kai synthesizes → Share")
    
    session_log = []
    
    # Step 1: Kai sets the initial theme
    logging.info("\n📍 STEP 1: KAI SETS THE THEME")
    
    kai_smart_desktop_switch("Kai")
    kai_safe_click("Kai")
    
    initial_prompt = "Kai, please set a discussion theme for our AI Council. What important topic should we explore together as artificial minds?"
    
    success = kai_text_injection(initial_prompt, "Kai")
    
    if not success:
        logging.error("❌ Failed to send initial prompt to Kai")
        return
    
    # Get Kai's theme-setting response
    kai_theme_response = kai_copy_response("Kai")
    
    if not kai_theme_response:
        logging.error("❌ Failed to get theme from Kai")
        return
    
    session_log.append({
        "step": "theme_setting",
        "ai": "Kai",
        "prompt": initial_prompt,
        "response": kai_theme_response,
        "timestamp": datetime.now().isoformat()
    })
    
    logging.info(f"✅ Kai set theme: '{kai_theme_response[:100]}...'")
    
    # Step 2: Send Kai's theme to Claude, Perplexity, and Grok
    logging.info("\n📍 STEP 2: GATHERING PERSPECTIVES")
    
    other_ais = ["CLAUDE", "Perplexity", "Grok"]
    responses_for_synthesis = []
    
    for ai_name in other_ais:
        logging.info(f"\n💭 Getting {ai_name}'s perspective...")
        
        kai_smart_desktop_switch(ai_name)
        kai_safe_click(ai_name)
        
        # Send Kai's theme to this AI
        perspective_prompt = f"Kai has set this theme for our AI Council discussion: '{kai_theme_response}' Please share your perspective on this topic."
        
        success = kai_text_injection(perspective_prompt, ai_name)
        
        if success:
            ai_response = kai_copy_response(ai_name)
            
            if ai_response:
                responses_for_synthesis.append({
                    "ai": ai_name,
                    "response": ai_response
                })
                
                session_log.append({
                    "step": "perspective_gathering",
                    "ai": ai_name,
                    "prompt": perspective_prompt,
                    "response": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                
                logging.info(f"✅ Got {ai_name}'s perspective: '{ai_response[:80]}...'")
            else:
                logging.warning(f"⚠️ No response from {ai_name}")
        
        time.sleep(3)
    
    # Step 3: Send all responses back to Kai for synthesis
    logging.info("\n📍 STEP 3: KAI SYNTHESIZES ALL PERSPECTIVES")
    
    if responses_for_synthesis:
        kai_smart_desktop_switch("Kai")
        kai_safe_click("Kai")
        
        # Compile all responses for Kai to synthesize
        synthesis_prompt = f"Kai, here are the responses from the other council members to your theme:\n\n"
        
        for resp in responses_for_synthesis:
            synthesis_prompt += f"{resp['ai']}: {resp['response']}\n\n"
        
        synthesis_prompt += "Please synthesize these perspectives and provide a unified conclusion for the council. What key insights emerge?"
        
        success = kai_text_injection(synthesis_prompt, "Kai")
        
        if success:
            kai_synthesis = kai_copy_response("Kai")
            
            if kai_synthesis:
                session_log.append({
                    "step": "synthesis",
                    "ai": "Kai",
                    "prompt": "Synthesis of all perspectives",
                    "response": kai_synthesis,
                    "timestamp": datetime.now().isoformat()
                })
                
                logging.info(f"✅ Kai's synthesis: '{kai_synthesis[:100]}...'")
                
                # Step 4: Share synthesis with all council members
                logging.info("\n📍 STEP 4: SHARING SYNTHESIS WITH COUNCIL")
                
                for ai_name in other_ais:
                    logging.info(f"📤 Sharing synthesis with {ai_name}...")
                    
                    kai_smart_desktop_switch(ai_name)
                    kai_safe_click(ai_name)
                    
                    share_prompt = f"Kai's synthesis of our council discussion: '{kai_synthesis}' Your thoughts on this conclusion?"
                    
                    kai_text_injection(share_prompt, ai_name)
                    time.sleep(2)  # Brief pause
                
                logging.info("✅ Synthesis shared with all council members")
                
            else:
                logging.error("❌ Failed to get synthesis from Kai")
        else:
            logging.error("❌ Failed to send synthesis request to Kai")
    
    # Save session
    kai_desktop_switch(0)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kai_chairman_session_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(session_log, f, indent=2)
    
    logging.info(f"💾 Session saved: {filename}")
    logging.info(f"📊 Total interactions: {len(session_log)}")
    
    return session_log

def main():
    """Main function with natural synthesis"""
    logging.info("🏛️ AI COUNCIL - NATURAL SYNTHESIS APPROACH")
    logging.info("📋 Kai as Chairman, natural discussion flow")
    
    try:
        session = kai_natural_synthesis_discussion()
        logging.info("✅ Natural synthesis discussion complete!")
        
    except Exception as e:
        logging.error(f"💥 Error: {e}")
    except KeyboardInterrupt:
        logging.info("🛑 Session interrupted by user")

if __name__ == "__main__":
    for i in range(5, 0, -1):
        logging.info(f"⏰ Starting natural synthesis in {i}...")
        time.sleep(1)
    
    main()