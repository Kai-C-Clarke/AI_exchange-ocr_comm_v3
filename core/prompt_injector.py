import time
import pyautogui
import pyperclip
import logging
import platform
from core import config

def get_modifier_key():
    return 'command' if platform.system() == 'Darwin' else 'ctrl'

def safe_click_area(ui: str):
    (x1, y1), (x2, y2) = config.UI_CONFIGS[ui]["safe_click"]
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    logging.info(f"🖱️ Clicking safe area for {ui} at ({center_x}, {center_y})")
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)

def inject_prompt_clipboard(prompt: str, ui: str):
    logging.info(f"📋 Preparing to inject into {ui}...")
    logging.info(f"📋 Prompt content: '{prompt[:50]}...'")
    
    top_left = config.UI_CONFIGS[ui]["input_top_left"]
    send_btn = config.UI_CONFIGS[ui]["send_button"]
    modifier = get_modifier_key()

    # First, copy to clipboard and verify
    pyperclip.copy(prompt)
    time.sleep(0.5)  # Increased wait time
    
    # Verify clipboard content
    clipboard_content = pyperclip.paste()
    if clipboard_content != prompt:
        logging.error(f"❌ Clipboard verification failed! Expected: '{prompt[:30]}...', Got: '{clipboard_content[:30]}...'")
        return False
    else:
        logging.info("✅ Clipboard content verified")

    # Click the input area (try clicking center of input area instead of top-left)
    input_x, input_y = top_left
    # Add some offset to click more center of input field
    input_x += 50  # Adjust these values based on your UI
    input_y += 10
    
    logging.info(f"🖱️ Clicking input area at ({input_x}, {input_y})")
    pyautogui.click(input_x, input_y)
    time.sleep(1.0)  # Increased wait time for focus

    # Double-click to potentially select existing text
    logging.info("🖱️ Double-clicking to select existing text")
    pyautogui.doubleClick(input_x, input_y)
    time.sleep(0.5)

    # Clear input box more thoroughly
    logging.info("⌨️ Clearing input box")
    pyautogui.hotkey(modifier, 'a')  # Select all
    time.sleep(0.3)
    pyautogui.press('delete')  # Delete selected text
    time.sleep(0.3)
    
    # Additional clearing attempts
    pyautogui.press('backspace')
    time.sleep(0.3)

    # Paste clipboard content
    logging.info("📥 Pasting clipboard content")
    pyautogui.hotkey(modifier, 'v')
    time.sleep(1.0)  # Increased wait time
    
    # Verify something was pasted by checking if we can select text
    pyautogui.hotkey(modifier, 'a')
    time.sleep(0.3)
    pyautogui.hotkey(modifier, 'c')
    time.sleep(0.3)
    pasted_content = pyperclip.paste()
    
    if pasted_content.strip() == "":
        logging.error("❌ No text appears to have been pasted!")
        return False
    else:
        logging.info(f"✅ Text pasted successfully: '{pasted_content[:30]}...'")

    # Send the message
    logging.info("📨 Sending message")
    pyautogui.press('enter')
    time.sleep(1.5)  # Increased wait time

    logging.info(f"✅ Prompt injection completed for {ui}")
    return True

def debug_ui_state(ui: str):
    """Debug function to check UI state"""
    logging.info(f"🔍 Debugging UI state for {ui}")
    
    # Get current mouse position
    x, y = pyautogui.position()
    logging.info(f"Current mouse position: ({x}, {y})")
    
    # Check if we can get screen region
    top_left = config.UI_CONFIGS[ui]["input_top_left"]
    logging.info(f"Configured input area top-left: {top_left}")
    
    # Take a screenshot of the input area for manual inspection
    import PIL.ImageGrab as ImageGrab
    input_region = (top_left[0], top_left[1], top_left[0] + 200, top_left[1] + 50)
    screenshot = ImageGrab.grab(bbox=input_region)
    screenshot.save(f"debug_{ui}_input_area.png")
    logging.info(f"Screenshot saved: debug_{ui}_input_area.png")