#!/usr/bin/env python3
"""
Response Coordinate Finder
Find the exact coordinates where AI responses appear
"""

import pyautogui
import subprocess
import time

class ResponseCoordinateFinder:
    """Find correct response coordinates for each AI"""
    
    def __init__(self):
        self.ai_layout = {
            "kai": {"desktop": 1, "position": "left"},
            "claude": {"desktop": 1, "position": "right"},
            "perplexity": {"desktop": 2, "position": "left"},
            "grok": {"desktop": 2, "position": "right"}
        }
    
    def switch_to_desktop(self, target_desktop):
        """Switch to target desktop"""
        current_desktop = 0  # Assume starting from 0
        
        if target_desktop > current_desktop:
            moves = target_desktop - current_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "right")
                time.sleep(1.5)
        elif target_desktop < current_desktop:
            moves = current_desktop - target_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "left")
                time.sleep(1.5)
        
        time.sleep(1)
    
    def find_response_coordinates_for_ai(self, ai_name):
        """Find response coordinates for a specific AI"""
        
        ai = self.ai_layout[ai_name]
        
        print(f"\n🔍 FINDING RESPONSE COORDINATES FOR {ai_name.upper()}")
        print(f"AI Location: Desktop {ai['desktop']} ({ai['position']} side)")
        
        # Switch to AI's desktop
        print(f"Switching to Desktop {ai['desktop']}...")
        self.switch_to_desktop(ai['desktop'])
        
        print(f"\nInstructions for {ai_name}:")
        print("1. Look at the AI's interface")
        print("2. Find where the AI's response text appears")
        print("3. Move your mouse over a good spot in the response area")
        print("4. Come back to Terminal and press Enter")
        
        input(f"Position mouse over {ai_name}'s response area, then press Enter...")
        
        # Get current mouse position
        response_coords = pyautogui.position()
        print(f"✅ {ai_name} response coordinates: {response_coords}")
        
        # Test these coordinates
        print(f"Testing coordinates {response_coords}...")
        
        # Move to coordinates and test click
        pyautogui.moveTo(response_coords[0], response_coords[1], duration=1)
        time.sleep(0.5)
        
        # Test triple-click selection
        pyautogui.click(response_coords[0], response_coords[1], clicks=3, interval=0.2)
        time.sleep(0.5)
        
        # Test copy
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        # Check what was copied
        try:
            copied_content = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"Copied content length: {len(copied_content)} characters")
            print(f"Preview: {copied_content[:100]}...")
            
            if len(copied_content) > 20:
                print(f"✅ Good coordinates for {ai_name}!")
                return response_coords
            else:
                print(f"⚠️ Coordinates may need adjustment for {ai_name}")
                return response_coords
                
        except Exception as e:
            print(f"❌ Copy failed: {e}")
            return response_coords
    
    def find_all_response_coordinates(self):
        """Find response coordinates for all AIs"""
        
        print("🎯 RESPONSE COORDINATE FINDER")
        print("Finding exact coordinates where each AI's responses appear")
        
        coordinates = {}
        
        for ai_name in self.ai_layout.keys():
            coords = self.find_response_coordinates_for_ai(ai_name)
            coordinates[ai_name] = coords
            
            # Return to Desktop 0 between AIs
            self.switch_to_desktop(0)
            
            # Pause between AIs
            input("Press Enter to find coordinates for next AI...")
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        
        # Print summary
        print(f"\n📋 RESPONSE COORDINATES SUMMARY:")
        print("Copy these into your script:")
        print()
        
        for ai_name, coords in coordinates.items():
            print(f'"{ai_name}": {{')
            print(f'    "response_coords": {coords},')
            print(f'}},')
        
        return coordinates
    
    def test_response_capture(self, ai_name, coords):
        """Test response capture with specific coordinates"""
        
        ai = self.ai_layout[ai_name]
        
        print(f"\n🧪 TESTING RESPONSE CAPTURE FOR {ai_name.upper()}")
        
        # Switch to AI's desktop
        self.switch_to_desktop(ai['desktop'])
        
        print(f"Testing coordinates {coords} for {ai_name}")
        print(f"Make sure {ai_name} has some response text visible...")
        input("Press Enter to test capture...")
        
        # Test the capture method
        pyautogui.moveTo(coords[0], coords[1], duration=1)
        time.sleep(0.5)
        
        # Triple-click to select
        pyautogui.click(coords[0], coords[1], clicks=3, interval=0.2)
        time.sleep(0.5)
        
        # Copy
        pyautogui.hotkey("command", "c")
        time.sleep(0.5)
        
        # Check result
        try:
            content = subprocess.check_output("pbpaste", universal_newlines=True).strip()
            print(f"✅ Captured {len(content)} characters")
            print(f"Content preview: {content[:200]}...")
            
            if len(content) > 50:
                print(f"🎉 SUCCESS! These coordinates work for {ai_name}")
                return True
            else:
                print(f"⚠️ Content too short - coordinates may need adjustment")
                return False
                
        except Exception as e:
            print(f"❌ Capture failed: {e}")
            return False

def main():
    """Main coordinate finder"""
    
    finder = ResponseCoordinateFinder()
    
    print("\n🎯 RESPONSE COORDINATE FINDER")
    print("Find exact coordinates where AI responses appear")
    
    choice = input(f"\nChoose:\n1. Find all response coordinates\n2. Test specific AI coordinates\nChoice: ")
    
    if choice == "1":
        coordinates = finder.find_all_response_coordinates()
        
        print(f"\n💾 Save these coordinates to fix the response capture!")
        
    elif choice == "2":
        ai_name = input("Which AI (kai/claude/perplexity/grok): ").lower()
        if ai_name in finder.ai_layout:
            x = int(input("X coordinate: "))
            y = int(input("Y coordinate: "))
            coords = (x, y)
            
            finder.test_response_capture(ai_name, coords)
        else:
            print("❌ Invalid AI name")
    
    print("\nCoordinate finding complete!")

if __name__ == "__main__":
    main()