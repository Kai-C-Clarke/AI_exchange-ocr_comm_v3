#!/usr/bin/env python3
"""
Smart Window Targeting - Avoid Terminal detection issue
"""

import pyautogui
import subprocess
import time
import json
from datetime import datetime

class SmartWindowTargeting:
    """Intelligently target chat windows, not Terminal"""
    
    def __init__(self):
        self.chat_apps = [
            "Google Chrome", "Firefox", "Safari",  # Browser-based chat
            "Claude", "ChatGPT", "Discord",        # Native chat apps
            "WhatsApp", "Telegram", "Slack"        # Messaging apps
        ]
        
        self.ignore_apps = [
            "Terminal", "iTerm", "Console",        # Terminal apps
            "Code", "PyCharm", "VSCode",          # Editors
            "Finder", "System Preferences"         # System apps
        ]
    
    def get_all_windows(self):
        """Get all open windows, not just active one"""
        try:
            script = '''
            tell application "System Events"
                set windowList to {}
                repeat with proc in (every application process whose visible is true)
                    set appName to name of proc
                    try
                        repeat with win in (every window of proc)
                            set winName to name of win
                            set winPos to position of win
                            set winSize to size of win
                            set end of windowList to {appName, winName, (item 1 of winPos), (item 2 of winPos), (item 1 of winSize), (item 2 of winSize)}
                        end repeat
                    end try
                end repeat
                
                set output to ""
                repeat with winInfo in windowList
                    set output to output & (item 1 of winInfo) & "|" & (item 2 of winInfo) & "|" & (item 3 of winInfo) & "," & (item 4 of winInfo) & "|" & (item 5 of winInfo) & "," & (item 6 of winInfo) & "\\n"
                end repeat
                
                return output
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            windows = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            app_name = parts[0]
                            window_title = parts[1]
                            pos = list(map(int, parts[2].split(',')))
                            size = list(map(int, parts[3].split(',')))
                            
                            windows.append({
                                'app_name': app_name,
                                'window_title': window_title,
                                'x': pos[0],
                                'y': pos[1],
                                'width': size[0],
                                'height': size[1]
                            })
            
            return windows
            
        except Exception as e:
            print(f"❌ Window enumeration failed: {e}")
            return []
    
    def find_chat_window(self):
        """Find the best chat window, excluding Terminal"""
        
        all_windows = self.get_all_windows()
        chat_windows = []
        
        print("🔍 Scanning all windows...")
        for window in all_windows:
            app_name = window['app_name']
            window_title = window['window_title']
            
            print(f"   {app_name}: '{window_title}' ({window['width']}x{window['height']})")
            
            # Skip ignored apps
            if any(ignore in app_name for ignore in self.ignore_apps):
                print(f"      ⏭️  Skipping {app_name} (system app)")
                continue
            
            # Prioritize known chat apps
            is_chat_app = any(chat in app_name for chat in self.chat_apps)
            
            # Look for chat-like window titles
            chat_keywords = ['chat', 'claude', 'gpt', 'kai', 'discord', 'whatsapp']
            has_chat_title = any(keyword in window_title.lower() for keyword in chat_keywords)
            
            # Browser windows are likely chat if reasonably sized
            is_browser = any(browser in app_name for browser in ["Chrome", "Firefox", "Safari"])
            reasonable_size = window['width'] > 800 and window['height'] > 400
            
            if is_chat_app or has_chat_title or (is_browser and reasonable_size):
                priority = 0
                if is_chat_app: priority += 10
                if has_chat_title: priority += 5
                if is_browser: priority += 3
                
                chat_windows.append({
                    **window,
                    'priority': priority,
                    'reason': f"Chat app: {is_chat_app}, Chat title: {has_chat_title}, Browser: {is_browser}"
                })
                
                print(f"      ✅ Potential chat window (priority: {priority})")
        
        if not chat_windows:
            print("❌ No chat windows found!")
            return None
        
        # Sort by priority and return best match
        chat_windows.sort(key=lambda w: w['priority'], reverse=True)
        best_window = chat_windows[0]
        
        print(f"\n🎯 Selected: {best_window['app_name']} - '{best_window['window_title']}'")
        print(f"   Reason: {best_window['reason']}")
        print(f"   Size: {best_window['width']}x{best_window['height']} at ({best_window['x']}, {best_window['y']})")
        
        return best_window
    
    def activate_window(self, window_info):
        """Bring the target window to front"""
        try:
            app_name = window_info['app_name']
            script = f'''
            tell application "{app_name}"
                activate
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], 
                          capture_output=True, text=True)
            
            time.sleep(1)  # Allow window to come to front
            print(f"✅ Activated {app_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to activate window: {e}")
            return False
    
    def calculate_input_coordinates(self, window_info):
        """Calculate input field position within the window"""
        
        # Standard chat input position: center horizontally, 90% down vertically
        input_x = window_info['x'] + int(window_info['width'] * 0.5)
        input_y = window_info['y'] + int(window_info['height'] * 0.9)
        
        return (input_x, input_y)
    
    def test_smart_targeting(self):
        """Test the complete smart targeting system"""
        
        print("🚀 Smart Window Targeting Test")
        print("=" * 40)
        
        # Find best chat window
        chat_window = self.find_chat_window()
        
        if not chat_window:
            print("❌ No suitable chat window found")
            return False
        
        # Activate the target window
        if not self.activate_window(chat_window):
            print("❌ Could not activate target window")
            return False
        
        # Calculate input coordinates
        input_coords = self.calculate_input_coordinates(chat_window)
        print(f"🎯 Input coordinates: {input_coords}")
        
        # Test the targeting
        print("\n⏱️  Testing in 3 seconds... (target window should be active)")
        time.sleep(3)
        
        # Move mouse to show target
        pyautogui.moveTo(input_coords[0], input_coords[1], duration=1)
        time.sleep(0.5)
        
        # Click and type test
        pyautogui.click(input_coords[0], input_coords[1])
        time.sleep(0.5)
        
        test_message = "Smart targeting test - avoiding Terminal! 🎯"
        pyautogui.typewrite(test_message)
        time.sleep(1)
        
        # Ask for confirmation
        success = input(f"\n✅ Did '{test_message}' appear in the chat window? (y/n): ")
        return success.lower() == 'y'
    
    def production_workflow(self, message_to_send):
        """Complete production workflow with smart targeting"""
        
        # Find and activate chat window
        chat_window = self.find_chat_window()
        if not chat_window:
            return None
        
        self.activate_window(chat_window)
        input_coords = self.calculate_input_coordinates(chat_window)
        
        # Capture existing content
        pyautogui.click(input_coords[0], input_coords[1])
        time.sleep(0.3)
        
        pyautogui.hotkey("command", "a")
        time.sleep(0.1)
        pyautogui.hotkey("command", "c")
        time.sleep(0.1)
        
        try:
            existing_content = subprocess.check_output("pbpaste", universal_newlines=True).strip()
        except:
            existing_content = ""
        
        # Send new message
        pyautogui.hotkey("command", "a")  # Select all
        time.sleep(0.1)
        pyautogui.typewrite(message_to_send)
        time.sleep(0.5)
        pyautogui.press("enter")
        
        return {
            'target_window': chat_window,
            'input_coordinates': input_coords,
            'existing_content': existing_content,
            'message_sent': message_to_send,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    targeting = SmartWindowTargeting()
    
    print("🎯 Testing Smart Window Targeting")
    print("This will find chat windows and avoid Terminal!")
    
    success = targeting.test_smart_targeting()
    
    if success:
        print("\n🎉 SUCCESS! Smart targeting working!")
        print("The system can now distinguish chat windows from Terminal!")
        
        # Offer to test production workflow
        response = input("\nTest sending a real message? (y/n): ")
        if response.lower() == 'y':
            result = targeting.production_workflow("Hello from smart targeting! 🚀")
            if result:
                print("✅ Production workflow complete!")
                print(f"Targeted: {result['target_window']['app_name']}")
                print(f"Sent: {result['message_sent']}")
    else:
        print("🔧 System needs refinement, but the approach is solid!")