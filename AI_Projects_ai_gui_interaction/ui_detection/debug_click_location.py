#!/usr/bin/env python3

import pyautogui
import time

def debug_click_location():
    """Debug where we're actually clicking"""
    
    coords = (950, 1944)
    
    print("🎯 Click Location Debug")
    print(f"Will click at: {coords}")
    print("Switch to ChatGPT and watch for the click...")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Move mouse to show where we'll click
    print("🖱️ Moving mouse to target location...")
    pyautogui.moveTo(coords[0], coords[1], duration=1)
    time.sleep(1)
    
    # Click and hold briefly to make it visible
    print("🖱️ Clicking (watch for visual feedback)...")
    pyautogui.click(coords[0], coords[1])
    time.sleep(2)
    
    # Check what application is now active
    print("⌨️ Testing what received focus...")
    pyautogui.typewrite("FOCUS TEST")
    time.sleep(1)
    
    print("✅ Done! Where did 'FOCUS TEST' appear?")
    print("If it appeared in Terminal, the click missed ChatGPT")
    print("If it appeared in ChatGPT input, coordinates are correct!")

def try_different_coords():
    """Try clicking between 'Ask' and 'anything' words"""
    
    # Try the midpoint between "Ask" (950, 1944) and "anything" (1006, 1944)
    midpoint = (978, 1944)
    
    print(f"\n🔄 Trying midpoint coordinates: {midpoint}")
    print("Switch to ChatGPT - clicking in 3 seconds...")
    time.sleep(3)
    
    pyautogui.moveTo(midpoint[0], midpoint[1], duration=1)
    time.sleep(0.5)
    pyautogui.click(midpoint[0], midpoint[1])
    time.sleep(1)
    
    pyautogui.typewrite("MIDPOINT TEST")
    time.sleep(1)
    
    print("✅ Where did 'MIDPOINT TEST' appear?")

def manual_coordinate_finder():
    """Help find the right coordinates manually"""
    
    print("\n🎯 Manual Coordinate Finder")
    print("1. Switch to ChatGPT")
    print("2. Click in the input field manually")
    print("3. Come back to Terminal and press Enter")
    input("Press Enter when ChatGPT input field is focused...")
    
    # Get current mouse position
    current_pos = pyautogui.position()
    print(f"🖱️ Current mouse position: {current_pos}")
    
    print("4. Now I'll test typing at the current mouse position...")
    time.sleep(2)
    pyautogui.typewrite("MANUAL POSITION TEST")
    
    print("✅ Did that work? If yes, use these coordinates:")
    print(f"coords = {current_pos}")

if __name__ == "__main__":
    print("🔍 Debugging click targeting...")
    debug_click_location()
    
    response = input("\nDid 'FOCUS TEST' appear in ChatGPT? (y/n): ")
    
    if response.lower() != 'y':
        try_different_coords()
        
        response2 = input("\nDid 'MIDPOINT TEST' work? (y/n): ")
        
        if response2.lower() != 'y':
            manual_coordinate_finder()
    else:
        print("🎉 Great! Coordinates (950, 1944) are working!")