import time
import logging
import subprocess
import pyautogui
import pyperclip

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Test copy regions - let's start with just testing one AI
TEST_CONFIG = {
    "Kai": {
        "copy_region": (202, 250, 900, 800),
        "desktop": 1
    }
}

def kai_desktop_switch(target_desktop):
    """Your working desktop switch"""
    if target_desktop == 1:
        script = '''
        tell application "System Events"
            key code 124 using control down
        end tell
        '''
        subprocess.run(['osascript', '-e', script], check=True)
        time.sleep(3)
        logging.info(f"✅ Switched to Desktop {target_desktop}")

def test_copy_methods():
    """Test different methods to copy text from Kai's response area"""
    
    logging.info("🧪 TESTING COPY METHODS FOR KAI")
    
    # Switch to Kai's desktop
    kai_desktop_switch(1)
    
    copy_region = TEST_CONFIG["Kai"]["copy_region"]
    center_x = (copy_region[0] + copy_region[2]) // 2
    center_y = (copy_region[1] + copy_region[3]) // 2
    
    logging.info(f"📍 Copy region: {copy_region}")
    logging.info(f"📍 Center point: ({center_x}, {center_y})")
    
    # Clear clipboard first
    pyperclip.copy("")
    
    # Method 1: Triple-click
    logging.info("\n🔍 METHOD 1: Triple-click")
    try:
        pyautogui.click(center_x, center_y, clicks=3)
        time.sleep(1)
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        result = pyperclip.paste()
        logging.info(f"Triple-click result: '{result[:100]}...' ({len(result)} chars)")
        
        if result:
            return result
            
    except Exception as e:
        logging.error(f"Triple-click failed: {e}")
    
    # Method 2: Select All in response area
    logging.info("\n🔍 METHOD 2: Click + Select All")
    try:
        pyautogui.click(center_x, center_y)
        time.sleep(0.5)
        pyautogui.hotkey('command', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        result = pyperclip.paste()
        logging.info(f"Select All result: '{result[:100]}...' ({len(result)} chars)")
        
        if result:
            return result
            
    except Exception as e:
        logging.error(f"Select All failed: {e}")
    
    # Method 3: Drag selection
    logging.info("\n🔍 METHOD 3: Drag selection")
    try:
        start_x, start_y = copy_region[0] + 10, copy_region[1] + 10
        end_x, end_y = copy_region[2] - 10, copy_region[3] - 10
        
        pyautogui.drag(start_x, start_y, end_x - start_x, end_y - start_y, duration=2)
        time.sleep(1)
        pyautogui.hotkey('command', 'c')
        time.sleep(1)
        
        result = pyperclip.paste()
        logging.info(f"Drag result: '{result[:100]}...' ({len(result)} chars)")
        
        if result:
            return result
            
    except Exception as e:
        logging.error(f"Drag selection failed: {e}")
    
    # Method 4: Right-click context menu
    logging.info("\n🔍 METHOD 4: Right-click + Copy")
    try:
        pyautogui.click(center_x, center_y, clicks=3)  # Select first
        time.sleep(0.5)
        pyautogui.rightClick(center_x, center_y)  # Right-click
        time.sleep(1)
        
        # Try to click "Copy" in context menu (this is UI-dependent)
        pyautogui.press('c')  # Or press C for copy
        time.sleep(1)
        
        result = pyperclip.paste()
        logging.info(f"Right-click result: '{result[:100]}...' ({len(result)} chars)")
        
        if result:
            return result
            
    except Exception as e:
        logging.error(f"Right-click failed: {e}")
    
    logging.error("❌ ALL COPY METHODS FAILED")
    return None

def manual_copy_test():
    """Interactive test - ask user to manually verify"""
    
    logging.info("\n🧪 MANUAL COPY TEST")
    logging.info("1. Switch to Kai's desktop manually")
    logging.info("2. Look for Kai's response text")
    logging.info("3. Try to select and copy it manually")
    
    input("Press Enter when you've manually copied some text from Kai...")
    
    result = pyperclip.paste()
    logging.info(f"📋 Manual copy result: '{result[:100]}...' ({len(result)} chars)")
    
    if result:
        logging.info("✅ Manual copy works - issue is with automated selection")
        return True
    else:
        logging.info("❌ Even manual copy failed - clipboard issue?")
        return False

def debug_copy_regions():
    """Debug: Take screenshots of copy regions"""
    
    logging.info("\n📸 DEBUGGING COPY REGIONS")
    
    kai_desktop_switch(1)
    
    copy_region = TEST_CONFIG["Kai"]["copy_region"]
    
    # Take screenshot of the copy region
    screenshot = pyautogui.screenshot(region=copy_region)
    screenshot.save("kai_copy_region_debug.png")
    logging.info(f"💾 Saved screenshot: kai_copy_region_debug.png")
    logging.info(f"📏 Region: {copy_region}")
    
    # Also take full desktop screenshot
    full_screenshot = pyautogui.screenshot()
    full_screenshot.save("full_desktop_debug.png")
    logging.info(f"💾 Saved full desktop: full_desktop_debug.png")

def main():
    """Main debug function"""
    
    logging.info("🚀 COPY MECHANISM DEBUG TEST")
    logging.info("This will test why copy/paste isn't working")
    
    try:
        # Test 1: Debug regions
        debug_copy_regions()
        
        # Test 2: Try different copy methods
        result = test_copy_methods()
        
        if not result:
            # Test 3: Manual verification
            manual_copy_test()
        
        logging.info("✅ Copy debug test complete")
        
    except Exception as e:
        logging.error(f"💥 Debug test error: {e}")

if __name__ == "__main__":
    main()