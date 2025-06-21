#!/usr/bin/env python3
"""
Desktop-Aware AI Council Targeting
Handles multiple desktops/spaces and UI positioning
"""

import pyautogui
import subprocess
import time
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class AILocation:
    """Precise location of an AI interface"""
    name: str
    desktop_number: int      # Which desktop/space (0, 1, 2...)
    position: str           # "left", "right", "center", "fullscreen"
    window_keywords: List[str]
    ui_profile: str
    
class DesktopAwareTargeting:
    """Navigate between desktops and target specific UI positions"""
    
    def __init__(self):
        # Jon's exact AI layout
        self.ai_locations = {
            "kai": AILocation(
                name="Kai",
                desktop_number=1,  # Desktop 1 LEFT
                position="left",   
                window_keywords=["claude", "kai", "anthropic"],
                ui_profile="claude_left"
            ),
            "claude": AILocation(
                name="Claude", 
                desktop_number=1,  # Desktop 1 RIGHT
                position="right",  
                window_keywords=["claude", "anthropic"],
                ui_profile="claude_right"
            ),
            "perplexity": AILocation(
                name="Perplexity",
                desktop_number=2,  # Desktop 2 LEFT
                position="left",   
                window_keywords=["perplexity", "pplx"],
                ui_profile="perplexity_left"
            ),
            "grok": AILocation(
                name="Grok",
                desktop_number=2,  # Desktop 2 RIGHT  
                position="right",  
                window_keywords=["grok", "x.ai", "twitter"],
                ui_profile="grok_right"
            )
        }
        
        # UI profiles for Jon's exact layout
        self.ui_profiles = {
            "claude_left": {
                "input_position": (0.25, 0.9),    # Kai on Desktop 1 LEFT
                "response_position": (0.25, 0.4),
                "window_fraction": 0.5
            },
            "claude_right": {
                "input_position": (0.75, 0.9),    # Claude on Desktop 1 RIGHT
                "response_position": (0.75, 0.4),
                "window_fraction": 0.5
            },
            "perplexity_left": {
                "input_position": (0.25, 0.88),   # Perplexity on Desktop 2 LEFT
                "response_position": (0.25, 0.4),
                "window_fraction": 0.5
            },
            "grok_right": {
                "input_position": (0.75, 0.92),   # Grok on Desktop 2 RIGHT
                "response_position": (0.75, 0.45),
                "window_fraction": 0.5
            }
        }
        
        self.current_desktop = self.get_current_desktop()
        self.screen_width, self.screen_height = self.get_screen_size()
        
        print(f"🖥️  Desktop-Aware Targeting initialized")
        print(f"   Current desktop: {self.current_desktop}")
        print(f"   Screen size: {self.screen_width}x{self.screen_height}")
    
    def get_screen_size(self):
        """Get current screen dimensions"""
        from PIL import ImageGrab
        img = ImageGrab.grab()
        return img.size
    
    def get_current_desktop(self):
        """Get the current desktop/space number"""
        try:
            # This AppleScript gets the current space number
            script = '''
            tell application "System Events"
                tell application process "Dock"
                    set currentSpace to value of attribute "AXSelectedChildren" of list 1 of group 1 of group 1
                    return (count of currentSpace)
                end tell
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return int(result.stdout.strip()) - 1  # Convert to 0-based indexing
            else:
                # Fallback: assume desktop 0
                return 0
                
        except Exception as e:
            print(f"⚠️  Could not detect current desktop: {e}")
            return 0
    
    def switch_to_desktop(self, desktop_number: int):
        """Switch to a specific desktop/space"""
        
        if desktop_number == self.current_desktop:
            print(f"✅ Already on desktop {desktop_number}")
            return True
        
        print(f"🔄 Switching from desktop {self.current_desktop} to {desktop_number}")
        
        try:
            # Method 1: Use Control + Arrow keys to switch desktops
            if desktop_number > self.current_desktop:
                # Move right
                moves = desktop_number - self.current_desktop
                for _ in range(moves):
                    pyautogui.hotkey("ctrl", "right")
                    time.sleep(0.5)
            else:
                # Move left  
                moves = self.current_desktop - desktop_number
                for _ in range(moves):
                    pyautogui.hotkey("ctrl", "left") 
                    time.sleep(0.5)
            
            # Give time for desktop switch animation
            time.sleep(1.5)
            
            # Update current desktop
            self.current_desktop = desktop_number
            print(f"✅ Switched to desktop {desktop_number}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to switch to desktop {desktop_number}: {e}")
            return False
    
    def calculate_position_coordinates(self, ai_name: str):
        """Calculate exact coordinates for an AI based on their location"""
        
        location = self.ai_locations[ai_name]
        profile = self.ui_profiles[location.ui_profile]
        
        # Calculate coordinates based on screen position
        input_x = int(self.screen_width * profile['input_position'][0])
        input_y = int(self.screen_height * profile['input_position'][1])
        
        response_x = int(self.screen_width * profile['response_position'][0])
        response_y = int(self.screen_height * profile['response_position'][1])
        
        return {
            'input_coords': (input_x, input_y),
            'response_coords': (response_x, response_y),
            'desktop': location.desktop_number,
            'position': location.position
        }
    
    def navigate_to_ai(self, ai_name: str):
        """Navigate to the specific desktop and position for an AI"""
        
        if ai_name not in self.ai_locations:
            print(f"❌ Unknown AI: {ai_name}")
            return None
        
        location = self.ai_locations[ai_name]
        
        print(f"🎯 Navigating to {ai_name}")
        print(f"   Target: Desktop {location.desktop_number}, {location.position} side")
        
        # Switch to the correct desktop
        if not self.switch_to_desktop(location.desktop_number):
            return None
        
        # Calculate coordinates for this AI
        coords = self.calculate_position_coordinates(ai_name)
        
        print(f"   Input coords: {coords['input_coords']}")
        print(f"   Response coords: {coords['response_coords']}")
        
        return coords
    
    def test_ai_targeting(self, ai_name: str):
        """Test targeting a specific AI"""
        
        coords = self.navigate_to_ai(ai_name)
        if not coords:
            return False
        
        print(f"🧪 Testing {ai_name} targeting...")
        print("⏱️  Moving to input field in 2 seconds...")
        time.sleep(2)
        
        # Visual feedback - move mouse to show target
        input_coords = coords['input_coords']
        pyautogui.moveTo(input_coords[0], input_coords[1], duration=1)
        time.sleep(0.5)
        
        # Click and type test
        pyautogui.click(input_coords[0], input_coords[1])
        time.sleep(0.5)
        
        test_message = f"Desktop-aware test for {ai_name}! 🎯"
        pyautogui.typewrite(test_message)
        time.sleep(1)
        
        success = input(f"✅ Did the message appear in {ai_name}'s input field? (y/n): ")
        return success.lower() == 'y'
    
    def test_full_navigation(self):
        """Test navigation to all AI locations"""
        
        print("🗺️  FULL NAVIGATION TEST")
        print("=" * 40)
        
        results = {}
        
        for ai_name in self.ai_locations.keys():
            print(f"\n📍 Testing {ai_name.upper()}")
            
            location = self.ai_locations[ai_name]
            print(f"   Expected: Desktop {location.desktop_number}, {location.position}")
            
            success = self.test_ai_targeting(ai_name)
            results[ai_name] = success
            
            if success:
                print(f"✅ {ai_name} targeting successful!")
            else:
                print(f"❌ {ai_name} targeting failed - needs adjustment")
            
            # Pause between tests
            input("Press Enter to test next AI...")
        
        # Summary
        print(f"\n📊 NAVIGATION TEST RESULTS:")
        for ai_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {ai_name.upper()}: {status}")
        
        success_count = sum(results.values())
        print(f"\n🎯 {success_count}/{len(results)} AIs successfully targeted")
        
        return results
    
    def setup_ai_locations(self):
        """Interactive setup to configure AI locations"""
        
        print("🔧 AI LOCATION SETUP")
        print("Let's configure where each AI is located...")
        
        for ai_name in self.ai_locations.keys():
            current_location = self.ai_locations[ai_name]
            
            print(f"\n🤖 {ai_name.upper()} Configuration:")
            print(f"   Current: Desktop {current_location.desktop_number}, {current_location.position}")
            
            change = input("Update this location? (y/n): ")
            if change.lower() == 'y':
                desktop = int(input("Desktop number (0, 1, 2...): "))
                position = input("Position (left/right/center/fullscreen): ")
                
                # Update the location
                self.ai_locations[ai_name].desktop_number = desktop
                self.ai_locations[ai_name].position = position
                
                # Update UI profile accordingly
                profile_name = f"{ai_name}_{position}"
                self.ai_locations[ai_name].ui_profile = profile_name
                
                print(f"✅ Updated {ai_name}: Desktop {desktop}, {position}")
        
        print(f"\n💾 AI locations configured!")
    
    def save_configuration(self, filename: str = "ai_desktop_config.json"):
        """Save the desktop configuration"""
        
        config = {
            'ai_locations': {
                name: {
                    'name': loc.name,
                    'desktop_number': loc.desktop_number,
                    'position': loc.position,
                    'window_keywords': loc.window_keywords,
                    'ui_profile': loc.ui_profile
                }
                for name, loc in self.ai_locations.items()
            },
            'ui_profiles': self.ui_profiles,
            'screen_size': [self.screen_width, self.screen_height],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Configuration saved: {filename}")

def main():
    """Main desktop-aware targeting demo"""
    
    print("🖥️  DESKTOP-AWARE AI COUNCIL TARGETING")
    print("=" * 50)
    
    targeting = DesktopAwareTargeting()
    
    print(f"\n📋 Current AI Layout:")
    for ai_name, location in targeting.ai_locations.items():
        print(f"   {ai_name.upper()}: Desktop {location.desktop_number}, {location.position}")
    
    choice = input(f"\nWhat would you like to do?\n1. Test navigation to all AIs\n2. Setup/modify AI locations\n3. Test specific AI\nChoice (1-3): ")
    
    if choice == "1":
        targeting.test_full_navigation()
    elif choice == "2":
        targeting.setup_ai_locations()
        targeting.save_configuration()
    elif choice == "3":
        ai_name = input("Enter AI name (kai/claude/finn/perplexity): ").lower()
        if ai_name in targeting.ai_locations:
            targeting.test_ai_targeting(ai_name)
        else:
            print("❌ Invalid AI name")
    
    print(f"\n🎯 Desktop-aware targeting complete!")

if __name__ == "__main__":
    main()