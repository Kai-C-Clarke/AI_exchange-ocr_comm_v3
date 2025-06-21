#!/usr/bin/env python3
"""
AI Council Targeting - Using Kai's Proven Method
Fixed coordinates + AppleScript typing + Click-to-focus
NO percentages, NO emoji, NO overcomplications
"""

import pyautogui
import subprocess
import time
import os
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class AITarget:
    """Simple AI targeting with fixed coordinates"""
    name: str
    desktop: int
    input_coords: Tuple[int, int]  # Fixed pixel coordinates
    response_coords: Tuple[int, int]

class KaiProvenTargeting:
    """Using Kai's proven method - fixed coords + AppleScript"""
    
    def __init__(self):
        # Jon's exact layout with FIXED PIXEL COORDINATES
        self.ai_targets = {
            "kai": AITarget(
                name="Kai",
                desktop=1,
                input_coords=(456, 960),    # Kai's proven coordinates
                response_coords=(456, 500)  # Response area above input
            ),
            "claude": AITarget(
                name="Claude", 
                desktop=1,
                input_coords=(1200, 960),   # Right side of Desktop 1
                response_coords=(1200, 500)
            ),
            "perplexity": AITarget(
                name="Perplexity",
                desktop=2, 
                input_coords=(456, 960),    # Left side of Desktop 2
                response_coords=(456, 500)
            ),
            "grok": AITarget(
                name="Grok",
                desktop=2,
                input_coords=(1200, 960),   # Right side of Desktop 2  
                response_coords=(1200, 500)
            )
        }
        
        self.current_desktop = 0  # Start from launch pad
        
        print("AI Council Targeting - Kai's Proven Method")
        print("Fixed coordinates + AppleScript + Click-to-focus")
    
    def switch_to_desktop(self, target_desktop: int):
        """Switch desktops using proven method"""
        
        if target_desktop == self.current_desktop:
            return True
        
        print(f"Switching from Desktop {self.current_desktop} to {target_desktop}")
        
        if target_desktop > self.current_desktop:
            moves = target_desktop - self.current_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "right")
                time.sleep(0.8)
        else:
            moves = self.current_desktop - target_desktop
            for _ in range(moves):
                pyautogui.hotkey("ctrl", "left")
                time.sleep(0.8)
        
        self.current_desktop = target_desktop
        time.sleep(1)  # Allow desktop switch to complete
        return True
    
    def click_to_focus(self, x: int, y: int):
        """Kai's method: Always click to focus before typing"""
        
        print(f"Click-to-focus at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.5)  # Critical pause for focus
    
    def type_with_applescript(self, text: str):
        """Kai's AppleScript typing method - avoids emoji popup"""
        
        # Sanitize text - remove any problematic characters
        clean_text = text.replace('"', '\\"').replace("'", "\\'")
        clean_text = ''.join(c for c in clean_text if ord(c) < 128)  # ASCII only
        
        script = f'''
        osascript -e 'tell application "System Events" to keystroke "{clean_text}"'
        '''
        
        print(f"Typing with AppleScript: {clean_text[:50]}...")
        os.system(script)
        time.sleep(0.3)
    
    def target_ai(self, ai_name: str, message: str):
        """Complete targeting using Kai's proven method"""
        
        if ai_name not in self.ai_targets:
            print(f"Unknown AI: {ai_name}")
            return False
        
        target = self.ai_targets[ai_name]
        
        print(f"\nTargeting {target.name}")
        print(f"Desktop: {target.desktop}")
        print(f"Input coords: {target.input_coords}")
        
        # Step 1: Switch to correct desktop
        self.switch_to_desktop(target.desktop)
        
        # Step 2: Click to focus (Kai's critical step)
        self.click_to_focus(target.input_coords[0], target.input_coords[1])
        
        # Step 3: Clear any existing content
        pyautogui.hotkey("command", "a")  # Select all
        time.sleep(0.2)
        
        # Step 4: Type with AppleScript (Kai's method)
        self.type_with_applescript(message)
        
        print(f"Message sent to {target.name}")
        return True
    
    def test_single_ai(self, ai_name: str):
        """Test targeting a single AI"""
        
        target = self.ai_targets[ai_name]
        test_message = f"Test message for {target.name} using Kai method"
        
        print(f"\nTesting {ai_name.upper()}")
        print(f"Will switch to Desktop {target.desktop} and click {target.input_coords}")
        
        ready = input("Press Enter when ready to watch...")
        
        success = self.target_ai(ai_name, test_message)
        
        if success:
            # Return to Desktop 0 for feedback
            self.switch_to_desktop(0)
            
            worked = input(f"Did you see the message in {target.name}? (y/n): ")
            return worked.lower() == 'y'
        
        return False
    
    def test_all_ais(self):
        """Test all AI targets"""
        
        print("\nTesting all AI targets using Kai's proven method")
        
        results = {}
        
        for ai_name in self.ai_targets.keys():
            print(f"\n{'='*40}")
            success = self.test_single_ai(ai_name)
            results[ai_name] = success
            
            if success:
                print(f"✅ {ai_name} - SUCCESS")
            else:
                print(f"❌ {ai_name} - FAILED (need coordinate adjustment)")
        
        print(f"\n{'='*40}")
        print("FINAL RESULTS:")
        for ai_name, success in results.items():
            status = "PASS" if success else "FAIL" 
            print(f"  {ai_name.upper()}: {status}")
        
        return results
    
    def run_ai_relay(self, initial_message: str):
        """Run the complete AI relay using proven method"""
        
        sequence = ["kai", "claude", "perplexity", "grok"]
        current_message = initial_message
        
        print(f"\nStarting AI relay with Kai's proven method")
        print(f"Sequence: {' -> '.join([ai.title() for ai in sequence])}")
        
        for i, ai_name in enumerate(sequence):
            print(f"\nStep {i+1}: Sending to {ai_name.title()}")
            
            success = self.target_ai(ai_name, current_message)
            
            if not success:
                print(f"Relay failed at {ai_name}")
                break
            
            # In a full system, we would read the response here
            # For now, just continue with the original message
            
            # Pause between relay steps
            time.sleep(2)
        
        # Return to Desktop 0
        self.switch_to_desktop(0)
        print("\nAI relay complete!")

def main():
    """Main function using Kai's proven method"""
    
    targeting = KaiProvenTargeting()
    
    print("\nKai's Proven Method:")
    print("1. Fixed pixel coordinates")
    print("2. Click-to-focus before typing")
    print("3. AppleScript for clean text entry")
    print("4. No emoji, no percentages, no complications")
    
    choice = input(f"\nChoose test:\n1. Test single AI\n2. Test all AIs\n3. Run AI relay\nChoice: ")
    
    if choice == "1":
        ai_name = input("Enter AI name (kai/claude/perplexity/grok): ").lower()
        if ai_name in targeting.ai_targets:
            targeting.test_single_ai(ai_name)
        else:
            print("Invalid AI name")
    
    elif choice == "2":
        targeting.test_all_ais()
    
    elif choice == "3":
        message = input("Enter initial message for relay: ") or "Hello from the AI Council relay system"
        targeting.run_ai_relay(message)
    
    print("\nUsing Kai's proven method - simple and reliable!")

if __name__ == "__main__":
    main()